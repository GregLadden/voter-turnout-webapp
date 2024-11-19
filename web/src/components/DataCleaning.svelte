
<script>
  import axios from "axios";

  const baseUrl = import.meta.env.VITE_API_BASE_URL;
  let handleMissing = true;
  let removeOutliers = true;
  let normalize = true;
  let convertNumeric = true;
  let cleanedData = [];
  let loading = false;
  let error = null;
  let sortColumn = null;
  let sortOrder = "asc";

  const columnOrder = [
    "Year", "Voting Population", "Total Voter Turnout", "White", "Black",
    "Asian", "Hispanic", "Male", "Female", "18 to 24", "22 to 44", "45 to 64", "65 and Over"
  ];

  const numberFormatter = new Intl.NumberFormat('en-US');

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

      const response = await axios.get(`${baseUrl}/clean-data?${queryParams}`);
      cleanedData = response.data.map(row =>
        Object.fromEntries(
          Object.entries(row).map(([key, value]) => [
            key.trim(),  // Trim spaces from keys for consistent column naming
            typeof value === 'number' ? parseFloat(value.toFixed(2)) : value
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

  function sortData(column) {
    if (sortColumn === column) {
      sortOrder = sortOrder === "asc" ? "desc" : "asc";
    } else {
      sortColumn = column;
      sortOrder = "asc";
    }

    cleanedData = [...cleanedData].sort((a, b) => {
      let valA = a[column];
      let valB = b[column];

      // Handle null or undefined values by placing them at the end
      if (valA === null || valA === undefined) return 1;
      if (valB === null || valB === undefined) return -1;

      if (sortOrder === "asc") {
        return valA > valB ? 1 : valA < valB ? -1 : 0;
      } else {
        return valA < valB ? 1 : valA > valB ? -1 : 0;
      }
    });
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
  .table-header {
    background-color: #3b82f6;
    color: white;
    font-weight: bold;
    cursor: pointer;
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
        {#each columnOrder as key}
          <th
            class="table-header py-3 px-4 text-left text-sm font-medium"
            on:click={() => sortData(key)}
          >
            {key.trim()}
            {#if sortColumn === key}
              {sortOrder === "asc" ? " ↑" : " ↓"}
            {/if}
          </th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#each cleanedData as row}
        <tr class="hover:bg-gray-100">
          {#each columnOrder as key}
            <td class="py-3 px-4 border-b text-sm text-gray-700">
              {#if key === "Voting Population"}
                {row[key] !== null && row[key] !== undefined ? numberFormatter.format(row[key]) : "N/A"}
              {:else}
                {row[key] === null || row[key] === undefined ? "N/A" : row[key]}
              {/if}
            </td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
{/if}

