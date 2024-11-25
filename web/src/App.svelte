<!-- src/App.svelte -->
<script>
  import RandomForestPrediction from "./components/RandomForestPrediction.svelte";
  import LinearPrediction from "./components/LinearPrediction.svelte";
  let activeMenu = "dashboard"; // Tracks the active menu item
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
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3L3 12h7l-4 9 12-15h-8z" />
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
    <h1 class="text-4xl font-bold mb-8">Fox Team</h1>

    <!-- Row for Random Forest Predictions -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Left Column: 2/3 -->
      <div class="lg:col-span-2 bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-semibold mb-4">Box Plot</h2>
        <RandomForestPrediction />
      </div>

      <!-- Right Column: 1/3 -->
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
        <h2 class="text-xl font-semibold mb-4">Pie Chart</h2>
        <RandomForestPrediction />
      </div>
    </div>
  </main>
</div>

