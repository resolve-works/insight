
import { env } from '$env/dynamic/public';
import { presignSignatureV4 } from 'minio/dist/esm/signing.mjs'

/**
 * Sign a S3 storage path for method. Keep this on the server because of the crypto dependency
 */
export function sign(path: string, locals: App.Locals, method: string = 'GET') {
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

    return presignSignatureV4(request, access_key_id, secret_access_key, session_token, 'insight', new Date(), 60 * 60)
}
