
import { env } from '$env/dynamic/private';
import { redirect } from '@sveltejs/kit';
import type { Cookies, Request } from '@sveltejs/kit';

type Token = {
  access_token: string;
  refresh_token: string;
};

function store_tokens(cookies: Cookies, token: Token) {
    const config = { secure: true, httpOnly: true }
    cookies.set('access_token', token.access_token, config)
    cookies.set('refresh_token', token.refresh_token, config)
}

function authorize_request(cookies: Cookies, request: Request) {
    request.headers.set('Authorization', `Bearer ${cookies.get('access_token')}`);
}

export async function handle({event, resolve}) {
    // No token, no access
    if(event.cookies.get('access_token') === undefined) {
        const code = event.url.searchParams.get('code')
        const redirect_uri = event.url.origin + event.url.pathname

        if(code !== null) {
            // Code granted, get tokens
            const data = new FormData()
            data.set('grant_type', 'authorization_code')
            data.set('redirect_uri', redirect_uri)
            data.set('client_id', env.AUTH_CLIENT_ID)
            data.set('code', code)

            const res = await fetch(env.AUTH_TOKEN_ENDPOINT, {
                method: 'post',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(data).toString(),
            })
            if(res.status !== 200) {
                throw redirect(307, redirect_uri)
            }

            store_tokens(event.cookies, await res.json()) 

            throw redirect(307, redirect_uri)
        } else {
            // Request auth code
            const url = new URL(env.AUTH_AUTHORIZATION_ENDPOINT)
            url.searchParams.set('scope', 'profile email')
            url.searchParams.set('response_type', 'code')
            url.searchParams.set('client_id', env.AUTH_CLIENT_ID)
            url.searchParams.set('redirect_uri', redirect_uri)

            throw redirect(307, url)
        }
    }

    return resolve(event)
}

export async function handleFetch({ event, request, fetch }) {
    // Requests to self should be authed
    const url = new URL(request.url)
    if (url.host === event.url.host) {
        authorize_request(event.cookies, request)

        const response = await fetch(request.clone());
        if(response.status === 401) {
            // Token expired? Try refresh
            const data = new FormData()
            data.set('grant_type', 'refresh_token')
            data.set('client_id', env.AUTH_CLIENT_ID)
            data.set('refresh_token', `${event.cookies.get('refresh_token')}`)
            data.set('scope', 'profile email')

            const res = await fetch(env.AUTH_TOKEN_ENDPOINT, {
                method: 'post',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(data).toString(),
            })
            
            // Refresh token failed, remove & re-login
            if(res.status !== 200) {
                event.cookies.delete('acccess_token');
                event.cookies.delete('refresh_token');
                throw redirect(307, event.url.href)
            }

            store_tokens(event.cookies, await res.json())
            authorize_request(event.cookies, request)

            // Re-fetch with new tokens
            return fetch(request)
        }
        return response
    }

    return fetch(request)
}
