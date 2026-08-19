"""
extract_faces.py

Extracts face crops from FF++ / Celeb-DF videos for deepfake detection training. 
Samples N frames per video, detects the highest-confidence face, crops it with margin, 
resizes to a fixed size, and saves it as a JPG.
Also appends a row to manifest.csv for every crop, so we end up with one file mapping 
every image back to its label, method, and source video.

Run this once per category folder (real and fake, separately) -- see the example
commands at the bottom of this file.

Requirements:
    pip install -r requirements.txt

Usage:
    python extract_faces.py --input /path.to/original_sequences/youtuve \
        --output ./extracted_faces --label 0 --method youtube --dataset ffpp
"""

