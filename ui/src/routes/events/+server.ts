
import { env } from '$env/dynamic/private';
import amqplib from 'amqplib';

export async function GET({ locals }) {
    const password = `${encodeURIComponent(locals.access_token)}`
    const connection = await amqplib.connect(`amqp://username:${password}@${env.RABBITMQ_HOST}`);

    const queue = `user-${locals.sub}`

    const channel = await connection.createChannel();
    await channel.assertQueue(queue, { autoDelete: true });

    let interval: ReturnType<typeof setInterval>;

    // Forward rabbitmq messages for user
	const readable = new ReadableStream({
		start(ctr) {
            // Pinging ensures that our connection stays alive
            interval = setInterval(() => ctr.enqueue(JSON.stringify({ message: 'ping' })), 30000)

            channel.consume(queue, (message) => {
                if (message !== null) {
                    ctr.enqueue(message.content)
                    channel.ack(message);
                } else {
                    console.log('Consumer cancelled by server');
                }
            });
		},
		cancel() {
            clearInterval(interval)
            connection.close()
		}
	});

	return new Response(readable, {
		headers: {
			'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
		}
	});
}
