
<script>
  import { onMount, onDestroy } from "svelte";
  import axios from "axios";
  import { Chart, registerables } from "chart.js";
  Chart.register(...registerables);

  let chart;
  const baseUrl = import.meta.env.VITE_API_BASE_URL;

  onMount(async () => {
    try {
      const response = await axios.get(`${baseUrl}/data`);
      const voterData = response.data;

      // Define the age groups and organize data
      const ageGroups = ["18 to 24", "22 to 44", "45 to 64", "65 and Over"];
      const ageGroupData = ageGroups.map(group =>
        voterData.map(entry => entry[group]).filter(val => val !== null)
      );

      // Calculate quartiles and median for each age group
      const boxPlotData = ageGroupData.map(groupData => {
        const sortedData = [...groupData].sort((a, b) => a - b);
        const q1 = sortedData[Math.floor(sortedData.length * 0.25)];
        const median = sortedData[Math.floor(sortedData.length * 0.5)];
        const q3 = sortedData[Math.floor(sortedData.length * 0.75)];
        const min = Math.min(...sortedData);
        const max = Math.max(...sortedData);
        return { min, q1, median, q3, max };
      });

      // Prepare data for Chart.js
      const datasets = ageGroups.map((group, i) => ({
        label: group,
        data: [
          boxPlotData[i].min,
          boxPlotData[i].q1,
          boxPlotData[i].median,
          boxPlotData[i].q3,
          boxPlotData[i].max,
        ],
        backgroundColor: "rgba(54, 162, 235, 0.2)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1,
      }));

      // Create the chart
      const ctx = document.getElementById("ageGroupBoxPlot").getContext("2d");
      chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ageGroups,
          datasets: datasets.map((dataset, index) => ({
            label: dataset.label,
            data: [
              { x: dataset.label, y: dataset.data[0] },
              { x: dataset.label, y: dataset.data[1] },
              { x: dataset.label, y: dataset.data[2] },
              { x: dataset.label, y: dataset.data[3] },
              { x: dataset.label, y: dataset.data[4] },
            ],
          })),
        },
        options: {
          responsive: true,
          scales: {
            x: {
              title: { display: true, text: "Age Group" },
            },
            y: {
              title: { display: true, text: "Turnout Rate (%)" },
              beginAtZero: true,
            },
          },
          plugins: {
            legend: {
              display: true,
              position: "top",
            },
          },
        },
      });
    } catch (error) {
      console.error("Failed to fetch data:", error);
    }
  });

  onDestroy(() => {
    if (chart) chart.destroy();
  });
</script>

<canvas id="ageGroupBoxPlot" width="400" height="200"></canvas>

<style>
  canvas {
    max-width: 100%;
    height: auto;
  }
</style>
