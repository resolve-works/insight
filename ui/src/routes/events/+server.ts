
import amqplib from 'amqplib';

export async function GET({ locals }) {
    const password = `${encodeURIComponent(locals.access_token)}`
    const connection = await amqplib.connect(`amqp://username:${password}@rabbitmq`);

    const queue = `user-${locals.sub}`

    const channel = await connection.createChannel();
    await channel.assertQueue(queue, { autoDelete: true });

    // Forward rabbitmq messages for user
	const readable = new ReadableStream({
		start(ctr) {
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
            connection.close()
		}
	});

	return new Response(readable, {
		headers: {
			'content-type': 'text/event-stream',
		}
	});
}
