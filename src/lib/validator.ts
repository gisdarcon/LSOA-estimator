// src/lib/validator.ts
import type { PostcodeLookupRow } from './spikes/csv-parser';

export interface ValidationResult {
  valid: boolean;
  errors: string[];
}

export function validateCodes(
  lookupData: PostcodeLookupRow[],
  boundaries: any,
  direction: '11to21' | '21to11'
): ValidationResult {
  const errors: string[] = [];
  const sourceKey = direction === '11to21' ? 'lsoa11' : 'lsoa21';

  // Extract codes from boundaries
  const boundaryCodes = new Set(
    boundaries.features.map((f: any) => f.properties?.LSOA11CD || f.properties?.LSOA21CD)
  );

  // Check lookup codes against boundary set
  const missing = new Set<string>();
  lookupData.forEach(row => {
    const code = row[sourceKey];
    if (code && !boundaryCodes.has(code)) {
      missing.add(code);
    }
  });

  if (missing.size > 0) {
    errors.push(`${missing.size} codes in lookup are missing from the boundary file (e.g., ${Array.from(missing)[0]})`);
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
