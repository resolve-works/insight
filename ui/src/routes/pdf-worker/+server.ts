
import fs from 'fs';

export async function GET() {
    const file = fs.createReadStream('node_modules/pdfjs-dist/build/pdf.worker.mjs');

	return new Response(file, { headers: { 'Content-Type': 'application/javascript' } });
}
