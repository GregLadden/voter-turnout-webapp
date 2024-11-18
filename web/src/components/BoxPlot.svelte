
<script>
  import { onMount } from "svelte";
  import Chart from "chart.js/auto";
  import "chartjs-chart-box-and-violin-plot";

  export let data = [];
  export let label = "";

  let canvas;

  onMount(() => {
    if (canvas) {
      new Chart(canvas, {
        type: "boxplot",
        data: {
          labels: [label],
          datasets: [
            {
              label: `Box Plot of ${label}`,
              data: [data],
              backgroundColor: "rgba(59, 130, 246, 0.5)",
              borderColor: "rgba(59, 130, 246, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            x: { title: { display: true, text: label } },
            y: { title: { display: true, text: "Values" } },
          },
        },
      });
    }
  });
</script>

<canvas bind:this={canvas}></canvas>
