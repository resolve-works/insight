
import { env } from '$env/dynamic/private';
import amqplib from 'amqplib';

export function amqp_connect(access_token: string) {
    const password = `${encodeURIComponent(access_token)}`
    return amqplib.connect(`amqp://username:${password}@${env.RABBITMQ_HOST}`);
}
