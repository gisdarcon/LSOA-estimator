<script lang="ts">
  import { onMount, tick } from 'svelte';
  import L from 'leaflet';
  import 'leaflet/dist/leaflet.css';

  export let geojson: any;
  export let direction: '11to21' | '21to11' = '11to21';

  let mapElement: HTMLElement;
  let map: L.Map;
  let boundaryLayer: L.GeoJSON | null = null;
  let isMaximized = false;

  const directionLabel = direction === '11to21' ? 'LSOA 2021 target/output polygons' : 'LSOA 2011 target/output polygons';

  onMount(() => {
    map = L.map(mapElement).setView([52.3555, -1.1743], 6);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19,
      className: 'greyscale-osm-tiles'
    }).addTo(map);

    updateMap();
    setTimeout(() => map.invalidateSize(), 150);
  });

  $: if (map && geojson && direction) {
    updateMap();
    setTimeout(() => map.invalidateSize(), 150);
  }

  function featureCode(feature: any): string {
    return feature?.properties?.LSOA21CD || feature?.properties?.LSOA11CD || '';
  }

  function featureName(feature: any): string {
    return feature?.properties?.LSOA21NM || feature?.properties?.LSOA11NM || '';
  }

  function updateMap() {
    if (!map || !geojson) return;
    if (boundaryLayer) {
      map.removeLayer(boundaryLayer);
      boundaryLayer = null;
    }

    boundaryLayer = L.geoJSON(geojson, {
      style: () => ({
        fillColor: '#f97316',
        color: '#ea580c',
        weight: 1,
        opacity: 0.75,
        fillOpacity: 0.42
      }),
      onEachFeature: (feature, layer) => {
        const code = featureCode(feature);
        const name = featureName(feature);
        layer.bindPopup(`<strong>${code}</strong><br>${name}<br>${directionLabel}`);
      }
    }).addTo(map);

    const bounds = boundaryLayer.getBounds();
    if (bounds.isValid()) map.fitBounds(bounds, { padding: [18, 18] });
  }

  async function toggleMaximize() {
    isMaximized = !isMaximized;
    await tick();
    if (map) {
      map.invalidateSize();
      const bounds = boundaryLayer?.getBounds();
      if (bounds?.isValid()) map.fitBounds(bounds, { padding: [18, 18] });
    }
  }
</script>

<div class:fixed={isMaximized} class:inset-4={isMaximized} class:z-50={isMaximized} class="w-full {isMaximized ? 'bg-slate-900 rounded-xl shadow-2xl p-4' : ''}">
  <div class="flex items-center justify-between mb-2 text-xs text-slate-400 gap-3">
    <span>Orange polygons = changed {directionLabel} using ONS Generalised Clipped LSOA boundaries</span>
    <div class="flex items-center gap-3">
      <span>{geojson?.features?.length?.toLocaleString?.() || 0} polygons loaded</span>
      <button type="button" class="px-2 py-1 rounded bg-slate-700 text-slate-100 hover:bg-slate-600 cursor-pointer" on:click={toggleMaximize}>
        {isMaximized ? 'Restore' : 'Maximise'}
      </button>
    </div>
  </div>
  <div bind:this={mapElement} class="map-box" class:maximized-map={isMaximized}></div>
</div>

<style>
  .map-box {
    height: 460px;
    width: 100%;
    min-height: 460px;
    border-radius: 0.5rem;
    overflow: hidden;
    border: 1px solid rgba(148, 163, 184, 0.25);
    background: #e5e7eb;
  }

  .maximized-map {
    height: calc(100vh - 6rem);
    min-height: calc(100vh - 6rem);
  }

  :global(.greyscale-osm-tiles) {
    filter: grayscale(1) saturate(0.15) contrast(0.9) brightness(1.05);
  }
</style>
