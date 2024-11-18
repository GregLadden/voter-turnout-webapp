
<script>
  import { onMount } from "svelte";
  import Chart from "chart.js/auto";

  export let data = [];
  export let label = "";

  let canvas;

  onMount(() => {
    if (canvas) {
      new Chart(canvas, {
        type: "bar",
        data: {
          labels: data.map((_, index) => index + 1),
          datasets: [
            {
              label: `Distribution of ${label}`,
              data: data,
              backgroundColor: "rgba(59, 130, 246, 0.5)", // Tailwind blue-500
              borderColor: "rgba(59, 130, 246, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            x: { title: { display: true, text: label } },
            y: { title: { display: true, text: "Frequency" } },
          },
        },
      });
    }
  });
</script>

<canvas bind:this={canvas}></canvas>
