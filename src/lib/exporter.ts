// src/lib/exporter.ts
import Papa from 'papaparse';
import type { DetailedEstimateRow } from './estimation-engine';

export function exportCSV(data: any[], filename: string) {
  const csv = Papa.unparse(data);
  const blob = new Blob([csv], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function titleCaseFilePart(value: string): string {
  const cleaned = value.replace(/[^a-zA-Z0-9]+/g, ' ').trim();
  if (!cleaned) return 'Value';
  return cleaned
    .split(/\s+/)
    .map(part => part.charAt(0).toUpperCase() + part.slice(1))
    .join('');
}

export function exportDetailedResults(
  rows: DetailedEstimateRow[],
  valueColName: string,
  direction: '11to21' | '21to11'
) {
  const exportData = rows.map(r => ({
    lsoa2011: r.lsoa2011,
    lsoa2021: r.lsoa2021,
    weight: r.ratio,
    [valueColName]: r.value
  }));

  const directionPart = direction === '11to21' ? 'LSOA2011toLSOA2021' : 'LSOA2021toLSOA2011';
  const variablePart = titleCaseFilePart(valueColName);
  exportCSV(exportData, `${directionPart}_${variablePart}.csv`);
}
