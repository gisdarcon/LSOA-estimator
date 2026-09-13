// src/lib/spikes/spatial-worker.ts
import { booleanPointInPolygon, point } from '@turf/turf';

self.onmessage = (e) => {
  const { postcodePoint, boundaryPolygon } = e.data;

  const pt = point([postcodePoint.long, postcodePoint.lat]);
  const isInside = booleanPointInPolygon(pt, boundaryPolygon);

  self.postMessage({ isInside });
};
