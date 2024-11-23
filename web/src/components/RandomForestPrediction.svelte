
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
      renderChart(response.data);
    } catch (error) {
      errorMessage = error.response?.data?.error || "An error occurred";
    }
  }

let chartType = "bar"; // Default chart type is bar

function renderChart(data) {
  // Destroy the existing chart if it exists
  if (chart) chart.destroy();

  // Dynamically get the correct canvas based on chart type
  const ctx =
    chartType === "doughnut"
      ? document.querySelector("#doughnutChart").getContext("2d")
      : document.querySelector("#barChart").getContext("2d");

  if (chartType === "bar") {
    // Stacked Bar Chart Logic
    const datasets = [];
    let allDataPoints = [];

    selectedColumns.forEach((column) => {
      const color = colorMap[column] || "rgba(0, 0, 0, 1)";
      const columnData = data.years.map((year, index) => ({
        x: year,
        y: data.predictions[column]?.[index] || data.actual_data[column]?.values?.[index] || 0,
      }));
      allDataPoints = allDataPoints.concat(columnData.map((point) => point.y));

      datasets.push({
        label: column,
        data: columnData,
        backgroundColor: `${color.replace("1)", "0.6)")}`,
        borderColor: color,
        borderWidth: 1,
      });
    });

    const minY = Math.min(...allDataPoints);
    const yAxisStart = minY - 0.1 * minY;

    chart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: data.years,
        datasets: datasets,
      },
      options: {
        responsive: true,
        scales: {
          x: {
            title: { display: true, text: "Year" },
            stacked: true,
          },
          y: {
            title: { display: true, text: "Turnout Rate (%)" },
            stacked: true,
            beginAtZero: true,
            min: yAxisStart,
          },
        },
        plugins: {
          legend: {
            display: true,
            position: "top",
          },
          tooltip: {
            callbacks: {
              label: (tooltipItem) =>
                `Year: ${tooltipItem.raw.x}, Value: ${tooltipItem.raw.y.toFixed(2)}%`,
            },
          },
        },
      },
    });
  } else if (chartType === "doughnut") {
    // Doughnut Chart Logic
    const aggregatedTotals = selectedColumns.map((column) => {
      return data.years.reduce((sum, _, yearIndex) => {
        const actualValue = data.actual_data[column]?.values?.[yearIndex] || 0;
        const predictedValue = data.predictions[column]?.[yearIndex] || 0;
        return sum + (predictedValue || actualValue);
      }, 0);
    });

    const totalSum = aggregatedTotals.reduce((a, b) => a + b, 0);

    if (totalSum === 0) {
      console.error("Total Sum of data is zero. Cannot render doughnut chart.");
      return;
    }

    chart = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: selectedColumns,
        datasets: [
          {
            label: "Turnout Proportions",
            data: aggregatedTotals,
            backgroundColor: selectedColumns.map(
              (column) => colorMap[column] || "rgba(0, 0, 0, 1)"
            ),
            hoverBackgroundColor: selectedColumns.map(
              (column) =>
                (colorMap[column] || "rgba(0, 0, 0, 1)").replace("1)", "0.8)")
            ),
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: true,
        aspectRatio: 1,
        cutout: "70%", // Inner hole size for doughnut chart
        plugins: {
          legend: {
            display: true,
            position: "top",
          },
          tooltip: {
            callbacks: {
              label: (tooltipItem) => {
                const value = tooltipItem.raw;
                const percentage = ((value / totalSum) * 100).toFixed(2);
                return `${tooltipItem.label}: ${value} (${percentage}%)`;
              },
            },
          },
        },
      },
    });
  }
}

  function clearInputs() {
    selectedColumns = [];
    predictionYears = "";
    responseMessage = null;
    responseData = null;
    errorMessage = null;

    if (chart) {
      chart.destroy();
      chart = null;
    }
  }
</script>

<div class="bg-gray-100 p-6 rounded-lg shadow-md max-w-xl mx-auto mt-10">
  <h1 class="text-3xl font-bold mb-6 text-center">Random Forest Prediction</h1>
  <div class="mb-4">
  <label class="block text-lg font-semibold mb-2">Select Chart Type:</label>
  <select bind:value={chartType} class="block w-full p-2 rounded-lg border border-gray-300">
    <option value="bar">Stacked Bar Chart</option>
    <option value="doughnut">Doughnut Chart</option>
  </select>
</div>
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

<!-- Doughnut Chart -->
<canvas id="doughnutChart" class="chart-doughnut"></canvas>

<!-- Bar Chart -->
<canvas id="barChart" class="chart-bar"></canvas>

<style>
 canvas.chart-doughnut {
  max-width: 70%;
  max-height: 100%;
  margin:  auto;
}

canvas.chart-bar {
  max-width: 100%; /* Default size for bar chart */
  height: auto;
}
</style>

