
<script>
  export let columns = [];
  export let selectedColumns = [];
  export let predictionYears = "2025,2030,2040";
  export let makePrediction;
  export let clearInputs;
</script>

<div class="bg-gray-800 p-6 rounded-lg shadow-md">
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
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

    <div>
      <label class="block text-sm font-semibold text-gray-300 mb-2">Enter Years:</label>
      <input
        type="text"
        bind:value={predictionYears}
        class="w-full p-3 rounded-lg bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring focus:ring-blue-500"
        placeholder="e.g., 2025,2030,2040"
      />
    </div>
  </div>

  <div class="flex justify-center mt-6 space-x-4">
    <button on:click={makePrediction} class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-6 rounded-lg">
      Submit
    </button>
    <button on:click={clearInputs} class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-6 rounded-lg">
      Clear
    </button>
  </div>
</div>

