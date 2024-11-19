
<script>
  import { onMount, onDestroy } from "svelte";
  import axios from "axios";
  import { Chart, registerables } from "chart.js";
  Chart.register(...registerables);

  const baseUrl = import.meta.env.VITE_API_BASE_URL;
  let chart;

  onMount(async () => {
    try {
      const response = await axios.get(`${baseUrl}/data`);
      const voterData = response.data;

      // Define race groups and organize data
      const raceGroups = ["White", "Black", "Hispanic", "Asian"];
      const raceGroupData = raceGroups.map(group =>
        voterData.map(entry => entry[group]).filter(val => val !== null)
      );

      // Calculate quartiles and median for each race group
      const boxPlotData = raceGroupData.map(groupData => {
        const sortedData = [...groupData].sort((a, b) => a - b);
        const q1 = sortedData[Math.floor(sortedData.length * 0.25)];
        const median = sortedData[Math.floor(sortedData.length * 0.5)];
        const q3 = sortedData[Math.floor(sortedData.length * 0.75)];
        const min = Math.min(...sortedData);
        const max = Math.max(...sortedData);
        return { min, q1, median, q3, max };
      });

      // Custom colors for each race group
      const colors = [
        "rgba(255, 99, 132, 0.2)", // Red for White
        "rgba(54, 162, 235, 0.2)", // Blue for Black
        "rgba(255, 206, 86, 0.2)", // Yellow for Hispanic
        "rgba(75, 192, 192, 0.2)"  // Teal for Asian
      ];
      const borderColors = [
        "rgba(255, 99, 132, 1)",   // Red border for White
        "rgba(54, 162, 235, 1)",   // Blue border for Black
        "rgba(255, 206, 86, 1)",   // Yellow border for Hispanic
        "rgba(75, 192, 192, 1)"    // Teal border for Asian
      ];

      // Prepare data for Chart.js
      const datasets = raceGroups.map((group, i) => ({
        label: group,
        data: [
          boxPlotData[i].min,
          boxPlotData[i].q1,
          boxPlotData[i].median,
          boxPlotData[i].q3,
          boxPlotData[i].max,
        ],
        backgroundColor: colors[i],
        borderColor: borderColors[i],
        borderWidth: 1,
      }));

      // Create the chart
      const ctx = document.getElementById("raceBoxPlot").getContext("2d");
      chart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: raceGroups,
          datasets: datasets.map((dataset, index) => ({
            label: dataset.label,
            data: [
              { x: dataset.label, y: dataset.data[0] },
              { x: dataset.label, y: dataset.data[1] },
              { x: dataset.label, y: dataset.data[2] },
              { x: dataset.label, y: dataset.data[3] },
              { x: dataset.label, y: dataset.data[4] },
            ],
            backgroundColor: dataset.backgroundColor,
            borderColor: dataset.borderColor,
            borderWidth: dataset.borderWidth,
          })),
        },
        options: {
          responsive: true,
          scales: {
            x: {
              title: { display: true, text: "Race/Ethnicity" },
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

<canvas id="raceBoxPlot" width="400" height="200"></canvas>

<style>
  canvas {
    max-width: 100%;
    height: auto;
  }
</style>

