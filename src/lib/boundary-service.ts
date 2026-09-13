// src/lib/boundary-service.ts
import type { ShareResult } from './share-calculator';
import changedLsoa21Polygons from '../assets/data/changed-lsoa21-polygons.json';
import changedLsoa11Polygons from '../assets/data/changed-lsoa11-polygons.json';

export type BoundaryDirection = '11to21' | '21to11';

export async function fetchChangedBoundaries(direction: BoundaryDirection, _shares: ShareResult[]): Promise<any> {
  // Static GitHub Pages app: use bundled ONS Generalised Clipped polygon layers.
  // 11→21 shows changed 2021 target LSOA polygons.
  // 21→11 shows changed 2011 source LSOA polygons.
  return direction === '11to21' ? changedLsoa21Polygons : changedLsoa11Polygons;
}
