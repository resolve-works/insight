
import { AUTH_CLIENT_ID, AUTH_AUTHORIZATION_ENDPOINT, AUTH_TOKEN_ENDPOINT } from '$env/static/private';
import { redirect } from '@sveltejs/kit';

export async function handle({event, resolve}) {
    if(event.cookies.get('access_token') === undefined) {
        const code = event.url.searchParams.get('code')
        const redirect_uri = event.url.origin + event.url.pathname

        if(code !== null) {
            const data = new FormData()
            data.set('grant_type', 'authorization_code')
            data.set('redirect_uri', redirect_uri)
            data.set('client_id', AUTH_CLIENT_ID)
            data.set('code', code)

            const res = await fetch(AUTH_TOKEN_ENDPOINT, {
                method: 'post',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams(data).toString(),
            })

            if(res.status !== 200) {
                throw redirect(307, redirect_uri)
            }

            const token = await res.json()
            console.log(token)

            event.cookies.set('access_token', token.access_token)
            event.cookies.set('refresh_token', token.refresh_token)

            throw redirect(307, redirect_uri)
        } else {
            const url = new URL(AUTH_AUTHORIZATION_ENDPOINT)
            url.searchParams.set('scope', 'profile email')
            url.searchParams.set('response_type', 'code')
            url.searchParams.set('client_id', AUTH_CLIENT_ID)
            url.searchParams.set('redirect_uri', redirect_uri)

            throw redirect(307, url)
        }
    }

    return resolve(event)
}

//export async function handleFetch({ event, request, fetch }) {
    //console.log(event.url)
    //console.log(request)
	//if (request.url.startsWith('https://api.my-domain.com/')) {
		//request.headers.set('cookie', event.request.headers.get('cookie'));
	//}

	//return fetch(request);
//}
