
<script>
  import axios from "axios";

  let responseMessage = null; // Holds the success message
  let responseData = null; // Holds the current API response
  let isLoading = false; // Tracks if any API call is in progress
  let errorMessage = null; // Holds any error message from the backend

  const baseUrl = import.meta.env.VITE_API_BASE_URL; // Base URL from the environment

  // Function to trigger training
  async function trainLinearRegression() {
    isLoading = true;
    responseMessage = null;
    responseData = null;
    errorMessage = null;

    try {
      const response = await axios.post(`${baseUrl}/train-linear-regression`);
      responseMessage = "Linear Regression model trained successfully!";
      responseData = response.data;
    } catch (error) {
      errorMessage = error.response?.data?.error || "An error occurred during training.";
    } finally {
      isLoading = false;
    }
  }

  // Function to trigger hyperparameter tuning
  async function hyperTuneLinearRegression() {
    isLoading = true;
    responseMessage = null;
    responseData = null;
    errorMessage = null;

    try {
      const response = await axios.post(`${baseUrl}/hyperparameter-tuning-linear`);
      responseMessage = "Hyperparameter tuning completed successfully!";
      responseData = response.data;
    } catch (error) {
      errorMessage = error.response?.data?.error || "An error occurred during hyperparameter tuning.";
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="bg-gray-800 p-6 rounded-lg shadow-md w-full">
  <h1 class="text-3xl font-bold text-center text-white mb-6">Linear Regression Model</h1>

  <!-- Buttons Section -->
  <div class="bg-gray-700 p-6 rounded-lg mb-6">
    <div class="flex justify-center gap-4">
      <!-- Train Model Button -->
      <button
        on:click={trainLinearRegression}
        class="px-6 py-2 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 focus:ring focus:ring-blue-300"
        disabled={isLoading}
      >
        {isLoading ? "Loading..." : "Train Model"}
      </button>

      <!-- Hyperparameter Tuning Button -->
      <button
        on:click={hyperTuneLinearRegression}
        class="px-6 py-2 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 focus:ring focus:ring-green-300"
        disabled={isLoading}
      >
        {isLoading ? "Loading..." : "Hyper Tune Model"}
      </button>
    </div>
  </div>

  <!-- Success Message -->
  {#if responseMessage}
    <p class="text-green-500 text-center font-semibold mt-4">{responseMessage}</p>
  {/if}

  <!-- Error Message -->
  {#if errorMessage}
    <p class="text-red-500 text-center font-semibold mt-4">{errorMessage}</p>
  {/if}

  <!-- Results Section -->
  {#if responseData}
    <div class="bg-gray-900 p-6 rounded-lg shadow-lg">
      <h2 class="text-xl font-semibold text-white mb-4">Results</h2>

      <!-- Metrics -->
      {#if responseData.metrics}
        <h3 class="text-lg font-medium text-gray-300 mb-2">Evaluation Metrics:</h3>
        <ul class="list-disc list-inside text-gray-400">
          <li>Mean Absolute Error (MAE): {responseData.metrics.mae}</li>
          <li>Mean Squared Error (MSE): {responseData.metrics.mse}</li>
          <li>Root Mean Squared Error (RMSE): {responseData.metrics.rmse}</li>
          <li>R² Score: {responseData.metrics.r2}</li>
        </ul>
      {/if}

      <!-- Best Parameters -->
      {#if responseData.best_params}
        <h3 class="text-lg font-medium text-gray-300 mt-6 mb-2">Best Parameters:</h3>
        <ul class="list-disc list-inside text-gray-400">
          {#each Object.entries(responseData.best_params) as [key, value]}
            <li>{key}: {value}</li>
          {/each}
        </ul>
      {/if}
    </div>
  {/if}
</div>

<style>
  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
</style>

