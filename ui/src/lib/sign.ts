
import { env } from '$env/dynamic/public';
import { presignSignatureV4 } from 'minio/dist/esm/signing.mjs'

// Seems to not matter, though is required
const REGION = 'insight';

export default function sign(path: string, locals: App.Locals, method: string = 'GET') {
    const { access_key_id, secret_access_key, session_token } = locals;
    const url = new URL(env.PUBLIC_STORAGE_ENDPOINT)

    const request = {
        protocol: url.protocol,
        port: url.port,
        method,
        path: '/' + env.PUBLIC_STORAGE_BUCKET + '/' + path,
        headers: {
            host: url.host
        },
    }

    return presignSignatureV4(request, access_key_id, secret_access_key, session_token, REGION, new Date(), 60 * 60)
}
