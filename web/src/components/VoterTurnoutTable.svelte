

<script>
  import axios from "axios";
  import { onMount } from "svelte";
  
  const baseUrl = import.meta.env.VITE_API_BASE_URL;
  let data = [];
  let cleanedData = [];
  let loading = true;
  let error = null;
  let sortColumn = null;
  let sortOrder = "asc";

  // Custom column order
  const columnOrder = [
    "Year", "Voting Population", "Total Voter Turnout", "White", "Black",
    "Asian", "Hispanic", "Male", "Female", "18 to 24", "22 to 44", "45 to 64", "65 and Over"
  ];

  // Formatter for numbers with commas
  const numberFormatter = new Intl.NumberFormat('en-US');

  // Fetch raw data on mount
  onMount(async () => {
    try {
      const response = await axios.get(`${baseUrl}/data`);
      data = response.data;
      console.log(data)
      loading = false;
    } catch (err) {
      error = "Failed to fetch data";
      loading = false;
      console.error("Error fetching data:", err);
    }
  });

  // Sorting function that directly reassigns the data array for Svelte reactivity
  function sortData(column) {
    if (sortColumn === column) {
      sortOrder = sortOrder === "asc" ? "desc" : "asc";
    } else {
      sortColumn = column;
      sortOrder = "asc";
    }

    let dataToSort = cleanedData.length > 0 ? [...cleanedData] : [...data];

    dataToSort = dataToSort.sort((a, b) => {
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

    if (cleanedData.length > 0) {
      cleanedData = dataToSort; // Update cleanedData array to trigger reactivity
    } else {
      data = dataToSort; // Update data array to trigger reactivity
    }
  }
</script>

<h1 class="text-3xl font-bold text-center text-white mb-8">Voter Turnout Data</h1>

<div class="bg-gray-800 p-4 rounded-lg shadow-md">
  <div class="overflow-x-auto">
    {#if loading}
      <p class="text-center text-gray-400">Loading...</p>
    {:else if error}
      <p class="text-center text-red-500">{error}</p>
    {:else if (data.length > 0 || cleanedData.length > 0)}
      <table class="min-w-full bg-gray-900 shadow-lg rounded-lg">
        <thead>
          <tr>
            {#each columnOrder as key}
              <th
                class="table-header py-3 px-4 text-left text-sm font-medium text-gray-300 hover:bg-gray-700 cursor-pointer"
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
          {#each (cleanedData.length > 0 ? cleanedData : data) as row}
            <tr class="hover:bg-gray-700">
              {#each columnOrder as key}
                <td class="py-3 px-4 border-b border-gray-700 text-sm text-gray-400">
                  {#if key === "Voting Population"}
                    {row[key] !== null && row[key] !== undefined ? numberFormatter.format(row[key]) : "N/A"}
                  {:else}
                    {row[key] === null || row[key] === undefined || Number.isNaN(row[key]) ? "N/A" : row[key]}
                  {/if}
                </td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    {:else}
      <p class="text-center text-gray-400">No data available</p>
    {/if}
  </div>
</div>

<style>
  .table-header {
    background-color: #4b5563; /* Dark Gray */
    color: #d1d5db; /* Light Gray Text */
    font-weight: bold;
    transition: background-color 0.3s ease;
  }
  .table-header:hover {
    background-color: #374151; /* Slightly lighter gray on hover */
  }
</style>
