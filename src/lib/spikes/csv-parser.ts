// src/lib/spikes/csv-parser.ts
import Papa from 'papaparse';

export interface PostcodeLookupRow {
  pcd?: string;
  pcds?: string;
  lsoa11?: string;
  lsoa21?: string;
  lat?: number;
  long?: number;
  [key: string]: string | number | undefined;
}

export async function parseVariableCSV(file: File): Promise<any[]> {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      dynamicTyping: true,
      complete: (results: Papa.ParseResult<any>) => {
        resolve(results.data as any[]);
      },
      error: reject
    });
  });
}
