
<script>
  import axios from "axios";
  import { onMount } from "svelte";
  import { Chart, registerables } from "chart.js";
  Chart.register(...registerables);

  let columns = []; // List of available columns
  let selectedColumns = []; // User-selected columns
  let predictionYears = "2025,2030,2040"; // Default prediction years
  let responseMessage = null;
  let responseData = null;
  let errorMessage = null;
  let chart;

  const baseUrl = import.meta.env.VITE_API_BASE_URL;

  // Updated color map to match Random Forest
  const colorMap = {
    "White": "rgba(75, 192, 192, 1)", // Teal
    "Black": "rgba(54, 162, 235, 1)", // Blue
    "Asian": "rgba(255, 99, 132, 1)", // Red
    "Hispanic": "rgba(255, 206, 86, 1)", // Yellow
    "Male": "rgba(153, 102, 255, 1)", // Purple
    "Female": "rgba(255, 159, 64, 1)", // Orange
    "18 to 24": "rgba(0, 128, 128, 1)", // Teal Green
    "22 to 44": "rgba(128, 0, 128, 1)", // Violet
    "45 to 64": "rgba(0, 255, 127, 1)", // Mint Green
    "65 and Over": "rgba(255, 69, 0, 1)" // Deep Red
  };

  // Fetch columns on mount
  onMount(async () => {
    try {
      const response = await axios.get(`${baseUrl}/columns`);
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
      const response = await axios.post(`${baseUrl}/predict-linear-regression`, {
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

    const ctx = document.getElementById("linearChart").getContext("2d");
    const datasets = [];
    let allDataPoints = [];

    // Generate datasets for actual and predicted data
    selectedColumns.forEach(column => {
      const color = colorMap[column] || "rgba(0, 0, 0, 1)";

      // Actual data
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

      // Predicted data
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
          backgroundColor: `${color.replace("1)", "0.2)")}`,
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
      data: { datasets },
      options: {
        responsive: true,
        plugins: {
          legend: { display: true, position: "top" },
        },
        scales: {
          x: { type: "linear", title: { display: true, text: "Year" } },
          y: { title: { display: true, text: "Turnout Rate (%)" }, beginAtZero: false, min: yAxisStart },
        },
      },
    });
  }

  function clearInputs() {
    selectedColumns = [];
    predictionYears = "2025,2030,2040";
    responseMessage = null;
    responseData = null;
    errorMessage = null;

    if (chart) {
      chart.destroy();
      chart = null;
    }
  }
</script>

<div class="bg-gray-800 p-6 rounded-lg shadow-md w-full">
  <h1 class="text-2xl font-bold text-white mb-6 text-center">Linear Regression Prediction</h1>

  <!-- Form Section -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
    <!-- Select Parameters -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">Choose Parameters:</label>
      <div class="flex flex-wrap gap-2">
        {#each columns as column}
          <label class="flex items-center text-gray-300">
            <input
              type="checkbox"
              value={column}
              bind:group={selectedColumns}
              class="h-4 w-4 rounded border-gray-600 text-blue-500 focus:ring-blue-500 mr-2"
            />
            <span class="text-sm">{column}</span>
          </label>
        {/each}
      </div>
    </div>

    <!-- Enter Years -->
    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">Enter Years:</label>
      <input
        type="text"
        bind:value={predictionYears}
        class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white"
        placeholder="e.g., 2025,2030,2040"
      />
    </div>

    <!-- Buttons -->
    <div class="flex justify-end gap-4 items-end">
      <button
        on:click={makePrediction}
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Submit
      </button>
      <button
        on:click={clearInputs}
        class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
      >
        Clear
      </button>
    </div>
  </div>

  <!-- Chart Section -->
  <div class="rounded-lg bg-gray-900 p-6 shadow-lg">
    <h2 class="text-xl font-semibold text-white mb-4">Prediction Chart</h2>
    <canvas id="linearChart" class="rounded-lg"></canvas>
  </div>
</div>

<style>
  canvas {
    max-width: 100%;
    height: auto;
  }
</style>

