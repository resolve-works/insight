// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
    namespace App {
		// interface Error {}
        interface Locals {
            access_token: string;
            access_key_id: string;
            secret_access_key: string;
            session_token: string;
        }
		// interface PageData {}
		// interface Platform {}
	}
}

export {};
