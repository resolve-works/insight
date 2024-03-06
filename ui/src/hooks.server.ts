
import { env } from '$env/dynamic/private';
import { env as public_env } from '$env/dynamic/public';
import { redirect } from '@sveltejs/kit';
import type { RequestEvent, HandleFetch } from '@sveltejs/kit';

import { get_tokens_through_refresh, get_storage_tokens, InvalidRefreshTokenError } from '$lib/auth.ts';

function auth_redirect(event: RequestEvent) {
    // No code or previous token, redirect to login
    const url = new URL(public_env.PUBLIC_OIDC_ENDPOINT + '/auth')
    url.searchParams.set('scope', 'profile email')
    url.searchParams.set('response_type', 'code')
    url.searchParams.set('client_id', env.OIDC_CLIENT_ID)
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
            client_id: env.OIDC_CLIENT_ID,
            code, 
        }

        const token_response = await fetch(public_env.PUBLIC_OIDC_ENDPOINT + '/token', {
            method: 'post',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(data).toString(),
        })

        if(token_response.status !== 200) {
            throw auth_redirect(event);
        }

        const { refresh_token } = await token_response.json();
        event.cookies.set('refresh_token', refresh_token, { path: '/' })

        // redirect to clear URL of params
        event.url.searchParams.delete('code');
        event.url.searchParams.delete('session_state');
        event.url.searchParams.delete('iss');
        throw redirect(307, event.url)
    }

    // TODO - don't always refresh
    // No code, do we have a refresh token?
    if(event.cookies.get('refresh_token') !== undefined) {
        try {
            const { access_token, refresh_token } 
                = await get_tokens_through_refresh(event.cookies.get('refresh_token') as string) 
                
            const storage_tokens = await get_storage_tokens(access_token)

            // Parse JWT payload to get claims
            const payload = access_token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
            const payload_data = JSON.parse(atob(payload))

            event.locals = { 
                access_token,
                ...storage_tokens,
                sub: payload_data.sub,
            }

            // Refresh token was good, store new response
            event.cookies.set('refresh_token', refresh_token, { path: '/' })

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

export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
    const url = new URL(request.url)

    if(url.pathname.startsWith('/api/v1')) {
        request.headers.append('Authorization', 'Bearer ' + event.locals.access_token)
    }

	return fetch(request);
};
