
<script>
  import RandomForestForm from "./RF-Form.svelte";
  import RandomForestCharts from "./RF-Charts.svelte";
  import { onMount } from "svelte";
  import axios from "axios";

  let columns = []; // List of available columns
  let selectedColumns = []; // User-selected columns
  let predictionYears = "2025,2030,2040"; // Default years
  let chartData = null; // Chart data for predictions
  let isLoading = false;
  let errorMessage = null;

  const baseUrl = import.meta.env.VITE_API_BASE_URL;

  // Fetch available columns on mount
  onMount(async () => {
    try {
      const response = await axios.get(`${baseUrl}/columns`);
      columns = response.data.columns.filter(
        (column) => !["Year", "Voting Population", "Total Voter Turnout"].includes(column)
      );
    } catch (error) {
      console.error("Failed to fetch columns:", error);
      errorMessage = "Unable to load parameters. Try again later.";
    }
  });

  async function makePrediction() {
    isLoading = true;
    errorMessage = null;

    try {
      const years = predictionYears.split(",").map((year) => parseInt(year.trim()));
      const response = await axios.post(`${baseUrl}/predict-randomforest`, {
        columns: selectedColumns,
        predict_years: years,
      });

      chartData = {
        years: response.data.years,
        predictions: response.data.predictions,
      };
    } catch (error) {
      console.error("Prediction error:", error);
      errorMessage = "Failed to generate predictions. Please try again.";
    } finally {
      isLoading = false;
    }
  }

  function clearInputs() {
    selectedColumns = [];
    predictionYears = "2025,2030,2040";
    chartData = null;
  }
</script>

<div>
  <div class="mb-8">
    <RandomForestForm
      {columns}
      {selectedColumns}
      {predictionYears}
      makePrediction={makePrediction}
      clearInputs={clearInputs}
    />
  </div>

  {#if errorMessage}
    <p class="text-red-500 text-center font-bold">{errorMessage}</p>
  {/if}

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <div class="lg:col-span-2 bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 class="text-xl font-semibold text-white mb-4">Bar Chart</h2>
      <RandomForestCharts chartType="bar" chartData={chartData} uniqueId="barChart" />
    </div>

    <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 class="text-xl font-semibold text-white mb-4">Doughnut Chart</h2>
      <RandomForestCharts chartType="doughnut" chartData={chartData} uniqueId="doughnutChart" />
    </div>
  </div>
</div>

