
<script>
  import axios from "axios";

  const baseUrl = import.meta.env.VITE_API_BASE_URL;

  let isLoading = false; // Tracks the loading state
  let isHyperTuningDisabled = true; // Disables the Hyperparameter Tuning button
  let message = "Render's free tier does not offer enough memory for this.";
  let responseMessage = null;
  let responseData = null;
  let errorMessage = null;

  // Function to train the model
  async function trainModel() {
    isLoading = true;
    responseMessage = null;
    responseData = null;
    errorMessage = null;

    try {
      const response = await axios.post(`${baseUrl}/train-randomforest`);
      responseMessage = "Model trained successfully!";
      responseData = response.data;
    } catch (error) {
      errorMessage = error.response?.data?.error || "An error occurred during training.";
    } finally {
      isLoading = false;
    }
  }

  // Function to trigger hyperparameter tuning
  async function hyperTuneModel() {
    isLoading = true;
    responseMessage = null;
    responseData = null;
    errorMessage = null;

    try {
      const response = await axios.post(`${baseUrl}/hyperparameter-tuning-randomforest`);
      responseMessage = "Hyperparameter tuning completed successfully!";
      responseData = response.data;
    } catch (error) {
      errorMessage = error.response?.data?.error || "An error occurred during hyperparameter tuning.";
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="bg-gray-800 p-8 rounded-lg shadow-md w-full">
  <h1 class="text-3xl font-bold text-center text-white mb-8">Random Forest Model</h1>

  <!-- Button Section -->
  <div class="bg-gray-700 p-6 rounded-lg mb-8">
    <div class="flex flex-col items-center gap-4">
      <!-- Buttons Row -->
      <div class="flex justify-center gap-6">
        <!-- Train Model Button -->
        <button
          on:click={trainModel}
          class="px-6 py-3 bg-blue-500 text-white font-semibold rounded-lg hover:bg-blue-600 focus:ring focus:ring-blue-300 transition"
          disabled={isLoading}
        >
          {isLoading ? "Loading..." : "Train Model"}
        </button>

        <!-- Hyperparameter Tuning Button -->
        <button
          on:click={hyperTuneModel}
          class="px-6 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 focus:ring focus:ring-green-300 transition disabled:opacity-50 disabled:cursor-not-allowed"
          disabled={isLoading || isHyperTuningDisabled}
        >
          {isLoading ? "Loading..." : "Hyper Tune Model"}
        </button>
      </div>

      <!-- Message Section -->
      {#if isHyperTuningDisabled}
        <p class="text-red-500 text-sm text-center mt-4 bg-red-100 px-4 py-2 rounded-lg">
          {message}
        </p>
      {/if}
    </div>
  </div>

  <!-- Feedback Messages -->
  {#if responseMessage}
    <p class="text-green-500 text-center font-semibold mb-4">{responseMessage}</p>
  {/if}

  {#if errorMessage}
    <p class="text-red-500 text-center font-semibold mb-4">{errorMessage}</p>
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

