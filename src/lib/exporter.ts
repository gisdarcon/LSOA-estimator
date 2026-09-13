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

export function exportDetailedResults(rows: DetailedEstimateRow[], valueColName: string) {
  const exportData = rows.map(r => ({
    lsoa2011: r.lsoa2011,
    lsoa2021: r.lsoa2021,
    weight: r.ratio,
    [valueColName]: r.value
  }));
  exportCSV(exportData, 'lsoa11_to_lsoa21_estimated.csv');
}
