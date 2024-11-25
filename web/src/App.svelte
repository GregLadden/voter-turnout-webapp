
<script>
  import RandomForestPrediction from "./components/RandomForestPrediction.svelte";
  import LinearPrediction from "./components/LinearPrediction.svelte";
  import VoterTurnoutTable from "./components/VoterTurnoutTable.svelte";
    import RandomForestModel from "./components/RandomForestModel.svelte";
    import LinearRegressionModel from "./components/LinearRegressionModel.svelte";

  let activeMenu = "dashboard";

</script>

<style>
  .smooth-hover {
    transition: all 0.3s ease;
  }
</style>

<div class="bg-gray-900 min-h-screen flex">
  <!-- Sidebar -->
  <aside class="bg-gray-800 w-20 lg:w-64 flex flex-col justify-between p-4 lg:p-6">
    <nav class="space-y-4">
      <!-- Dashboard Icon -->
      <a 
        href="#"
        class={`p-4 lg:py-3 lg:px-6 rounded-md flex justify-center lg:justify-start lg:items-center space-x-0 lg:space-x-2 text-white/50 ${
          activeMenu === "dashboard" ? "bg-gray-700 text-white" : "hover:bg-gray-700 hover:text-white smooth-hover"
        }`}
        on:click={() => (activeMenu = "dashboard")}
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 lg:h-5 lg:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
        </svg>
        <span class="hidden lg:block text-sm font-medium">Dashboard</span>
      </a>
      <!-- Data Icon -->
      <a 
        href="#"
        class={`p-4 lg:py-3 lg:px-6 rounded-md flex justify-center lg:justify-start lg:items-center space-x-0 lg:space-x-2 text-white/50 ${
          activeMenu === "data" ? "bg-gray-700 text-white" : "hover:bg-gray-700 hover:text-white smooth-hover"
        }`}
        on:click={() => (activeMenu = "data")}
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 lg:h-5 lg:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3L5 9h4l-4 6h4l-4 6h4l6-18H9z" />
        </svg>
        <span class="hidden lg:block text-sm font-medium">Data</span>
      </a>
      <!-- Model Training Icon -->
      <a 
        href="#"
        class={`p-4 lg:py-3 lg:px-6 rounded-md flex justify-center lg:justify-start lg:items-center space-x-0 lg:space-x-2 text-white/50 ${
          activeMenu === "model" ? "bg-gray-700 text-white" : "hover:bg-gray-700 hover:text-white smooth-hover"
        }`}
        on:click={() => (activeMenu = "model")}
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 lg:h-5 lg:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <span class="hidden lg:block text-sm font-medium">Model Training</span>
      </a>
    </nav>
  </aside>

  <!-- Main Content -->
  <main class="flex-1 bg-gray-900 p-6 lg:p-10 text-white">
    {#if activeMenu === "dashboard"}
      <!-- Inject RandomForestPrediction -->
      <RandomForestPrediction />
      <LinearPrediction />
    {/if}
    {#if activeMenu === "data"}
      <h1 class="text-2xl font-bold mb-6">Data</h1>
      <VoterTurnoutTable /> 
    {/if}
    {#if activeMenu === "model"}
      <h1 class="text-3xl font-bold text-white mb-6 text-center">Model Training</h1>
      <div class=" p-6 rounded-lg shadow-md">
        <div class="flex flex-col lg:flex-row gap-6">
          <!-- Random Forest Model Section -->
          <div class="flex-1 bg-gray-700 p-6 rounded-lg shadow-md">
            <RandomForestModel />
          </div>

          <!-- Linear Regression Model Section -->
          <div class="flex-1 bg-gray-700 p-6 rounded-lg shadow-md">
            <LinearRegressionModel />
          </div>
        </div>
      </div>
    {/if}
  </main>
</div>


