
export async function load({ fetch }) {
	const res = await fetch(`/api/v1/`);
	const item = await res.json();

	return { item };
}
