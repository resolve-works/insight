
import { env as private_env } from '$env/dynamic/private';
import { env as public_env } from '$env/dynamic/public';
import { XMLParser } from 'fast-xml-parser';
import { redirect } from '@sveltejs/kit';
import type { RequestEvent } from '@sveltejs/kit';

function auth_redirect(event: RequestEvent) {
    // No code or previous token, redirect to login
    const url = new URL(private_env.AUTH_AUTHORIZATION_ENDPOINT)
    url.searchParams.set('scope', 'profile email')
    url.searchParams.set('response_type', 'code')
    url.searchParams.set('client_id', private_env.AUTH_CLIENT_ID)
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
            client_id: private_env.AUTH_CLIENT_ID,
            code, 
        }

        const token_response = await fetch(private_env.AUTH_TOKEN_ENDPOINT, {
            method: 'post',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(data).toString(),
        })

        if(token_response.status !== 200) {
            throw auth_redirect(event);
        }

        const tokens = await token_response.json();
        event.cookies.set('refresh_token', tokens.refresh_token, { path: '/' })

        // redirect
        event.url.searchParams.delete('code');
        event.url.searchParams.delete('session_state');
        throw redirect(307, event.url)
    }

    // No code, do we have a refresh token?
    const refresh_token = event.cookies.get('refresh_token')
    if(refresh_token !== undefined) {
        const data = { 
            grant_type: 'refresh_token', 
            client_id: private_env.AUTH_CLIENT_ID, 
            refresh_token, 
            scope: 'profile email', 
        }

        const token_response = await fetch(private_env.AUTH_TOKEN_ENDPOINT, {
            method: 'post',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(data).toString(),
        })

        // Refresh token failed, remove & re-login
        if(token_response.status === 400) {
            event.cookies.delete('refresh_token')
            throw auth_redirect(event)
        }

        // Everything good, store access token for access to API & search index
        const tokens = await token_response.json();
        event.cookies.set('refresh_token', tokens.refresh_token, { path: '/' })
        event.locals.access_token = tokens.access_token;

        // Fetch timed S3 credentials
        const url = new URL(public_env.PUBLIC_STORAGE_ENDPOINT)
        url.searchParams.set("Action", "AssumeRoleWithWebIdentity")
        url.searchParams.set("Version", "2011-06-15")
        url.searchParams.set("DurationSeconds", "3600")
        url.searchParams.set("WebIdentityToken", tokens.access_token)
        const s3_response = await fetch(url, { method: 'post' })

        const parser = new XMLParser();
        const body = parser.parse(await s3_response.text());
        const { AccessKeyId: access_key_id, SecretAccessKey: secret_access_key, SessionToken: session_token } 
            = body.AssumeRoleWithWebIdentityResponse.AssumeRoleWithWebIdentityResult.Credentials;
        event.locals = { ...event.locals, access_key_id, secret_access_key, session_token }

        return resolve(event)
    }

    throw auth_redirect(event)
}

export function handleFetch({ event, request, fetch }) {
    const url = new URL(request.url)
    if (url.host === event.url.host) {
        request.headers.set('Authorization', `Bearer ${event.locals.access_token}`);
    }

    return fetch(request);
}

