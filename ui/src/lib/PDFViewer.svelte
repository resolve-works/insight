<script lang="ts">
    import { onMount } from 'svelte';

    export let url: string;
    export let index: string;

    let canvas: HTMLCanvasElement;

    onMount(async () => {
        const { getDocument, GlobalWorkerOptions } = await import('pdfjs-dist');

        GlobalWorkerOptions.workerSrc = '/pdf-worker';

        const pdf = await getDocument(url).promise;
        const page = await pdf.getPage(parseInt(index))

        const scale = 1.5;
        const viewport = page.getViewport({ scale: scale, });
        // Support HiDPI-screens.
        const outputScale = window.devicePixelRatio || 1;

        const context = canvas.getContext('2d');

        canvas.width = Math.floor(viewport.width * outputScale);
        canvas.height = Math.floor(viewport.height * outputScale);
        canvas.style.width = Math.floor(viewport.width) + "px";
        canvas.style.height =  Math.floor(viewport.height) + "px";

        const transform = outputScale !== 1
          ? [outputScale, 0, 0, outputScale, 0, 0]
          : null;

        const renderContext = {
          canvasContext: context,
          transform: transform,
          viewport: viewport
        };
        page.render(renderContext);
    })
</script>

<article>
    <canvas bind:this={canvas} />
</article>

<style>
    article {
        display: grid;
        justify-content: center;
    }
</style>
