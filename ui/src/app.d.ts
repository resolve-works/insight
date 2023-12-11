// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
    namespace App {
		// interface Error {}
        interface Locals {
            access_token: String;
        }
		// interface PageData {}
		// interface Platform {}
	}
}

export {};
