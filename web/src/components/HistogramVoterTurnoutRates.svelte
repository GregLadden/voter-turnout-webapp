<script>
  import { onMount, onDestroy } from "svelte";
  import axios from "axios";
  import { Chart, registerables } from "chart.js";
  Chart.register(...registerables);

  const baseUrl = import.meta.env.VITE_API_BASE_URL;
  let chart;
  let data = []; // Data for the plot

  onMount(async () => {
    try {
      // Fetch the data from the backend
      const response = await axios.get(`${baseUrl}/data`);
      const voterData = response.data;

      // Sort data by year
      const sortedData = voterData.sort((a, b) => a.Year - b.Year);

      // Extract years and voter turnout values
      const years = sortedData.map((entry) => entry.Year);
      const turnoutRates = sortedData.map((entry) => entry["Total Voter Turnout"]);

      // Render the chart after data is loaded
      const ctx = document.getElementById("voterTurnoutChart").getContext("2d");
      chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: years,
          datasets: [
            {
              label: "Total Voter Turnout (%)",
              data: turnoutRates,
              backgroundColor: "rgba(34, 139, 34, 0.6)", // green
              borderColor: "rgba(34, 139, 34, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            x: {
              title: {
                display: true,
                text: "Year",
              },
            },
            y: {
              title: {
                display: true,
                text: "Turnout Rate (%)",
              },
              beginAtZero: true,
            },
          },
        },
      });
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  });

  // Clean up chart when component is destroyed
  onDestroy(() => {
    if (chart) chart.destroy();
  });
</script>

<canvas id="voterTurnoutChart" width="400" height="200"></canvas>

<style>
  /* Add any custom styling for the chart here */
  canvas {
    max-width: 100%;
    height: auto;
  }
</style>

