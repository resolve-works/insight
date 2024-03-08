
import { env } from '$env/dynamic/private';
import amqplib from 'amqplib';
import type { Connection, Channel as AMQPChannel } from 'amqplib';

export function connect(access_token: string) {
    const password = `${encodeURIComponent(access_token)}`
    return amqplib.connect(`amqp://username:${password}@${env.RABBITMQ_HOST}`);
}

export class Channel {
    connection: Connection;
    channel: AMQPChannel;

    constructor(connection: Connection, channel: AMQPChannel) {
        this.connection = connection;
        this.channel = channel;
    }

    static async connect(access_token: string) {
        const connection = await connect(access_token)
        const channel = await connection.createChannel()
        return new Channel(connection, channel)
    }

    async publish(routing_key: string, data: Record<string, any>) {
        this.channel.publish('insight', routing_key, Buffer.from(JSON.stringify(data)));
        return this
    }

    async close() {
        await this.channel.close()
        this.connection.close()
    }
}
