
import { env } from '$env/dynamic/public';
import * as Minio from 'minio';

export async function load({ parent, params, fetch }) {
    const { access_token, access_key_id, secret_access_key, session_token } = await parent();

    const res = await fetch(`/api/v1/file?id=eq.${params.file}`, {
        headers: { Authorization: `Bearer ${access_token}` }
    })
    const files = await res.json();
    const file = files[0]

    const url = new URL(env.PUBLIC_STORAGE_ENDPOINT)
    const minio = new Minio.Client({
        endPoint: url.hostname,
        port: parseInt(url.port),
        useSSL: url.protocol === 'https:',
        accessKey: access_key_id,
        secretKey: secret_access_key,
        sessionToken: session_token,
        region: 'insight',
    })

    return {
        ...file,
        url: minio.presignedGetObject(env.PUBLIC_STORAGE_BUCKET, file.path, 60 * 60),
    }
}
