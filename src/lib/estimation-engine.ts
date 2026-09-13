// src/lib/estimation-engine.ts
import type { ShareResult } from './share-calculator';

export interface VariableRow {
  code: string;
  value: number;
}

export interface DetailedEstimateRow {
  lsoa2011: string;
  lsoa2021: string;
  value: number;
  ratio: number;
}

export function estimateDetailedFlow(
  variableData: VariableRow[],
  shares: ShareResult[],
  direction: '11to21' | '21to11' = '11to21'
): DetailedEstimateRow[] {
  const results: DetailedEstimateRow[] = [];

  const shareMap = new Map<string, ShareResult[]>();

  if (direction === '11to21') {
    shares.forEach(s => {
      const list = shareMap.get(s.source_lsoa) || [];
      list.push(s);
      shareMap.set(s.source_lsoa, list);
    });

    variableData.forEach(row => {
      const relevantShares = shareMap.get(row.code);
      if (!relevantShares) {
        results.push({ lsoa2011: row.code, lsoa2021: row.code, value: row.value, ratio: 1.0 });
        return;
      }
      relevantShares.forEach(s => {
        results.push({ lsoa2011: s.source_lsoa, lsoa2021: s.target_lsoa, value: row.value * s.share, ratio: s.share });
      });
    });
  } else {
    // 21to11 Direction: source is target_lsoa, target is source_lsoa.
    // Use precomputed reverseShare, normalised within each LSOA21. This is
    // based on the same NSPL active residential postcode evidence, not equal
    // splitting by relationship count.
    const reverseMap = new Map<string, { source_lsoa: string; target_lsoa: string; reverseShare: number }[]>();
    shares.forEach(s => {
      const list = reverseMap.get(s.target_lsoa) || [];
      list.push({ source_lsoa: s.target_lsoa, target_lsoa: s.source_lsoa, reverseShare: s.reverseShare ?? s.share });
      reverseMap.set(s.target_lsoa, list);
    });

    variableData.forEach(row => {
      const revShares = reverseMap.get(row.code);
      if (!revShares) {
        results.push({ lsoa2011: row.code, lsoa2021: row.code, value: row.value, ratio: 1.0 });
        return;
      }
      revShares.forEach(rs => {
        results.push({ lsoa2011: rs.target_lsoa, lsoa2021: rs.source_lsoa, value: row.value * rs.reverseShare, ratio: rs.reverseShare });
      });
    });
  }

  return results;
}
