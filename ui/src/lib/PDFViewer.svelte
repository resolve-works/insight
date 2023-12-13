<script lang="ts">
    import * as pdfjs from "pdfjs-dist";
    import { onMount } from 'svelte';

    export let url: URL;
    export let index: string;

    let canvas: HTMLCanvasElement;

    onMount(async () => {
        pdfjs.GlobalWorkerOptions.workerSrc = '/pdf-worker';

        const pdf = await pdfjs.getDocument(url).promise;
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

<canvas bind:this={canvas} />
