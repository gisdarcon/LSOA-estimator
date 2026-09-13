#!/usr/bin/env python3
"""Build real LSOA11↔LSOA21 postcode-count weights from ONS Geoportal data.

Inputs downloaded from ONS Geoportal / ArcGIS item data:
- National Statistics Postcode Lookup - 2011 Census (August 2024) for the UK
- National Statistics Postcode Lookup - 2021 Census (August 2024) for the UK
- LSOA (2011) to LSOA (2021) to LAD (2022) Exact Fit Lookup for EW (V3)

Method:
- Join NSPL 2011 and NSPL 2021 by normalised postcode.
- Keep active residential England postcodes: usertype == 0, doterm empty, ctry == E92000001.
- Count postcodes in each official exact-fit LSOA11→LSOA21 pair.
- Calculate forward weight by LSOA11 total and reverse_weight by LSOA21 total.
- Use the Exact Fit Lookup as the authoritative set of valid relationships.
"""
from __future__ import annotations

import csv
import json
import pathlib
import zipfile
from collections import Counter, defaultdict
from typing import Iterable

ROOT = pathlib.Path('/home/kd')
PROJECT = ROOT / 'projects/lsoa-estimator'
WORK = ROOT / 'NAS_Hermes/work/lsoa11-to-lsoa21-estimator'
RAW = WORK / 'data/raw'
PROCESSED = WORK / 'data/processed'
OUT_APP = PROJECT / 'src/assets/data/lsoa11-to-lsoa21-crosswalk.json'
OUT_PROCESSED = PROCESSED / 'lsoa11-to-lsoa21-crosswalk-real-aug-2024.json'

NSPL_2011 = RAW / 'nspl_2011_aug_2024.zip'
NSPL_2021 = RAW / 'nspl_2021_aug_2024.zip'
EXACT_FIT = RAW / 'lsoa11_lsoa21_exact_fit_v3.geojson'


def norm_pcd(p: str) -> str:
    return ''.join((p or '').upper().split())


def csv_members(zip_path: pathlib.Path) -> list[str]:
    with zipfile.ZipFile(zip_path) as z:
        return [n for n in z.namelist() if n.lower().endswith('.csv') and '/multi_csv/' in n]


def iter_zip_csv(zip_path: pathlib.Path, fields: list[str]) -> Iterable[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as z:
        for name in csv_members(zip_path):
            with z.open(name) as fh:
                text = (line.decode('utf-8-sig', 'replace') for line in fh)
                reader = csv.DictReader(text)
                for row in reader:
                    yield {k: (row.get(k) or '').strip() for k in fields}


def keep_active_residential_england(row: dict[str, str], lsoa_key: str) -> bool:
    return (
        row.get('usertype') == '0'
        and row.get('doterm', '') == ''
        and row.get('ctry') == 'E92000001'
        and row.get(lsoa_key, '').startswith('E01')
    )


def load_exact_pairs() -> set[tuple[str, str]]:
    with EXACT_FIT.open() as f:
        gj = json.load(f)
    pairs: set[tuple[str, str]] = set()
    for feat in gj['features']:
        p = feat['properties']
        l11 = (p.get('LSOA11CD') or '').strip()
        l21 = (p.get('LSOA21CD') or '').strip()
        # England only for the app/test universe.
        if l11.startswith('E01') and l21.startswith('E01'):
            pairs.add((l11, l21))
    return pairs


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    exact_pairs = load_exact_pairs()
    exact_sources = {s for s, _ in exact_pairs}
    exact_targets = {t for _, t in exact_pairs}
    print(f'exact-fit pairs={len(exact_pairs):,} sources2011={len(exact_sources):,} targets2021={len(exact_targets):,}')

    pcd_to_lsoa11: dict[str, str] = {}
    for row in iter_zip_csv(NSPL_2011, ['pcds', 'pcd', 'doterm', 'usertype', 'ctry', 'lsoa11']):
        if keep_active_residential_england(row, 'lsoa11'):
            pcd_to_lsoa11[norm_pcd(row['pcds'] or row['pcd'])] = row['lsoa11']
    print(f'active residential England postcodes with lsoa11={len(pcd_to_lsoa11):,}')

    pair_counts: Counter[tuple[str, str]] = Counter()
    target_counts: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    used = skipped_not_in_2011 = skipped_not_exact = 0

    for row in iter_zip_csv(NSPL_2021, ['pcds', 'pcd', 'doterm', 'usertype', 'ctry', 'lsoa21']):
        if not keep_active_residential_england(row, 'lsoa21'):
            continue
        pcd = norm_pcd(row['pcds'] or row['pcd'])
        l11 = pcd_to_lsoa11.get(pcd)
        if not l11:
            skipped_not_in_2011 += 1
            continue
        l21 = row['lsoa21']
        pair = (l11, l21)
        # The exact-fit lookup is the authoritative allowed relationship set.
        if pair not in exact_pairs:
            skipped_not_exact += 1
            continue
        pair_counts[pair] += 1
        source_counts[l11] += 1
        target_counts[l21] += 1
        used += 1

    print(f'joined postcode evidence used={used:,} skipped_no_2011={skipped_not_in_2011:,} skipped_not_exact={skipped_not_exact:,}')
    print(f'counted pairs={len(pair_counts):,} sources={len(source_counts):,} targets={len(target_counts):,}')

    # Ensure every exact-fit pair exists in the app crosswalk. If a relationship has
    # no active residential postcode evidence, use equal fallback within its source/target
    # groups so both directions remain complete and conservative.
    by_source_exact: dict[str, list[str]] = defaultdict(list)
    by_target_exact: dict[str, list[str]] = defaultdict(list)
    for l11, l21 in sorted(exact_pairs):
        by_source_exact[l11].append(l21)
        by_target_exact[l21].append(l11)

    rows = []
    for l11, l21 in sorted(exact_pairs):
        cnt = pair_counts[(l11, l21)]
        if source_counts[l11]:
            forward = cnt / source_counts[l11]
        else:
            forward = 1 / len(by_source_exact[l11])
        if target_counts[l21]:
            reverse = cnt / target_counts[l21]
        else:
            reverse = 1 / len(by_target_exact[l21])
        rows.append({
            'source_lsoa': l11,
            'target_lsoa': l21,
            'count': int(cnt),
            'share': round(forward, 8),
            'reverseShare': round(reverse, 8),
            'weightingSource': 'nspl_aug_2024_active_residential_postcode_count_with_exact_fit_v3',
        })

    OUT_PROCESSED.write_text(json.dumps(rows, separators=(',', ':')))
    OUT_APP.write_text(json.dumps(rows, separators=(',', ':')))

    # QA summaries
    fsum: dict[str, float] = defaultdict(float)
    rsum: dict[str, float] = defaultdict(float)
    for r in rows:
        fsum[r['source_lsoa']] += r['share']
        rsum[r['target_lsoa']] += r['reverseShare']
    bad_f = [(k, v) for k, v in fsum.items() if abs(v - 1) > 1e-6]
    bad_r = [(k, v) for k, v in rsum.items() if abs(v - 1) > 1e-6]
    changed = [r for r in rows if r['source_lsoa'] != r['target_lsoa']]
    nontrivial = [r for r in rows if r['source_lsoa'] != r['target_lsoa'] and r['share'] not in (0, 0.5, 1)]
    print(f'wrote rows={len(rows):,} to {OUT_APP}')
    print(f'forward_bad_sums={len(bad_f)} reverse_bad_sums={len(bad_r)} changed_pairs={len(changed):,} non_50_changed_pairs={len(nontrivial):,}')
    print('sample changed rows:')
    for r in changed[:10]:
        print(r)


if __name__ == '__main__':
    main()
