// src/lib/simple-parser.ts
export function parseCSVText(text: string): { codeKey: string; valKey: string; data: { code: string; value: number }[] } {
  const lines = text.split(/\r?\n/).map(l => l.trim()).filter(l => l.length > 0);
  if (lines.length < 2) throw new Error("CSV too short");

  const header = lines[0].split(',').map(h => h.trim().replace(/^["\']|["\']$/g, ''));
  const codeKey = header.find(h => h.toLowerCase().includes('code') || h.toLowerCase().includes('lsoa')) || header[0];
  const valKey = header.find(h => h.toLowerCase().includes('val') || h.toLowerCase().includes('pop') || h.toLowerCase().includes('count')) || header[1];

  const codeIdx = header.indexOf(codeKey);
  const valIdx = header.indexOf(valKey);

  const data: { code: string; value: number }[] = [];
  for (let i = 1; i < lines.length; i++) {
    const parts = lines[i].split(',').map(p => p.trim().replace(/^["\']|["\']$/g, ''));
    if (parts.length > Math.max(codeIdx, valIdx)) {
      const code = parts[codeIdx];
      const value = parseFloat(parts[valIdx]) || 0;
      if (code) data.push({ code, value });
    }
  }

  return { codeKey, valKey, data };
}
