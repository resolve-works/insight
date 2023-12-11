
import { env } from '$env/dynamic/private';
import { redirect } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';

function auth_redirect(event: RequestEvent) {
    // No code or previous token, redirect to login
    const url = new URL(env.AUTH_AUTHORIZATION_ENDPOINT)
    url.searchParams.set('scope', 'profile email')
    url.searchParams.set('response_type', 'code')
    url.searchParams.set('client_id', env.AUTH_CLIENT_ID)
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
        console.log('Authenticating with authorization_code')
        // Code granted, get tokens
        const data = { 
            grant_type: 'authorization_code',
            redirect_uri: event.url.origin + event.url.pathname,
            client_id: env.AUTH_CLIENT_ID,
            code, 
        }

        const res = await fetch(env.AUTH_TOKEN_ENDPOINT, {
            method: 'post',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(data).toString(),
        })

        if(res.status !== 200) {
            throw auth_redirect(event);
        }

        const tokens = await res.json();
        console.log('Storing refresh_token and redirecting')
        event.cookies.set('refresh_token', tokens.refresh_token)

        // redirect
        event.url.searchParams.delete('code');
        event.url.searchParams.delete('session_state');
        throw redirect(307, event.url)
    }

    // No code, do we have a refresh token?
    const refresh_token = event.cookies.get('refresh_token')
    if(refresh_token !== undefined) {
        console.log('Refreshing token')
        const data = { 
            grant_type: 'refresh_token', 
            client_id: env.AUTH_CLIENT_ID, 
            refresh_token, 
            scope: 'profile email', 
        }

        const res = await fetch(env.AUTH_TOKEN_ENDPOINT, {
            method: 'post',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(data).toString(),
        })

        // Refresh token failed, remove & re-login
        if(res.status === 400) {
            console.log('Token refresh failed, redirecting to auth')
            event.cookies.delete('refresh_token')
            throw auth_redirect(event)
        }

        const tokens = await res.json();
        console.log('Storing refresh_token, access_token and resolving')
        event.cookies.set('refresh_token', tokens.refresh_token)
        event.locals.access_token = tokens.access_token;

        return resolve(event)
    }

    console.log('Unauthenticated, redirecting')
    throw auth_redirect(event)
}

export function handleFetch({ event, request, fetch }) {
    const url = new URL(request.url)
    if (url.host === event.url.host) {
        request.headers.set('Authorization', `Bearer ${event.locals.access_token}`);
    }

    return fetch(request);
}

