
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
      responseData = response.data; // Store the response data
    } catch (error) {
      if (error.response) {
        errorMessage = error.response.data.error || "An error occurred during training.";
      } else {
        errorMessage = "Failed to connect to the server. Please try again.";
      }
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
      responseData = response.data; // Store the response data
    } catch (error) {
      if (error.response) {
        errorMessage = error.response.data.error || "An error occurred during hyperparameter tuning.";
      } else {
        errorMessage = "Failed to connect to the server. Please try again.";
      }
    } finally {
      isLoading = false;
    }
  }
</script>

<!-- UI for buttons and messages -->
<div class="train-container">
  <h1 class="text-2xl font-bold mb-4">Linear Regression</h1>

  <!-- Buttons for training and tuning -->
  <button
    on:click={trainLinearRegression}
    class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-700"
    disabled={isLoading}
  >
    {isLoading ? "Loading..." : "Train Model"}
  </button>

  <button
    on:click={hyperTuneLinearRegression}
    class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-700 ml-4"
    disabled={isLoading}
  >
    {isLoading ? "Loading..." : "Hyper Tune Model"}
  </button>

  <!-- Success message -->
  {#if responseMessage}
    <p class="text-green-500 mt-4 font-semibold">{responseMessage}</p>
  {/if}

  <!-- Error message -->
  {#if errorMessage}
    <p class="text-red-500 mt-4">{errorMessage}</p>
  {/if}

  <!-- Response box -->
  {#if responseData}
    <div class="mt-4 p-4 bg-gray-100 rounded shadow-md">
      <h2 class="text-xl font-semibold">Results:</h2>

      <!-- Conditional rendering for metrics -->
      {#if responseData.metrics}
        <h3 class="text-lg font-medium mt-4">Evaluation Metrics:</h3>
        <ul class="list-disc list-inside mt-2">
          <li>Mean Absolute Error (MAE): {responseData.metrics.mae}</li>
          <li>Mean Squared Error (MSE): {responseData.metrics.mse}</li>
          <li>Root Mean Squared Error (RMSE): {responseData.metrics.rmse}</li>
          <li>R² Score: {responseData.metrics.r2}</li>
        </ul>
      {/if}

      <!-- Conditional rendering for best parameters -->
      {#if responseData.best_params}
        <h3 class="text-lg font-medium mt-4">Best Parameters:</h3>
        <ul class="list-disc list-inside mt-2">
          {#each Object.entries(responseData.best_params) as [key, value]}
            <li>{key}: {value}</li>
          {/each}
        </ul>
      {/if}
    </div>
  {/if}
</div>

<style>
  .train-container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
