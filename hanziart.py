#!/usr/bin/env python3

from skimage import exposure
from skimage.transform import rescale
from skimage.color import rgb2gray
from scipy import ndimage
import numpy as np
import argparse
import csv
from random import choice
from re import match
from collections import defaultdict

parser = argparse.ArgumentParser(description="Convert image to hanziart",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i","--image",
                    help="Image to convert into text",
                    type=str, required=True)
parser.add_argument("-w","--width",
                    help="Width of output text block",
                    type=int,
                    default=80)
parser.add_argument("-l","--levels",
                    help="Levels of intensity to use, recommended < 30",
                    type=int,default=20)
parser.add_argument("-c","--color",
                    help="Color image",
                    type=bool,default=True)
parser.add_argument("-n","--negative",
                    help="Negative image",
                    action='store_true')
parser.add_argument("-o","--out",
                    help="Name of output file",
                    type=str,
                    default="hanziart_test.txt")
parser.add_argument("-d","--dict",
                    help="Path to Unihan_DictionaryLikeData.txt",
                    type=str,
                    default="./Unihan_DictionaryLikeData.txt")
parser.add_argument("-g","--gradelevel",
                    help="Use characters up to this primary school grade level (Hong Kong) only. Range 1 to 6. Other values mean use all characters.",
                    type=int, default=6)
args = parser.parse_args()

def resize_img_width(img, width: int):
    """Resize image img to desired width in pixels"""
    oldwidth = img.shape[1]
    factor = width/oldwidth
    return(rescale(img,scale=factor))

def rescale_img_int(img, maxint: int, color: bool):
    """Rescale image intensities to maxint number of levels, and convert to
    grayscale if color
    """
    img_rounded = exposure.rescale_intensity(img,out_range=(0,maxint)).round()
    if color:
        img_rounded = rgb2gray(img_rounded)
    return(img_rounded)

def load_Unihan_data(dictfile,maxgradelevel: int):
    """Load Unihan strokecount data from file and return dict of chars by
    strokecount
    """
    outdict = defaultdict(list)
    with open(dictfile) as tsvfile:
        tsvreader = csv.reader(tsvfile,delimiter="\t")
        if maxgradelevel in range(1,7): # kGradeLevel only from 1 to 6 inclusive
            # Dict of character stroke counts and grade levels
            char_grade_count_dict = defaultdict(lambda: defaultdict(int)) 
            for line in tsvreader:
                if len(line) == 3 and line[1] == "kTotalStrokes" and match("^\d+$",line[2]):
                    char_grade_count_dict[line[0]]['strokes'] = line[2]
                elif len(line) == 3 and line[1] == "kGradeLevel" and match("^\d+$",line[2]):
                    char_grade_count_dict[line[0]]['gradelevel'] = line[2]
            # Go through dictionary and report characters keyed by stroke count
            for char in char_grade_count_dict.keys():
                if int(char_grade_count_dict[char]['gradelevel']) in range(1,maxgradelevel+1):
                    # Cannot use <= maxgradelevel because undefined grade level is automatically 0
                    outdict[char_grade_count_dict[char]['strokes']].append(char)
        else: # Ignore kGradeLevel parameter
            for line in tsvreader:
                if len(line) == 3 and line[1] == "kTotalStrokes" and match("^\d+$",line[2]):
                    outdict[line[2]].append(line[0])
    return(outdict)

def make_uchr(code: str):
    """Convert Unicode code points in U+XXXXX format to character glyph"""
    # Function from https://realpython.com/python-encodings-guide/
    return chr(int(code.lstrip("U+").zfill(8),16))

def randchar(val: int, tbl: dict):
    """Return a random character from dict with a given strokecount"""
    return(make_uchr(choice(tbl[str(val)])))

def img2text(img, tbl:dict, outfile):
    """Convert image to hanziart, given dict of chars by strokecount"""
    outarr = [randchar(int(x+1),tbl) for x in img.ravel()]
    (height,width) = img.shape
    f = open(outfile, 'w')
    for i in range(1, height):
        first = width * (i-1)
        last = width * i - 1
        f.write("".join(outarr[first:last]))
        f.write("\n")
    f.close

# main #

# Read image from file
print(" ".join(["... Reading image from file",args.image]))
img = ndimage.imread(args.image)
if (args.negative):
    img = np.invert(img)
# Read Unihan table and key by strokecount
print(" ".join(["... Loading Unihan data from file",args.dict]))
strokedict = load_Unihan_data(args.dict,args.gradelevel)
# Rescale intensity to maximize dynamic range
img = exposure.rescale_intensity(img)
# Resize and rescale image
if args.levels > 42:
    print("... WARNING: --levels value above 42, using levels=42 instead")
    args.levels = 42
imgsmall = rescale_img_int(resize_img_width(img,args.width),args.levels,args.color)
# Convert image to hanziart
print(" ".join(["... Writing output to file",args.out]))
img2text(imgsmall,strokedict,args.out)
