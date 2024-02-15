
import { env } from '$env/dynamic/public';

/**
 * Wrapper for Postgrest API and OpenSearch Index. This one interface is here
 * to allow for easy stubbing in testing
 */
export class Insight {
    access_token: string

    constructor(access_token: string) {
        this.access_token = access_token;
    }

    // TODO - Allow bodyInit type being object here
    fetch(path: string, config: RequestInit) {
        const defaults = { method: 'GET', headers: {} }
        config = { ...defaults, ...config }

        // Add auth
        config.headers['Authorization'] = `Bearer ` + this.access_token;
        
        // Automatically handle JSON bodies
        if(config.body) {
            config.headers['Content-Type'] = 'application/json';
            config.body = JSON.stringify(config.body);
        }

        return fetch(`${env.PUBLIC_API_ENDPOINT}${path}`, config)
    }

    async post(path: string, body: BodyInit) {
        const response = await this.fetch(path, { 
            method: 'POST', 
            headers: { 'Prefer': 'return=representation' },
            body, 
        })
        if(response.status != 201) {
            throw new Error(`Could not POST to ${path}: ${response.text}`)
        }
        return (await response.json())[0]
    }

    async patch(path: string, id: string, body: BodyInit) {
        path = `${path}?id=eq.${id}`;
        const response = await this.fetch(path, { method: 'PATCH', body })
        if(response.status != 204) {
            throw new Error(`Could not patch ${path}: ${response.text}`)
        }
    }

    async rpc(path: string, id: string) {
        const response = await this.fetch(`/rpc${path}`, { method: 'POST', body: { id }})
        if(response.status != 204) {
            throw new Error(`Could not trigger ${path}: ${response.text}`)
        }
    }
}

