// src/lib/spikes/boundary-loader.ts
import shp from 'shpjs';

export async function loadZippedBoundaries(file: File): Promise<any> {
  const buffer = await file.arrayBuffer();
  const geojson = await shp(buffer);
  return geojson;
}
