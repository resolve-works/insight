
import { connect } from '$lib/amqp.ts';

export async function GET({ locals }) {
    const connection = await connect(locals.access_token)
    const channel = await connection.createChannel()

    // Make sure user queue exists
    const queue = `user-${locals.sub}`
    await channel.assertExchange(queue, 'fanout', { autoDelete: true })
    await channel.assertQueue(queue, { autoDelete: true });
    await channel.bindQueue(queue, queue, '')

    let interval: ReturnType<typeof setInterval>;

    // Forward rabbitmq messages for user
	const readable = new ReadableStream({
		start(ctr) {
            // Pinging ensures that our connection stays alive
            interval = setInterval(() => ctr.enqueue(JSON.stringify({ message: 'ping' })), 30000)

            channel.consume(queue, (message) => {
                if (message !== null) {
                    ctr.enqueue(JSON.stringify({ 
                        routing_key: message.fields.routingKey, 
                        content: JSON.parse(message.content.toString()),
                    }))
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
