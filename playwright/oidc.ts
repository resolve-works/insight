import { randomUUID } from 'crypto';

export class OIDCProvider {
	access_token: string;

	async authenticate(username: string, password: string) {
		const data = {
			username,
			password,
			grant_type: 'password',
			client_id: 'admin-cli'
		};

		const res = await fetch('https://localhost:8000/realms/master/protocol/openid-connect/token', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded'
			},
			body: new URLSearchParams(data).toString()
		});

		const { access_token } = await res.json();
		this.access_token = access_token;
	}

	async create_user() {
		const username = randomUUID();
		const password = 'insight';

		const data = {
			enabled: true,
			username,
			email: `${username}@example.com`,
			firstName: username,
			lastName: 'insight',
			credentials: [{ type: 'password', value: password, temporary: false }]
		};

		const res = await fetch('https://localhost:8000/admin/realms/insight/users', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${this.access_token}`
			},
			body: JSON.stringify(data)
		});

		const url = res.headers.get('location');
		if (!url) {
			throw new Error('User location not found in headers');
		}

		return { url, username, password };
	}

	delete_user(url: string) {
		return fetch(url, {
			method: 'DELETE',
			headers: {
				Authorization: `Bearer ${this.access_token}`
			}
		});
	}
}
