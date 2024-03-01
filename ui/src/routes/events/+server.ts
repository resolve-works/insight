
import amqplib from 'amqplib';

export async function GET({ locals }) {
    const password = `${encodeURIComponent(locals.access_token)}`
    const conn = await amqplib.connect(`amqp://username:${password}@rabbitmq`);

    const channel = await conn.createChannel();

	const readable = new ReadableStream({
		start(ctr) {
			this.interval = setInterval(() => ctr.enqueue(`data: ${new Date().toISOString()}\n\n`), 1000);
		},
		cancel() {
			clearInterval(this.interval);
		}
	});

	return new Response(readable, {
		headers: {
			'content-type': 'text/event-stream',
		}
	});
}
