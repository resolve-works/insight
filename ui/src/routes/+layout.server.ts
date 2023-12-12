export async function load({ locals }) {
	return {
		access_token: locals.access_token,
	};
}
