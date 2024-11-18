

<script>
  import axios from "axios";

  let handleMissing = true;
  let removeOutliers = true;
  let normalize = true;
  let convertNumeric = true;
  let cleanedData = [];
  let loading = false;
  let error = null;

  async function submitForm() {
    loading = true;
    error = null;

    try {
      const queryParams = new URLSearchParams({
        handle_missing: handleMissing.toString(),
        remove_outliers: removeOutliers.toString(),
        normalize: normalize.toString(),
        convert_numeric: convertNumeric.toString()
      });

      const response = await axios.get(`http://127.0.0.1:5000/clean-data?${queryParams}`);
      cleanedData = response.data.map(row =>
        Object.fromEntries(
          Object.entries(row).map(([key, value]) => [
            key,
            typeof value === 'number' ? parseFloat(value.toFixed(2)) : value // Round numeric values to 2 decimal places
          ])
        )
      );
    } catch (err) {
      error = "Failed to clean data. Please try again.";
      console.error("Error cleaning data:", err);
    } finally {
      loading = false;
    }
  }
</script>

<style>
  .form-container { 
    max-width: 600px; 
    margin: auto; 
    padding: 20px; 
    background-color: #f3f4f6; 
    border-radius: 8px; 
  }
</style>

<div class="form-container">
  <h2 class="text-2xl font-semibold mb-4">Data Cleaning Options</h2>

  <form on:submit|preventDefault={submitForm}>
    <div class="mb-4">
      <label><input type="checkbox" bind:checked={handleMissing} /> Handle Missing Values</label>
    </div>
    <div class="mb-4">
      <label><input type="checkbox" bind:checked={removeOutliers} /> Remove Outliers</label>
    </div>
    <div class="mb-4">
      <label><input type="checkbox" bind:checked={normalize} /> Normalize Data</label>
    </div>
    <div class="mb-4">
      <label><input type="checkbox" bind:checked={convertNumeric} /> Convert to Numeric</label>
    </div>

    <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded">Clean Data</button>
  </form>
</div>

<!-- Display Cleaned Data Below the Form Container -->
{#if loading}
  <p class="text-center text-gray-500 mt-4">Cleaning data...</p>
{:else if error}
  <p class="text-center text-red-500 mt-4">{error}</p>
{:else if cleanedData.length > 0}
  <p class="text-center text-green-500 mt-4">Data cleaned successfully! Displaying below:</p>

  <!-- Table for displaying cleaned data -->
  <table class="min-w-full bg-white shadow-md rounded-lg overflow-hidden mt-4">
    <thead>
      <tr>
        {#each Object.keys(cleanedData[0] || {}) as key}
          <th class="py-3 px-4 text-left text-sm font-medium">{key.trim()}</th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each cleanedData as row}
        <tr class="hover:bg-gray-100">
          {#each Object.values(row) as value}
            <td class="py-3 px-4 border-b text-sm text-gray-700">
              {value === null || value === undefined || Number.isNaN(value) ? "N/A" : value}
            </td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
{/if}

