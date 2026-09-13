<script lang="ts">
  export let isDarkMode = false;
  export let onBack: () => void;
</script>

<div class="fixed inset-0 z-50 bg-slate-900/80 backdrop-blur-sm flex justify-center p-4 sm:p-6 overflow-y-auto">
  <div class="{isDarkMode ? 'bg-slate-900 text-slate-100 border-slate-700' : 'bg-white text-slate-800 border-slate-200'} border rounded-2xl shadow-2xl max-w-4xl w-full p-6 sm:p-8 space-y-8 my-auto relative">
    <div class="flex items-center justify-between border-b {isDarkMode ? 'border-slate-700' : 'border-slate-200'} pb-4 gap-4">
      <div>
        <h2 class="text-2xl font-bold {isDarkMode ? 'text-white' : 'text-slate-900'}">Methodology & Sources</h2>
        <p class="text-sm {isDarkMode ? 'text-slate-400' : 'text-slate-500'}">How the LSOA 2011 ↔ LSOA 2021 weights are built, used, and verified.</p>
      </div>
      <button 
        type="button"
        class="px-4 py-2 text-sm font-medium cursor-pointer {isDarkMode ? 'bg-slate-700 text-slate-200 hover:bg-slate-600' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'} rounded-lg transition-colors shrink-0"
        on:click={onBack}
      >
        ✕ Close Guide
      </button>
    </div>

    <div class="{isDarkMode ? 'bg-slate-800/80 border-slate-700 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-700'} p-6 rounded-xl border space-y-3">
      <h3 class="text-lg font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">1. Estimation method</h3>
      <p class="text-sm leading-relaxed">
        The app estimates additive variables, such as population counts, between 2011 and 2021 Lower Layer Super Output Areas. It does not assign every source LSOA to a single target. It uses fractional <strong>weights</strong> for each official LSOA11→LSOA21 relationship.
      </p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div class="{isDarkMode ? 'bg-slate-900 border-slate-700 text-indigo-300' : 'bg-white border-indigo-200 text-indigo-900'} p-3 rounded-lg font-mono text-xs border">
          2011 → 2021:<br />
          value_2021 = Σ(value_2011 × weight)
        </div>
        <div class="{isDarkMode ? 'bg-slate-900 border-slate-700 text-indigo-300' : 'bg-white border-indigo-200 text-indigo-900'} p-3 rounded-lg font-mono text-xs border">
          2021 → 2011:<br />
          value_2011 = Σ(value_2021 × reverse_weight)
        </div>
      </div>
      <p class="text-sm leading-relaxed">
        The direction is automatically selected from the uploaded file. A column named <code>lsoa2011</code> selects 2011→2021; a column named <code>lsoa2021</code> selects 2021→2011. If the column is generic, the app compares uploaded codes against the official 2011 and 2021 code sets.
      </p>
    </div>

    <div class="{isDarkMode ? 'bg-slate-800/80 border-slate-700 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-700'} p-6 rounded-xl border space-y-3">
      <h3 class="text-lg font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">2. How weights are built</h3>
      <ol class="space-y-2 text-sm pl-4 list-decimal">
        <li>The <strong>ONS Exact Fit Lookup V3</strong> is used as the authoritative list of valid LSOA11→LSOA21 relationships.</li>
        <li>The <strong>NSPL 2011 Census (August 2024)</strong> and <strong>NSPL 2021 Census (August 2024)</strong> files are joined by normalised postcode.</li>
        <li>The build keeps active residential England postcodes only: <code>usertype = 0</code>, <code>doterm</code> empty, <code>ctry = E92000001</code>.</li>
        <li>Postcodes are counted inside each official LSOA11→LSOA21 pair. The forward weight is normalised within each 2011 LSOA. The reverse weight is normalised within each 2021 LSOA.</li>
      </ol>
      <p class="text-sm leading-relaxed">
        This produces empirical fractional weights where active residential postcode evidence reflects uneven splits across boundary changes. It also conserves totals in both directions because weights sum to 1 within each source geography.
      </p>
    </div>

    <div class="{isDarkMode ? 'bg-slate-800/80 border-slate-700 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-700'} p-6 rounded-xl border space-y-3">
      <h3 class="text-lg font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">3. Current crosswalk coverage and checks</h3>
      <ul class="space-y-1.5 text-sm pl-4 list-disc">
        <li><strong>LSOA11 source areas:</strong> 32,844</li>
        <li><strong>LSOA21 target areas:</strong> 33,755</li>
        <li><strong>Official exact-fit relationship rows:</strong> 33,856</li>
        <li><strong>Active residential England postcode evidence used:</strong> 1,415,849 postcodes</li>
        <li><strong>Forward weight checks:</strong> all 2011 source weights sum to 1</li>
        <li><strong>Reverse weight checks:</strong> all 2021 source weights sum to 1</li>
      </ul>
      <p class="text-sm leading-relaxed">
        Example empirical fractional split (forward): <code>E01000010 → E01034473 = 0.45569620</code> and <code>E01000010 → E01034474 = 0.54430380</code>.
      </p>
      <p class="text-sm leading-relaxed">
        Example empirical fractional split (reverse): <code>E01028040 ← E01033769 = 0.4375</code> and <code>E01028041 ← E01033769 = 0.5625</code>.
      </p>
    </div>

    <div class="{isDarkMode ? 'bg-slate-800/80 border-slate-700 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-700'} p-6 rounded-xl border space-y-3">
      <h3 class="text-lg font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">4. Boundary-change map</h3>
      <p class="text-sm leading-relaxed">
        The map is a visual QA layer for boundary changes. It uses real ONS polygon boundaries, not centroid points or synthetic geometries. To keep the static browser app responsive, it loads only the changed LSOA polygons needed for the selected direction rather than every LSOA in England and Wales.
      </p>
      <ul class="space-y-1.5 text-sm pl-4 list-disc">
        <li><strong>2011 → 2021:</strong> maps the changed <strong>LSOA 2021 target/output polygons</strong> from <strong>Lower Layer Super Output Areas (December 2021) Boundaries EW BGC V5</strong>.</li>
        <li><strong>2021 → 2011:</strong> maps the changed <strong>LSOA 2011 target/output polygons</strong> from <strong>Lower Layer Super Output Areas (December 2011) Boundaries EW BGC V3</strong>.</li>
        <li>Both layers use ONS <strong>Generalised Clipped</strong> polygon boundaries and retain official LSOA codes/names in map popups.</li>
        <li>Current bundled changed-boundary coverage: <strong>1,945 LSOA21 polygons</strong> for forward output and <strong>1,034 LSOA11 polygons</strong> for reverse output.</li>
      </ul>
    </div>

    <div class="{isDarkMode ? 'bg-slate-800/80 border-slate-700 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-700'} p-6 rounded-xl border space-y-3">
      <h3 class="text-lg font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">5. Official ONS Geoportal sources</h3>
      <p class="text-sm leading-relaxed">
        Source datasets are from the official <a href="https://geoportal.statistics.gov.uk/" target="_blank" rel="noopener noreferrer" class="text-indigo-400 underline hover:text-indigo-300">ONS Open Geography Portal</a>. The app uses the England subset for the estimator.
      </p>
      <ul class="space-y-3 text-sm pl-4 list-disc">
        <li>
          <a href="https://geoportal.statistics.gov.uk/datasets/ons::lsoa-2011-to-lsoa-2021-to-local-authority-district-2022-exact-fit-lookup-for-ew-v3/about" target="_blank" rel="noopener noreferrer" class="text-indigo-400 underline hover:text-indigo-300 font-medium">
            LSOA (2011) to LSOA (2021) to Local Authority District (2022) Exact Fit Lookup for EW (V3)
          </a>
          <p class="text-xs {isDarkMode ? 'text-slate-400' : 'text-slate-500'} mt-0.5">Authoritative LSOA11↔LSOA21 relationship table used to constrain all relationships.</p>
        </li>
        <li>
          <a href="https://geoportal.statistics.gov.uk/datasets/c5afedb9204a47e99559a4880feddcb1/about" target="_blank" rel="noopener noreferrer" class="text-indigo-400 underline hover:text-indigo-300 font-medium">
            National Statistics Postcode Lookup - 2011 Census (August 2024) for the UK
          </a>
          <p class="text-xs {isDarkMode ? 'text-slate-400' : 'text-slate-500'} mt-0.5">Exact file used for 2011 LSOA membership. The downloaded archive contains <code>Data/multi_csv/NSPL_AUG_2024_UK_*.csv</code>.</p>
        </li>
        <li>
          <a href="https://geoportal.statistics.gov.uk/datasets/73ce619853044aaaa6f7fa5b90765b85/about" target="_blank" rel="noopener noreferrer" class="text-indigo-400 underline hover:text-indigo-300 font-medium">
            National Statistics Postcode Lookup - 2021 Census (August 2024) for the UK
          </a>
          <p class="text-xs {isDarkMode ? 'text-slate-400' : 'text-slate-500'} mt-0.5">Exact file used for 2021 LSOA membership. The downloaded archive contains <code>Data/multi_csv/NSPL21_AUG_2024_UK_*.csv</code>.</p>
        </li>
        <li>
          <a href="https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2011-boundaries-ew-bgc-v3/about" target="_blank" rel="noopener noreferrer" class="text-indigo-400 underline hover:text-indigo-300 font-medium">
            Lower Layer Super Output Areas (December 2011) Boundaries EW BGC (V3)
          </a>
          <p class="text-xs {isDarkMode ? 'text-slate-400' : 'text-slate-500'} mt-0.5">Official 2011 boundary source reference.</p>
        </li>
        <li>
          <a href="https://geoportal.statistics.gov.uk/datasets/ons::lower-layer-super-output-areas-december-2021-boundaries-generalised-clipped-ew-bgc/about" target="_blank" rel="noopener noreferrer" class="text-indigo-400 underline hover:text-indigo-300 font-medium">
            Lower Layer Super Output Areas (December 2021) Boundaries Generalised Clipped EW BGC
          </a>
          <p class="text-xs {isDarkMode ? 'text-slate-400' : 'text-slate-500'} mt-0.5">Official 2021 generalised clipped boundary source used for fast map visualisation.</p>
        </li>
      </ul>
    </div>

    <div class="{isDarkMode ? 'bg-slate-800/80 border-slate-700 text-slate-300' : 'bg-slate-50 border-slate-200 text-slate-700'} p-6 rounded-xl border space-y-3">
      <h3 class="text-lg font-semibold {isDarkMode ? 'text-white' : 'text-slate-900'}">6. Limitations</h3>
      <ul class="space-y-1.5 text-sm pl-4 list-disc">
        <li>The browser app uses a precomputed static crosswalk; it does not run full point-in-polygon analysis during upload.</li>
        <li>The weighting evidence is postcode-count based, using active residential postcodes from NSPL August 2024. It is suitable for additive variables, but it is not a substitute for bespoke address-level or household-level weighting where such data is available.</li>
        <li>Only additive variables should be apportioned directly. Rates, percentages, medians, and ranks should be converted to counts or numerator/denominator components first.</li>
      </ul>
    </div>

    <div class="flex justify-end pt-2">
      <button 
        type="button" 
        class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm rounded-lg shadow transition-colors cursor-pointer"
        on:click={onBack}
      >
        Close Guide & Return to Estimator
      </button>
    </div>
  </div>
</div>
