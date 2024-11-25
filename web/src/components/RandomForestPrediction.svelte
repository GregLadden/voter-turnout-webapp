
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
  let chartBar, chartDoughnut;

  const baseUrl = import.meta.env.VITE_API_BASE_URL;

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
      const response = await axios.post(`${baseUrl}/predict-randomforest`, {
        columns: selectedColumns,
        predict_years: years,
      });

      responseMessage = response.data.message;
      responseData = response.data;
      renderCharts(response.data);
    } catch (error) {
      errorMessage = error.response?.data?.error || "An error occurred";
      console.error("Prediction error:", errorMessage);
    }
  }

  function renderCharts(data) {
    if (chartBar) chartBar.destroy();
    if (chartDoughnut) chartDoughnut.destroy();

    const barCtx = document.querySelector("#barChart").getContext("2d");
    const doughnutCtx = document.querySelector("#doughnutChart").getContext("2d");

    const barDatasets = selectedColumns.map(column => ({
      label: column,
      data: data.years.map((_, index) => data.predictions[column]?.[index] || 0),
      backgroundColor: `${colorMap[column]?.replace("1)", "0.6)")}`,
      borderColor: colorMap[column],
      borderWidth: 1
    }));

    chartBar = new Chart(barCtx, {
      type: "bar",
      data: {
        labels: data.years,
        datasets: barDatasets
      },
      options: {
        responsive: true,
        scales: {
          x: { title: { display: true, text: "Year" } },
          y: { title: { display: true, text: "Turnout Rate (%)" }, beginAtZero: true }
        },
        plugins: {
          legend: { display: true, position: "top" }
        }
      }
    });

    const doughnutData = selectedColumns.map(column => 
      data.years.reduce((sum, _, index) => sum + (data.predictions[column]?.[index] || 0), 0)
    );

    chartDoughnut = new Chart(doughnutCtx, {
      type: "doughnut",
      data: {
        labels: selectedColumns,
        datasets: [
          {
            data: doughnutData,
            backgroundColor: selectedColumns.map(column => colorMap[column]),
            hoverBackgroundColor: selectedColumns.map(column => colorMap[column]?.replace("1)", "0.8)"))
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: true, position: "top" }
        }
      }
    });
  }

  function clearInputs() {
    selectedColumns = [];
    predictionYears = "2025,2030,2040";
    responseMessage = null;
    responseData = null;
    errorMessage = null;

    if (chartBar) chartBar.destroy();
    if (chartDoughnut) chartDoughnut.destroy();
  }
</script>

<div class="bg-gray-800 p-4 rounded-lg shadow-md w-full">
  <div class="mb-6">
    <h1 class="text-3xl font-bold text-center text-white mb-6">
      Random Forest Prediction
    </h1>
    <!-- Form Section -->
    <div class="bg-gray-700 p-6 rounded-lg mb-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
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
          <label class="block text-sm font-semibold text-gray-300 mb-2">Enter Years (comma-separated):</label>
          <input
            type="text"
            bind:value={predictionYears}
            class="w-full p-3 rounded-lg bg-gray-600 border border-gray-500 text-white focus:outline-none focus:ring focus:ring-blue-500"
            placeholder="e.g., 2025,2030,2040"
          />
        </div>
        <!-- Submit and Clear Buttons -->
        <div class="flex justify-end gap-4">
          <button
            on:click={makePrediction}
            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:ring focus:ring-blue-500"
          >
            Submit
          </button>
          <button
            on:click={clearInputs}
            class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-6 rounded-lg focus:outline-none focus:ring focus:ring-gray-400"
          >
            Clear
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Chart Section -->
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <!-- Box Plot: Occupies 3/4 of the width -->
    <div class="lg:col-span-2 bg-gray-900 p-6 rounded-lg shadow-lg">
      <h2 class="text-xl font-semibold text-white mb-4">Box Plot</h2>
      <canvas id="barChart" class="chart-bar"></canvas>
    </div>
    <!-- Doughnut Chart: Occupies 1/4 of the width -->
    <div class="lg:col-span-1 bg-gray-900 p-6 rounded-lg shadow-lg">
      <h2 class="text-xl font-semibold text-white mb-4">Doughnut Chart</h2>
      <canvas id="doughnutChart" class="chart-doughnut"></canvas>
    </div>
  </div>
</div>

<style>
  .chart-bar {
    max-width: 100%;
    height: auto;
  }

  .chart-doughnut {
    max-width: 100%;
    height: auto;
  }
</style>

