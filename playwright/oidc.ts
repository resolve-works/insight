
export class OIDCProvider {
    access_token: string

    async authenticate(username: string, password: string) {
        const data = {
            username,
            password,
            grant_type: "password",
            client_id: "admin-cli",
        }

        const res = await fetch('https://localhost:8000/realms/master/protocol/openid-connect/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams(data).toString(),
        });

        const {access_token} = await res.json()
        this.access_token = access_token
    }

    create_user(username: string, password: string) {
        const data = {
            enabled: true,
            username,
            email: `${username}@example.com`,
            firstName: username,
            lastName: "insight",
            credentials: [{type: "password", value: password, temporary: false, }]
        }

        return fetch('https://localhost:8000/admin/realms/insight/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.access_token}`,
            },
            body: JSON.stringify(data),
        })
    }

    delete_user(url: string) {
        return fetch(url, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${this.access_token}`,
            }
        })
    }
}

