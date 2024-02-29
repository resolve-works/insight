
import { env } from '$env/dynamic/public';
import { XMLParser } from 'fast-xml-parser';
import { redirect } from '@sveltejs/kit';
import type { RequestEvent, HandleFetch } from '@sveltejs/kit';

import { get_tokens_through_refresh, get_storage_tokens, InvalidRefreshTokenError } from '$lib/auth.ts';

function auth_redirect(event: RequestEvent) {
    // No code or previous token, redirect to login
    const url = new URL(env.PUBLIC_OIDC_ENDPOINT + '/auth')
    url.searchParams.set('scope', 'profile email')
    url.searchParams.set('response_type', 'code')
    url.searchParams.set('client_id', env.PUBLIC_OIDC_CLIENT_ID)
    url.searchParams.set('redirect_uri', event.url.origin + event.url.pathname)

    return redirect(307, url)
}

export async function handle({event, resolve}) {
    if(event.url.pathname.startsWith('/api')) {
        return resolve(event);
    }

    // Did the authentication platform just redirect to us with a new code?
    const code = event.url.searchParams.get('code')
    if(code !== null) {
        // Code granted, get tokens
        const data = { 
            grant_type: 'authorization_code',
            redirect_uri: event.url.origin + event.url.pathname,
            client_id: env.PUBLIC_OIDC_CLIENT_ID,
            code, 
        }

        const token_response = await fetch(env.PUBLIC_OIDC_ENDPOINT + '/token', {
            method: 'post',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(data).toString(),
        })

        if(token_response.status !== 200) {
            throw auth_redirect(event);
        }

        const tokens = await token_response.json();
        event.cookies.set('refresh_token', tokens.refresh_token, { path: '/' })

        // redirect to clear URL of params
        event.url.searchParams.delete('code');
        event.url.searchParams.delete('session_state');
        throw redirect(307, event.url)
    }

    // No code, do we have a refresh token?
    const refresh_token = event.cookies.get('refresh_token')
    if(refresh_token !== undefined) {
        try {
            const tokens = await get_tokens_through_refresh(refresh_token)
            const storage_tokens = await get_storage_tokens(tokens.access_token)
            event.locals = { access_token: tokens.access_token, ...storage_tokens }

            // Refresh token was good, store new response
            event.cookies.set('refresh_token', tokens.refresh_token, { path: '/' })

            // Resolve event with new tokens
            return resolve(event)
        } catch(error) {
            if(error instanceof InvalidRefreshTokenError) {
                // Remove stale token and redirect to login
                event.cookies.delete('refresh_token', { path: '/' })
                throw auth_redirect(event)
            } else {
                throw error;
            }
        }

    }

    throw auth_redirect(event)
}

export const handleFetch: HandleFetch = async ({ request, fetch }) => {
    console.log('fetchin')
	return fetch(request);
};
