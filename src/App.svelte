<script lang="ts">
  import { parseCSVText } from './lib/simple-parser';
  import { loadZippedBoundaries } from './lib/spikes/boundary-loader';
  import { estimateDetailedFlow, type VariableRow, type DetailedEstimateRow } from './lib/estimation-engine';
  import { exportDetailedResults } from './lib/exporter';
  import MapPreview from './lib/MapPreview.svelte';
  import MethodologyModal from './lib/MethodologyModal.svelte';
  import { fetchChangedBoundaries } from './lib/boundary-service';
  
  import crosswalkData from './assets/data/lsoa11-to-lsoa21-crosswalk.json';
  import type { ShareResult } from './lib/share-calculator';

  let variableData: VariableRow[] = [];
  let originalCodeKey = 'code';
  let originalValueKey = 'value';
  let boundaries: any = null;
  let shares: ShareResult[] = [];
  let estimates: DetailedEstimateRow[] = [];
  let totalInputPop = 0;
  let totalEstimatedPop = 0;
  let nonUnitWeights = 0;
  let status = 'Ready';
  let fileName = '';
  let direction: '11to21' | '21to11' = '11to21';
  let currentStep = 1;
  let isDarkMode = true;
  let showMethodology = false;

  import { onMount } from 'svelte';
  $: crosswalkRows = crosswalkData as unknown as ShareResult[];
  $: lsoa2011Codes = new Set(crosswalkRows.map(r => r.source_lsoa));
  $: lsoa2021Codes = new Set(crosswalkRows.map(r => r.target_lsoa));
  $: previewRows = [...estimates]
    .sort((a, b) => (Math.abs(a.ratio - 1) < 0.00000001 ? 1 : 0) - (Math.abs(b.ratio - 1) < 0.00000001 ? 1 : 0))
    .slice(0, 10);

  function inferDirection(rows: VariableRow[]): { direction: '11to21' | '21to11'; matched2011: number; matched2021: number } {
    let matched2011 = 0;
    let matched2021 = 0;
    for (const row of rows) {
      if (lsoa2011Codes.has(row.code)) matched2011 += 1;
      if (lsoa2021Codes.has(row.code)) matched2021 += 1;
    }

    return {
      direction: matched2021 > matched2011 ? '21to11' : '11to21',
      matched2011,
      matched2021
    };
  }

  $: crosswalkStats = (() => {
    const bySource = new Map<string, ShareResult[]>();
    const byTarget = new Map<string, ShareResult[]>();
    for (const row of crosswalkRows) {
      const sourceRels = bySource.get(row.source_lsoa) || [];
      sourceRels.push(row);
      bySource.set(row.source_lsoa, sourceRels);

      const targetRels = byTarget.get(row.target_lsoa) || [];
      targetRels.push(row);
      byTarget.set(row.target_lsoa, targetRels);
    }

    let stableSourceOneToOne = 0;
    let splitSources = 0;
    let complexSources = 0;
    let changedSources = 0;
    for (const rels of bySource.values()) {
      const changed = rels.length > 1 || rels.some(r => r.source_lsoa !== r.target_lsoa);
      if (rels.length === 1 && rels[0].source_lsoa === rels[0].target_lsoa) stableSourceOneToOne += 1;
      if (rels.length > 1) splitSources += 1;
      if (rels.length >= 3) complexSources += 1;
      if (changed) changedSources += 1;
    }

    let stableTargetOneToOne = 0;
    let mergedTargets = 0;
    let complexTargets = 0;
    let changedTargets = 0;
    for (const rels of byTarget.values()) {
      const changed = rels.length > 1 || rels.some(r => r.source_lsoa !== r.target_lsoa);
      if (rels.length === 1 && rels[0].source_lsoa === rels[0].target_lsoa) stableTargetOneToOne += 1;
      if (rels.length > 1) mergedTargets += 1;
      if (rels.length >= 3) complexTargets += 1;
      if (changed) changedTargets += 1;
    }

    return {
      stableSourceOneToOne,
      splitSources,
      complexSources,
      changedSources,
      sourceTotal: bySource.size,
      stableTargetOneToOne,
      mergedTargets,
      complexTargets,
      changedTargets,
      targetTotal: byTarget.size
    };
  })();

  onMount(() => {
    status = 'Ready';
  });

  async function handleVariableCSV(e: any) {
    const file = e.target.files[0];
    if (!file) return;
    fileName = file.name;
    status = 'Reading CSV file...';
    
    try {
      const text = await file.text();
      status = 'Parsing 33,755 national records...';
      
      const parsed = parseCSVText(text);
      originalCodeKey = parsed.codeKey;
      originalValueKey = parsed.valKey;
      variableData = parsed.data;

      const inferred = inferDirection(variableData);
      const codeKeyLower = originalCodeKey.toLowerCase();
      if (codeKeyLower.includes('2021') || codeKeyLower.includes('lsoa21')) {
        direction = '21to11';
      } else if (codeKeyLower.includes('2011') || codeKeyLower.includes('lsoa11')) {
        direction = '11to21';
      } else {
        direction = inferred.direction;
      }
      const directionLabel = direction === '21to11' ? 'LSOA 2021 → LSOA 2011' : 'LSOA 2011 → LSOA 2021';
      status = `Successfully loaded ${variableData.length.toLocaleString()} records. Auto-selected ${directionLabel} (${inferred.matched2021.toLocaleString()} matched 2021 codes; ${inferred.matched2011.toLocaleString()} matched 2011 codes).`;
      if (variableData.length > 0) currentStep = 2;
    } catch (err) {
      status = 'Error parsing CSV file. Please check format.';
      console.error(err);
    }
  }

  async function handleBoundaries(e: any) {
    const file = e.target.files[0];
    if (!file) return;
    boundaries = await loadZippedBoundaries(file);
    status = `Loaded boundary file successfully.`;
  }

  async function runCalculation() {
    shares = crosswalkData as unknown as ShareResult[];
    estimates = estimateDetailedFlow(variableData, shares, direction);
    
    totalInputPop = variableData.reduce((sum, r) => sum + r.value, 0);
    totalEstimatedPop = estimates.reduce((sum, r) => sum + r.value, 0);
    nonUnitWeights = estimates.filter(r => Math.abs(r.ratio - 1) > 0.00000001).length;

    currentStep = 3;
    const boundaryLabel = direction === '11to21' ? '2021 changed target/output polygons' : '2011 changed target/output polygons';
    status = `Apportionment (${direction}) complete. Loading ONS generalised ${boundaryLabel}...`;

    try {
      boundaries = await fetchChangedBoundaries(direction, shares);
      status = `Apportionment (${direction}) complete. Generated ${estimates.length.toLocaleString()} mapping records; ${nonUnitWeights.toLocaleString()} rows have non-1 weights. Loaded ${boundaries.features?.length?.toLocaleString?.() || 0} ONS generalised boundary polygons.`;
    } catch (e) {
      console.error(e);
      boundaries = null;
      status = `Apportionment (${direction}) complete, but the ONS generalised boundary polygons failed to load.`;
    }
  }

  function downloadResults() {
    exportDetailedResults(estimates, originalValueKey, direction);
  }

  function resetApp() {
    variableData = [];
    boundaries = null;
    shares = [];
    estimates = [];
    currentStep = 1;
    fileName = '';
    status = 'Ready';
  }
</script>

<div class="{isDarkMode ? 'dark bg-slate-900 text-slate-100' : 'bg-slate-50 text-slate-800'} min-h-screen flex flex-col font-sans transition-colors duration-200">
  <!-- Header -->
  <header class="{isDarkMode ? 'bg-slate-800 border-slate-700 text-white' : 'bg-indigo-700 text-white'} shadow-md border-b">
    <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">LSOA 2011 to 2021 Estimator</h1>
        <p class="{isDarkMode ? 'text-slate-400' : 'text-indigo-200'} text-sm">Official ONS Geographic Proportional Apportionment Tool</p>
      </div>
      <div class="flex items-center space-x-4">
        <button 
          type="button"
          class="text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors cursor-pointer {isDarkMode ? 'bg-slate-700 text-slate-200 hover:bg-slate-600' : 'bg-indigo-800 text-indigo-100 hover:bg-indigo-900'}"
          on:click={() => { showMethodology = !showMethodology; console.log('Toggled showMethodology:', showMethodology); }}
        >
          {showMethodology ? 'Estimator' : 'Methodology & Sources'}
        </button>
        <button 
          type="button"
          class="flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors cursor-pointer {isDarkMode ? 'bg-slate-700 text-amber-400 hover:bg-slate-600' : 'bg-indigo-800 text-indigo-100 hover:bg-indigo-900'}"
          on:click={() => isDarkMode = !isDarkMode}
          title="Toggle Theme"
        >
          {#if isDarkMode}
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path></svg>
            <span>Light Mode</span>
          {:else}
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
            <span>Dark Mode</span>
          {/if}
        </button>
        <span class="bg-indigo-800/60 text-indigo-100 text-xs px-3 py-1 rounded-full font-medium hidden sm:inline-block">v1.0 Production</span>
      </div>
    </div>
  </header>

  <!-- Stepper Header -->
  {#if !showMethodology}
    <div class="{isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} border-b shadow-sm">
      <div class="max-w-4xl mx-auto px-6 py-4 flex justify-between items-center text-sm font-medium">
        <div class="flex items-center space-x-2 {currentStep >= 1 ? (isDarkMode ? 'text-indigo-400' : 'text-indigo-600') : 'text-slate-500'}">
          <span class="w-7 h-7 rounded-full flex items-center justify-center border {currentStep >= 1 ? (isDarkMode ? 'border-indigo-500 bg-indigo-950/50' : 'border-indigo-600 bg-indigo-50') : 'border-slate-600'}">1</span>
          <span>Upload Data</span>
        </div>
        <div class="h-0.5 flex-1 {isDarkMode ? 'bg-slate-700' : 'bg-slate-200'} mx-4"></div>
        <div class="flex items-center space-x-2 {currentStep >= 2 ? (isDarkMode ? 'text-indigo-400' : 'text-indigo-600') : 'text-slate-500'}">
          <span class="w-7 h-7 rounded-full flex items-center justify-center border {currentStep >= 2 ? (isDarkMode ? 'border-indigo-500 bg-indigo-950/50' : 'border-indigo-600 bg-indigo-50') : 'border-slate-600'}">2</span>
          <span>Configure & Run</span>
        </div>
        <div class="h-0.5 flex-1 {isDarkMode ? 'bg-slate-700' : 'bg-slate-200'} mx-4"></div>
        <div class="flex items-center space-x-2 {currentStep >= 3 ? (isDarkMode ? 'text-indigo-400' : 'text-indigo-600') : 'text-slate-500'}">
          <span class="w-7 h-7 rounded-full flex items-center justify-center border {currentStep >= 3 ? (isDarkMode ? 'border-indigo-500 bg-indigo-950/50' : 'border-indigo-600 bg-indigo-50') : 'border-slate-600'}">3</span>
          <span>Audit & Export</span>
        </div>
      </div>
    </div>
  {/if}

  <!-- Main Container -->
  <main class="max-w-5xl mx-auto px-6 py-8 flex-1 w-full">
    {#if showMethodology}
      <MethodologyModal {isDarkMode} onBack={() => showMethodology = false} />
    {:else}
      <!-- Status Banner -->
      <div class="mb-6 {isDarkMode ? 'bg-slate-800 border-slate-700 text-indigo-300' : 'bg-indigo-50 border-indigo-100 text-indigo-900'} border px-4 py-3 rounded-lg text-sm flex items-center justify-between">
        <div><span class="font-semibold">Status:</span> {status}</div>
        {#if variableData.length > 0 && currentStep < 3}
          <div class="text-xs {isDarkMode ? 'bg-indigo-950 text-indigo-300' : 'bg-indigo-100 text-indigo-800'} px-2.5 py-1 rounded font-medium">
            {variableData.length.toLocaleString()} rows ready
          </div>
        {/if}
      </div>

      <!-- Step 1: Upload -->
      {#if currentStep === 1}
        <div class="{isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} rounded-xl shadow-sm border p-8 space-y-6">
          <div>
            <h2 class="text-lg font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">Step 1: Upload Variable Data</h2>
            <p class="text-sm {isDarkMode ? 'text-slate-400' : 'text-slate-500'} mt-1">Upload your CSV file containing 2011 LSOA codes and the variable to be estimated (e.g. population).</p>
          </div>

          <div class="border-2 border-dashed {isDarkMode ? 'border-slate-600 hover:border-indigo-400 bg-slate-900/50' : 'border-slate-300 hover:border-indigo-500 bg-slate-50/50'} rounded-xl p-8 text-center transition-colors relative">
            <input type="file" id="csv-upload" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10" on:change={handleVariableCSV} accept=".csv" />
            <div class="flex flex-col items-center space-y-2 pointer-events-none">
              <svg class="w-12 h-12 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
              <span class="{isDarkMode ? 'text-slate-200' : 'text-slate-700'} font-medium">Click or Drop Variable CSV here</span>
              <span class="text-xs text-slate-400">Supports standard CSV with LSOA codes and numeric variable columns</span>
            </div>
          </div>

          {#if fileName}
            <div class="flex items-center justify-between {isDarkMode ? 'bg-emerald-950/50 border-emerald-800 text-emerald-300' : 'bg-emerald-50 border-emerald-200 text-emerald-800'} border px-4 py-3 rounded-lg text-sm">
              <span>✓ Loaded file: <strong>{fileName}</strong></span>
              <button type="button" class="text-xs underline font-medium cursor-pointer" on:click={() => document.getElementById('csv-upload')?.click()}>Change file</button>
            </div>
          {/if}
        </div>

      <!-- Step 2: Configure & Run -->
      {:else if currentStep === 2}
        <div class="{isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} rounded-xl shadow-sm border p-8 space-y-6">
          <div>
            <h2 class="text-lg font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">Step 2: Spatial Apportionment Configuration</h2>
            <p class="text-sm {isDarkMode ? 'text-slate-400' : 'text-slate-500'} mt-1">Review your loaded data and optional boundary attachments before running the national crosswalk.</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="{isDarkMode ? 'bg-slate-900/60 border-slate-700' : 'bg-slate-50 border-slate-200'} p-4 rounded-lg border space-y-2">
              <h3 class="text-xs font-semibold uppercase text-slate-400 tracking-wider">Estimation Direction</h3>
              <select bind:value={direction} class="w-full mt-1 p-2 text-sm rounded border {isDarkMode ? 'bg-slate-800 border-slate-600 text-white' : 'bg-white border-slate-300 text-slate-900'}">
                <option value="11to21">LSOA 2011 → LSOA 2021</option>
                <option value="21to11">LSOA 2021 → LSOA 2011</option>
              </select>
              <p class="text-xs text-slate-400 mt-1">Select whether your input data corresponds to 2011 or 2021 boundaries.</p>
            </div>

            <div class="{isDarkMode ? 'bg-slate-900/60 border-slate-700' : 'bg-slate-50 border-slate-200'} p-4 rounded-lg border space-y-2">
              <h3 class="text-xs font-semibold uppercase text-slate-400 tracking-wider">Input Summary</h3>
              <p class="text-sm {isDarkMode ? 'text-slate-300' : 'text-slate-700'}"><strong>Records:</strong> {variableData.length.toLocaleString()} LSOAs</p>
              <p class="text-sm {isDarkMode ? 'text-slate-300' : 'text-slate-700'}"><strong>Code Column:</strong> <code>{originalCodeKey}</code></p>
              <p class="text-sm {isDarkMode ? 'text-slate-300' : 'text-slate-700'}"><strong>Value Column:</strong> <code>{originalValueKey}</code></p>
            </div>
          </div>

          <div class="flex justify-between pt-4 border-t {isDarkMode ? 'border-slate-700' : 'border-slate-100'}">
            <button type="button" class="px-4 py-2 text-sm font-medium cursor-pointer {isDarkMode ? 'text-slate-300 bg-slate-700 hover:bg-slate-600' : 'text-slate-600 bg-slate-100 hover:bg-slate-200'} rounded-lg transition-colors" on:click={() => currentStep = 1}>Back</button>
            <button type="button" class="px-6 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg shadow-sm transition-colors flex items-center space-x-2 cursor-pointer" on:click={runCalculation}>
              <span>Run National Estimation</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
            </button>
          </div>
        </div>

      <!-- Step 3: Audit & Export -->
      {:else if currentStep === 3}
        <div class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            <div class="lg:col-span-5 space-y-6">
              <!-- Summary Cards -->
              <div class="{isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} rounded-xl shadow-sm border p-4">
                <div class="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-1 gap-3">
                  <div class="space-y-0.5">
                    <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Total Input ({direction === '11to21' ? '2011' : '2021'})</span>
                    <div class="text-lg font-bold {isDarkMode ? 'text-white' : 'text-slate-900'}">{totalInputPop.toLocaleString(undefined, {maximumFractionDigits: 2})}</div>
                  </div>
                  <div class="space-y-0.5 sm:border-l sm:pl-3 lg:border-l-0 lg:pl-0 lg:border-t lg:pt-3 {isDarkMode ? 'border-slate-700' : 'border-slate-200'}">
                    <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Total Estimated ({direction === '11to21' ? '2021' : '2011'})</span>
                    <div class="text-lg font-bold {isDarkMode ? 'text-white' : 'text-slate-900'}">{totalEstimatedPop.toLocaleString(undefined, {maximumFractionDigits: 2})}</div>
                  </div>
                  <div class="space-y-0.5 sm:border-l sm:pl-3 lg:border-l-0 lg:pl-0 lg:border-t lg:pt-3 {isDarkMode ? 'border-slate-700' : 'border-slate-200'}">
                    <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Conservation Check</span>
                    <div class="text-lg font-bold {Math.abs(totalInputPop - totalEstimatedPop) > 5 ? 'text-red-500' : 'text-emerald-400'}">
                      {Math.abs(totalInputPop - totalEstimatedPop) < 0.01 ? 'Perfect Match' : `${Math.abs(totalInputPop - totalEstimatedPop).toFixed(2)} diff`}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action Bar -->
              <div class="{isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} rounded-xl shadow-sm border p-6 space-y-4">
                <div>
                  <h3 class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">Apportionment Complete</h3>
                  <p class="text-sm {isDarkMode ? 'text-slate-400' : 'text-slate-500'}">Generated {estimates.length.toLocaleString()} target mapping rows across national boundaries. {nonUnitWeights.toLocaleString()} rows use a non-1 apportionment weight.</p>
                </div>
                <div class="flex flex-col sm:flex-row gap-3">
                  <button type="button" class="px-4 py-2 text-sm font-medium cursor-pointer {isDarkMode ? 'text-slate-300 bg-slate-700 hover:bg-slate-600' : 'text-slate-700 bg-slate-100 hover:bg-slate-200'} rounded-lg transition-colors" on:click={resetApp}>Start Over</button>
                  <button type="button" class="px-5 py-2 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm transition-colors flex items-center justify-center space-x-2 cursor-pointer" on:click={downloadResults}>
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                    <span>Download Estimates (CSV)</span>
                  </button>
                </div>
              </div>

              <!-- Relationship Statistics -->
              <div class="{isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} rounded-xl shadow-sm border p-6 space-y-4">
                <h3 class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{direction === '11to21' ? '2011 → 2021 Relationship Statistics' : '2021 → 2011 Relationship Statistics'}</h3>
                <p class="text-xs {isDarkMode ? 'text-slate-400' : 'text-slate-500'}">
                  Shows both active-direction splits and output-side merges from the ONS Exact Fit crosswalk. The map to the right shows changed {direction === '11to21' ? 'LSOA 2021 target/output polygons' : 'LSOA 2011 target/output polygons'} using ONS Generalised Clipped boundaries.
                </p>

                {#if direction === '11to21'}
                  <div class="space-y-2">
                    <h4 class="text-xs font-semibold uppercase tracking-wider text-slate-400">Input-side splits: 2011 LSOAs → 2021 LSOAs</h4>
                    <ul class="space-y-2 text-sm {isDarkMode ? 'text-slate-300' : 'text-slate-700'}">
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">Stable 1-to-1 LSOA11 relationships</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.stableSourceOneToOne.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.stableSourceOneToOne / crosswalkStats.sourceTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">LSOA11s split across 2+ LSOA21s</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.splitSources.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.splitSources / crosswalkStats.sourceTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">LSOA11s split across 3+ LSOA21s</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.complexSources.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.complexSources / crosswalkStats.sourceTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                    </ul>
                  </div>

                  <div class="space-y-2">
                    <h4 class="text-xs font-semibold uppercase tracking-wider text-slate-400">Output-side merges: 2021 LSOAs from 2011 LSOAs</h4>
                    <ul class="space-y-2 text-sm {isDarkMode ? 'text-slate-300' : 'text-slate-700'}">
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">LSOA21s made from 2+ LSOA11s</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.mergedTargets.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.mergedTargets / crosswalkStats.targetTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">LSOA21s made from 3+ LSOA11s</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.complexTargets.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.complexTargets / crosswalkStats.targetTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                    </ul>
                  </div>
                {:else}
                  <div class="space-y-2">
                    <h4 class="text-xs font-semibold uppercase tracking-wider text-slate-400">Input-side splits: 2021 LSOAs → 2011 LSOAs</h4>
                    <ul class="space-y-2 text-sm {isDarkMode ? 'text-slate-300' : 'text-slate-700'}">
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">Stable 1-to-1 LSOA21 relationships</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.stableTargetOneToOne.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.stableTargetOneToOne / crosswalkStats.targetTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">LSOA21s split across 2+ LSOA11s</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.mergedTargets.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.mergedTargets / crosswalkStats.targetTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">LSOA21s split across 3+ LSOA11s</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.complexTargets.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.complexTargets / crosswalkStats.targetTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                    </ul>
                  </div>

                  <div class="space-y-2">
                    <h4 class="text-xs font-semibold uppercase tracking-wider text-slate-400">Output-side merges: 2011 LSOAs from 2021 LSOAs</h4>
                    <ul class="space-y-2 text-sm {isDarkMode ? 'text-slate-300' : 'text-slate-700'}">
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">LSOA11s receiving from 2+ LSOA21s</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.splitSources.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.splitSources / crosswalkStats.sourceTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                      <li class="flex justify-between items-center gap-3 {isDarkMode ? 'bg-slate-900/60' : 'bg-slate-50'} p-2.5 rounded-lg">
                        <span class="{isDarkMode ? 'text-slate-400' : 'text-slate-600'}">LSOA11s receiving from 3+ LSOA21s</span>
                        <span class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">{crosswalkStats.complexSources.toLocaleString()} <span class="text-xs text-slate-400 font-normal">({(crosswalkStats.complexSources / crosswalkStats.sourceTotal * 100).toFixed(2)}%)</span></span>
                      </li>
                    </ul>
                  </div>
                {/if}
              </div>
            </div>

            {#if boundaries}
              <div class="lg:col-span-7 {isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} rounded-xl shadow-sm border p-5">
                <h3 class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'} mb-3">Spatial Boundary Preview</h3>
                <MapPreview geojson={boundaries} {direction} />
              </div>
            {/if}
          </div>

          <!-- Preview Table -->
          <div class="{isDarkMode ? 'bg-slate-800 border-slate-700' : 'bg-white border-slate-200'} rounded-xl shadow-sm border overflow-hidden">
            <div class="px-6 py-4 border-b {isDarkMode ? 'border-slate-700' : 'border-slate-200'} flex justify-between items-center">
              <h3 class="font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">Output Data Preview (non-1 weights shown first)</h3>
              <span class="text-xs text-slate-400">Schema: lsoa2011, lsoa2021, weight, {originalValueKey}</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full text-left border-collapse text-sm">
                <thead>
                  <tr class="{isDarkMode ? 'bg-slate-900/70 text-slate-400 border-slate-700' : 'bg-slate-50 text-slate-500 border-slate-200'} font-semibold uppercase text-xs tracking-wider border-b">
                    <th class="px-6 py-3">LSOA 2011</th>
                    <th class="px-6 py-3">LSOA 2021</th>
                    <th class="px-6 py-3">Weight</th>
                    <th class="px-6 py-3">Value ({originalValueKey})</th>
                  </tr>
                </thead>
                <tbody class="divide-y {isDarkMode ? 'divide-slate-700 text-slate-300' : 'divide-slate-200 text-slate-700'}">
                  {#each previewRows as est}
                    <tr class="{isDarkMode ? 'hover:bg-slate-700/50' : 'hover:bg-slate-50/50'}">
                      <td class="px-6 py-3 font-mono text-xs">{est.lsoa2011}</td>
                      <td class="px-6 py-3 font-mono text-xs {isDarkMode ? 'text-indigo-400' : 'text-indigo-600'} font-medium">{est.lsoa2021}</td>
                      <td class="px-6 py-3">{est.ratio.toFixed(4)}</td>
                      <td class="px-6 py-3 font-semibold">{est.value.toLocaleString(undefined, {maximumFractionDigits: 2})}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      {/if}
    {/if}
  </main>

  <!-- Footer -->
  <footer class="{isDarkMode ? 'bg-slate-800 border-slate-700 text-slate-400' : 'bg-white border-slate-200 text-slate-400'} border-t py-6 mt-12 text-center text-xs">
    LSOA11 to LSOA21 Proportional Estimator • Built with Svelte & Tailwind CSS
  </footer>
</div>
