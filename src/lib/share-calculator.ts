// src/lib/share-calculator.ts
import type { PostcodeLookupRow } from './spikes/csv-parser';

export interface ShareResult {
  source_lsoa: string;
  target_lsoa: string;
  count: number;
  share: number;
  reverseShare?: number;
  weightingSource: 'postcode' | 'census' | 'ons_exact_fit' | 'nspl_aug_2024_active_residential_postcode_count_with_exact_fit_v3';
}

/**
 * Calculates shares with optional census-grade household weights.
 * @param lookupData Postcode data
 * @param censusWeights Map of LSOA Code -> Household Count
 */
export function calculateShares(
  lookupData: PostcodeLookupRow[],
  direction: '11to21' | '21to11',
  censusWeights?: Record<string, number>
): ShareResult[] {
  const sourceKey = direction === '11to21' ? 'lsoa11' : 'lsoa21';
  const targetKey = direction === '11to21' ? 'lsoa21' : 'lsoa11';

  // Use weights if provided; otherwise default to raw postcode counts
  const pairs: Record<string, number> = {};
  const sourceTotals: Record<string, number> = {};

  lookupData.forEach(row => {
    const src = row[sourceKey];
    const tgt = row[targetKey];
    if (!src || !tgt) return;

    // Logic: If censusWeights are provided for the Source, override weighting logic
    // Currently using Postcode Count baseline as primary, Census as custom override
    const weight = censusWeights ? (censusWeights[src] || 1) / 100 : 1;

    const pairId = `${src}:${tgt}`;
    pairs[pairId] = (pairs[pairId] || 0) + weight;
    sourceTotals[src] = (sourceTotals[src] || 0) + weight;
  });

  return Object.entries(pairs).map(([id, count]) => {
    const [source_lsoa, target_lsoa] = id.split(':');
    return {
      source_lsoa,
      target_lsoa,
      count,
      share: count / sourceTotals[source_lsoa],
      weightingSource: censusWeights ? 'census' : 'postcode'
    };
  });
}
