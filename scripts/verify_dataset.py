"""
Scans downloaded FaceForensics++ and/or Celeb-DF-v2 folders and reports video counts + total size per category, 
so we know exactly what we have before building extraction pipeline. Counting is recursive!

Reference counts (full datasets, for comparison against what we actually have):
    FF++ original_sequences/youtube               1,000 videos
    FF++ original_sequences/actors                   363 videos
    FF++ manipulated_sequences/Deepfakes           1,000 videos
    FF++ manipulated_sequences/Face2Face           1,000 videos
    FF++ manipulated_sequences/FaceSwap            1,000 videos
    FF++ manipulated_sequences/NeuralTextures      1,000 videos
    FF++ manipulated_sequences/FaceShifter        ~1,000 videos
    FF++ manipulated_sequences/DeepFakeDetection   3,000+ videos
    Celeb-DF Celeb-real                              590 videos
    Celeb-DF YouTube-real                            300 videos
    Celeb-DF Celeb-synthesis                       5,639 videos

Usage:
    python verify_dataset.py --ffpp /path.to/FaceForensics++ --celebdf /path.to/Celeb-DF-v2
"""

import argparse
from pathlib import Path

VIDEO_EXTS = {".mp4", ".avi", ".mov"}

def scan_folder(folder: Path):
    """Return (file_count, total_size_bytes) for videos under folder (recursive)."""
    count = 0
    size = 0
    if not folder.exists():
        return count, size
    for p in folder.rglob("*"):
        if p.is_file() and p.suffix.lower() in VIDEO_EXTS:
            count += 1
            size += p.stat().st_size
    return count, size

def human_size(num_bytes):
    n = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"

def report(root: Path, categories, header):
    print(f"\n=== {header} ====")
    total_count, total_size = 0, 0
    for cat in categories:
        count, size = scan_folder(root / cat)
        total_count += count
        total_size += size
        print(f"{cat:45s} {count:6d} videos  {human_size(size):>10s}")
    print(f"{'TOTAL':45s} {total_count:6d} videos  {human_size(total_size):>10s}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ffpp", type=str, help="Path to FaceForensics++ root")
    parser.add_argument("--celebdf", type=str, help="Path to Celeb-DF-v2 root")
    args = parser.parse_args()

    if args.ffpp:
        root = Path(args.ffpp)
        report(
            root,
            ["original_sequences/youtube", "original_sequences/actors"],
            "FaceForensics++ -- original (real)",
        )
        report(
            root,
            [
                "manipulated_sequences/DeepFakes",
                "manipulated_sequences/Face2Face",
                "manipulated_sequences/FaceSwap",
                "manipulated_sequences/NeuralTextures",
                "manipulated_sequences/FaceShifter",
                "manipulated_sequences/DeepFakeDetection",
            ],
            "FaceForensics++ -- manipulated (fake)",
        )

    if args.celebdf:
        root = Path(args.celebdf)
        report(
            root,
            ["Celeb-real", "YouTube-real", "Celeb-synthesis"],
            "Celeb-DF-v2",
        )

    if not args.ffpp and not args.celebdf:
        parser.print_help()

if __name__ == "__main__":
    main()