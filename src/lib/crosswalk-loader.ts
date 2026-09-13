import crosswalkData from '../assets/data/lsoa11-to-lsoa21-crosswalk.json';
import type { ShareResult } from './share-calculator';

export function loadCrosswalk(): ShareResult[] {
  return crosswalkData as unknown as ShareResult[];
}
