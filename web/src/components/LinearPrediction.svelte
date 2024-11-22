
<script>
  import axios from "axios";
  import { onMount } from "svelte";
  import { Chart, registerables } from "chart.js";
  Chart.register(...registerables);

  let columns = []; // List of available columns
  let selectedColumns = []; // User-selected columns
  let predictionYears = "2025,2030,2040";
  let responseMessage = null;
  let responseData = null;
  let errorMessage = null;
  let chart;

  const baseUrl = import.meta.env.VITE_API_BASE_URL;

  // Define a color map for the columns
  const colorMap = {
    "White": "rgba(75, 192, 192, 1)",
    "Black": "rgba(54, 162, 235, 1)",
    "Asian": "rgba(255, 99, 132, 1)",
    "Hispanic": "rgba(255, 206, 86, 1)",
    "Male": "rgba(153, 102, 255, 1)",
    "Female": "rgba(255, 159, 64, 1)",
    "18 to 24": "rgba(0, 128, 128, 1)",
    "22 to 44": "rgba(128, 0, 128, 1)",
    "45 to 64": "rgba(0, 255, 127, 1)",
    "65 and Over": "rgba(255, 69, 0, 1)"
  };

  // Fetch available columns on mount
  onMount(async () => {
    try {
      const response = await axios.get(`${baseUrl}/columns`); // Fetch column names
      columns = response.data.columns.filter(
        column => !["Year", "Voting Population", "Total Voter Turnout"].includes(column)
      );
    } catch (error) {
      console.error("Failed to fetch columns:", error);
    }
  });

  async function makePrediction() {
    errorMessage = null;
    responseMessage = null;
    responseData = null;

    try {
      const years = predictionYears.split(",").map(year => parseInt(year.trim()));
      const response = await axios.post(`${baseUrl}/predict`, {
        columns: selectedColumns,
        predict_years: years,
      });

      responseMessage = response.data.message;
      responseData = response.data;
      renderChart(response.data);
    } catch (error) {
      errorMessage = error.response?.data?.error || "An error occurred";
    }
  }

  function renderChart(data) {
    if (chart) chart.destroy();

    const ctx = document.getElementById("predictionChart").getContext("2d");
    const datasets = [];
    let allDataPoints = [];

    // Loop through selected columns and generate datasets
    selectedColumns.forEach(column => {
      const color = colorMap[column] || "rgba(0, 0, 0, 1)"; // Default to black if no color found

      // Plot actual data
      if (data.actual_data[column]) {
        const actualData = data.actual_data[column].years.map((year, index) => ({
          x: year,
          y: data.actual_data[column].values[index],
        }));
        allDataPoints = allDataPoints.concat(actualData.map(point => point.y));

        datasets.push({
          label: `Actual Data (${column})`,
          data: actualData,
          type: "scatter",
          backgroundColor: color,
          borderColor: color,
        });
      }

      // Plot predictions
      if (data.predictions[column]) {
        const predictionData = data.years.map((year, index) => ({
          x: year,
          y: data.predictions[column][index],
        }));
        allDataPoints = allDataPoints.concat(predictionData.map(point => point.y));

        datasets.push({
          label: `Predicted (${column})`,
          data: predictionData,
          type: "line",
          backgroundColor: `${color.replace("1)", "0.2)")}`, // Transparent background for line
          borderColor: color,
          fill: false,
          tension: 0.3,
        });
      }
    });

    const minY = Math.min(...allDataPoints);
    const yAxisStart = minY - (0.1 * minY);

    chart = new Chart(ctx, {
      type: "scatter",
      data: {
        datasets: datasets,
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: true,
            position: "top",
          },
        },
        scales: {
          x: {
            type: "linear",
            title: { display: true, text: "Year" },
          },
          y: {
            title: { display: true, text: "Turnout Rate (%)" },
            beginAtZero: false,
            min: yAxisStart,
          },
        },
      },
    });
  }

  function clearInputs() {
    selectedColumns = []; // Reset selected columns
    predictionYears = ""; // Clear prediction years
    responseMessage = null;
    responseData = null;
    errorMessage = null;

    if (chart) {
      chart.destroy(); // Clear the chart
      chart = null;
    }
  }
</script>

<div class="bg-gray-100 p-6 rounded-lg shadow-md max-w-xl mx-auto mt-10">
  <h1 class="text-3xl font-bold mb-6 text-center">Data Section</h1>

  <div class="mb-4">
    <label class="block text-lg font-semibold mb-2">Choose Parameters:</label>
    {#each columns as column}
      <label class="block">
        <input
          type="checkbox"
          value={column}
          bind:group={selectedColumns}
          class="mr-2"
        />
        {column}
      </label>
    {/each}
  </div>

  <div class="mb-4">
    <label class="block text-lg font-semibold mb-2">Enter Years (comma-separated):</label>
    <input
      type="text"
      bind:value={predictionYears}
      class="block w-full p-2 rounded-lg border border-gray-300 focus:outline-none focus:ring focus:ring-blue-300"
      placeholder="e.g., 2025,2030,2040"
    />
  </div>

  <div class="text-center space-x-4">
    <button
      on:click={makePrediction}
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow-md focus:outline-none focus:ring focus:ring-blue-300"
    >
      Submit
    </button>

    <button
      on:click={clearInputs}
      class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-6 rounded-lg shadow-md focus:outline-none focus:ring focus:ring-gray-300"
    >
      Clear
    </button>
  </div>

  <!-- Response Message -->
  {#if responseMessage}
    <p class="text-green-500 mt-4 font-semibold text-center">{responseMessage}</p>
  {/if}

  <!-- Error Message -->
  {#if errorMessage}
    <p class="text-red-500 mt-4 font-semibold text-center">{errorMessage}</p>
  {/if}
</div>

<canvas id="predictionChart"></canvas>

<style>
  canvas {
    max-width: 100%;
    height: auto;
  }
</style>

