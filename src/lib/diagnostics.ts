// src/lib/diagnostics.ts
import type { PostcodeLookupRow } from './spikes/csv-parser';
import type { ShareResult } from './share-calculator';

export interface DiagnosticReport {
  missingCodes: string[];
  unmatchedRecords: number;
  shareSumWarnings: string[];
}

export function runDiagnostics(
  lookupData: PostcodeLookupRow[],
  shares: ShareResult[],
  direction: '11to21' | '21to11'
): DiagnosticReport {
  const sourceKey = direction === '11to21' ? 'lsoa11' : 'lsoa21';
  const targetKey = direction === '11to21' ? 'lsoa21' : 'lsoa11';

  const report: DiagnosticReport = {
    missingCodes: [],
    unmatchedRecords: 0,
    shareSumWarnings: []
  };

  // 1. Check for missing codes
  const uniqueSources = new Set(lookupData.map(r => r[sourceKey]));
  uniqueSources.forEach(code => {
    if (!code) report.missingCodes.push('Unknown');
  });

  // 2. Validate share sums (should be 1.0)
  const totals: Record<string, number> = {};
  shares.forEach(s => {
    totals[s.source_lsoa] = (totals[s.source_lsoa] || 0) + s.share;
  });

  Object.entries(totals).forEach(([src, total]) => {
    if (Math.abs(total - 1.0) > 0.01) {
      report.shareSumWarnings.push(`Source ${src} sums to ${(total * 100).toFixed(2)}%`);
    }
  });

  return report;
}
