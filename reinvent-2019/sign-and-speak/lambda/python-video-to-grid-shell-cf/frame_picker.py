#!/usr/bin/env python3

import argparse
import sys
import glob
from math import ceil


def total_frame_count(dir):
    """
    Returns the number of frames found in a directory.
    """
    frame_files = glob.glob("{}/frame_*.png".format(dir))
    num_files = len(frame_files)
    return num_files


def choose_frames(dir):
    """
    Picks n evenly spaced frames from m frames.
    Returns indices of chosen frames.
    """
    NUM_GRID_FRAMES = 9
    total_frames = total_frame_count(dir)
    grid_frame_indices = []
    for index in range(1, NUM_GRID_FRAMES + 1):
        grid_frame_indices.append(int(ceil(index * total_frames / NUM_GRID_FRAMES)))
    # Format as a string which can be easily parsed by a bash script
    indices = "|".join(str(item) for item in grid_frame_indices)
    return str(indices)


if __name__ == "__main__":
    # Parse input
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", help="directory containing the video frames")
    args = parser.parse_args()
    frame_indices = choose_frames(args.dir)
    sys.exit(frame_indices)
