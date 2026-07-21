"""
Generate samplesheet.csv from a directory of long-read files.

Each of the long-read files should be either:
   - a FASTQ file (.fastq.gz, .fq.gz, .fastq, .fq) -> ONT
   - unaligned BAM file (.bam) -> PacBio HiFi CCS
The sample name will be the dile basename with the read suffix stripped. 

Output columns: sample, reads, reference
"""

import argparse
import csv
import sys
from pathlib import Path

READ_SUFFIXES = ('.fastq.gz', '.fq.gz', '.fastq', '.fq', '.bam')

def find_reads(input_dir: Path) -> list[Path]:
    """Find all long read files in the directory."""
    reads = []
    for suffix in READ_SUFFIXES:
        reads.extend(input_dir.glob(f'*{suffix}'))
    return sorted(set(reads))

def strip_suffix(name: str) -> str:
    for suffix in READ_SUFFIXES:
        if name.endswith(suffix):
            return name[:-len(suffix)]
    return name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=Path, required=True, help='Directory containing long-read files')
    parser.add_argument('--reference', type=Path, required=True, help='Reference FASTA (relative to reference_dir)')
    parser.add_argument('--output', type=Path, default=Path('samplesheet.csv'), help='Output CSV file')
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    if not input_dir.is_dir():
        print(f"Error: Input directory '{input_dir}' does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    reads = find_reads(input_dir=input_dir)
    if not reads:
        print(f"Error: No long-read files found in '{input_dir}'", file=sys.stderr)
        sys.exit(1)

    rows = []
    seen = {}
    for f in reads:
        sample_name = strip_suffix(f.name)
        if sample_name in seen:
            print(f"Warning: Duplicate sample name '{sample_name}' found for file '{f}'. Skipping.", file=sys.stderr)
            continue
        seen[sample_name] = f
        rows.append((sample_name, str(f), str(args.reference)))

    if not rows:
        print(f"Error: No valid samples found in '{input_dir}'", file=sys.stderr)
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['sample', 'reads', 'reference'])
        writer.writerows(rows)

    print(f'Wrote {len(rows)} samples to {args.output}')

if __name__ == '__main__':
    main()