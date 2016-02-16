import json
import os
import urllib

import argparse
from progress.bar import Bar

from text2int import text2int

parser = argparse.ArgumentParser()
parser.add_argument("root_dir")
parser.add_argument("out_dir")

ARGS = parser.parse_args()

def main():
    pass