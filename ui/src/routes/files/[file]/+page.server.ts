
import { env } from '$env/dynamic/public';
import { presignSignatureV4 } from '../../../../node_modules/minio/src/signing.ts'

const REGION = 'insight';

export async function load({ parent, params, fetch }) {
    const { access_token, access_key_id, secret_access_key, session_token } = await parent();

    const res = await fetch(`/api/v1/file?id=eq.${params.file}`, {
        headers: { Authorization: `Bearer ${access_token}` }
    })
    const files = await res.json();
    const file = files[0]

    const url = new URL(env.PUBLIC_STORAGE_ENDPOINT)

    const request = {
        protocol: url.protocol,
        port: parseInt(url.port),
        method: 'GET',
        path: '/' + env.PUBLIC_STORAGE_BUCKET + '/' + file.path,
        headers: {
            host: url.host
        },
    }

    return {
        ...file,
        url: presignSignatureV4(request, access_key_id, secret_access_key, session_token, REGION, new Date(), 60 * 60),
    }
}
