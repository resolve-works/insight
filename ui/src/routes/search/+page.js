
import { PUBLIC_API_ENDPOINT } from '$env/static/public';

export async function load({ fetch }) {
	const pagestreams = await fetch(PUBLIC_API_ENDPOINT + '/pagestream');
	const results = await fetch(PUBLIC_API_ENDPOINT + '/index');

	return { pagestreams: await pagestreams.json(), results: await results.json() };
}
