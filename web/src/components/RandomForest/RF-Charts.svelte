
<script>
  import { onMount } from "svelte";
  import { Chart, registerables } from "chart.js";
  Chart.register(...registerables);

  export let chartType = "bar";
  export let chartData = null;
  export let uniqueId = "";

  const colorMap = {
    "White": "rgba(52, 211, 153, 1)", // Teal Green
    "Black": "rgba(99, 102, 241, 1)", // Indigo
    "Asian": "rgba(244, 114, 182, 1)", // Pink
    "Hispanic": "rgba(34, 211, 238, 1)", // Cyan
  };

  let chart;

  function renderChart() {
    if (chart) chart.destroy();

    const ctx = document.querySelector(`#${uniqueId}`).getContext("2d");

    if (chartType === "bar") {
      chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: chartData?.years || [],
          datasets: Object.keys(chartData?.predictions || {}).map((col) => ({
            label: col,
            data: chartData?.predictions[col] || [],
            backgroundColor: colorMap[col] || "rgba(128, 128, 128, 0.5)",
            borderColor: colorMap[col] || "rgba(128, 128, 128, 1)",
            borderWidth: 1,
          })),
        },
        options: {
          responsive: true,
          scales: {
            x: { title: { display: true, text: "Year" } },
            y: { title: { display: true, text: "Value" }, beginAtZero: true },
          },
        },
      });
    } else if (chartType === "doughnut") {
      chart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: Object.keys(chartData?.predictions || {}),
          datasets: [
            {
              data: Object.keys(chartData?.predictions || {}).map((col) =>
                (chartData?.predictions[col] || []).reduce((sum, val) => sum + val, 0)
              ),
              backgroundColor: Object.keys(chartData?.predictions || {}).map((col) => colorMap[col]),
            },
          ],
        },
        options: {
          responsive: true,
        },
      });
    }
  }

  $: if (chartData) {
    renderChart();
  }

  onMount(renderChart);
</script>

<canvas id={uniqueId} class="chart"></canvas>

<style>
  canvas.chart {
    max-width: 100%;
    max-height: 100%;
    margin: auto;
  }
</style>

