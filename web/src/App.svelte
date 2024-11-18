<!-- src/App.svelte -->


<script>
  import { onMount } from "svelte";
  import axios from "axios";
  import VoterTurnoutTable from "./components/VoterTurnoutTable.svelte";
  import DataCleaning from './components/DataCleaning.svelte';

  let data = []; // Raw data
  let activeMenu = "data"; // Main menu selection
  let activeTab = "raw"; // Tab selection within the Data section

  // Fetch raw data on mount
  onMount(async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/data");
      data = response.data;
    } catch (error) {
      console.error("Failed to fetch raw data:", error);
    }
  });

  // Menu selection function
  function selectMenu(menu) {
    activeMenu = menu;
  }

  // Tab selection function for Raw Data and Cleaned Data
  function selectTab(tab) {
    activeTab = tab;
  }
</script>

<style>
  .sidebar { width: 200px; background-color: #3b82f6; color: white; padding: 20px; }
  .menu-item { padding: 10px 0; cursor: pointer; font-weight: bold; }
  .menu-item-active { background-color: #2563eb; color: white; }
  .tab-button { padding: 10px 20px; cursor: pointer; font-weight: bold; border-bottom: 2px solid transparent; }
  .tab-button-active { border-color: #2563eb; }
  .content { padding: 20px; flex: 1; }
</style>

<div class="flex min-h-screen">
  <!-- Sidebar Menu -->
  <div class="sidebar">
    <h2 class="text-lg font-semibold mb-4">Menu</h2>
    <div class="menu-item {activeMenu === 'data' ? 'menu-item-active' : ''}" on:click={() => selectMenu("data")}>Data</div>
    <div class="menu-item {activeMenu === 'graphs' ? 'menu-item-active' : ''}" on:click={() => selectMenu("graphs")}>Graphs</div>
    <div class="menu-item {activeMenu === 'model' ? 'menu-item-active' : ''}" on:click={() => selectMenu("model")}>Model Training</div>
  </div>

  <!-- Main Content Area -->
  <div class="content">
    {#if activeMenu === "data"}
      <h1 class="text-3xl font-bold mb-4">Data Section</h1>

      <!-- Tab Navigation for Raw and Cleaned Data -->
      <div class="mt-4 flex space-x-4">
        <button class="tab-button {activeTab === 'raw' ? 'tab-button-active' : ''}" on:click={() => selectTab("raw")}>Raw Data</button>
        <button class="tab-button {activeTab === 'cleaned' ? 'tab-button-active' : ''}" on:click={() => selectTab("cleaned")}>Cleaned Data</button>
      </div>

      <!-- Display Raw or Cleaned Data based on Tab Selection -->
      {#if activeTab === "raw"}
        <VoterTurnoutTable />
      {:else if activeTab === "cleaned"}
        <DataCleaning />
      {/if}

    {:else if activeMenu === "graphs"}
      <!-- Placeholder for Graphs Component -->
      <p>Graphs Component</p>
      
    {:else if activeMenu === "model"}
      <!-- Placeholder for ModelTraining Component -->
      <p>Model Training Component</p>
    {/if}
  </div>
</div>

