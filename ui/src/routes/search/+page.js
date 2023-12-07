
import { PUBLIC_API_ENDPOINT } from '$env/static/public';

export async function load({ fetch }) {
	const res = await fetch(PUBLIC_API_ENDPOINT + '/pagestream');
	const item = await res.json();

	return { item };
}
