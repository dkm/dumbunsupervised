#!/usr/bin/env python3
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Copyright 2019
# Marc Poulhies <dkm@kataplop.net>

import argparse
import sys
import json
import random
import nltk

parser = argparse.ArgumentParser()

parser.add_argument("-l", "--learn",
                    help="learn from input", action="store_true")

parser.add_argument("--poem",  help="automatic poem ", type=str)

parser.add_argument("-i", "--input", type=str,
                    help="input text")

parser.add_argument("--lowcase", action="store_true",
                    help="lowcase everything")

parser.add_argument("-b", "--brain-data", type=str,
                    help="brain data as json")

parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()

def tokenizer(file):
    for l in fin.readlines():
        for w in nltk.word_tokenize(l):
            if args.lowcase:
                w = w.lower()
            yield w

try:
    bdata = json.load(open(args.brain_data, "r"))
    if args.verbose:
        print("Using data: {}".format(len(bdata)))
except:
    if args.verbose:
        print("Using empty data")
    bdata = {}

    
if args.learn:
    if args.verbose:
        print("Learn mode")
    with open(args.input, "r") as fin:
        prev=None
        for w in tokenizer(fin):
            if prev:
                prev_guesses = bdata.get(prev, [])
                bdata[prev] = prev_guesses + [w]

            prev = w
    json.dump(bdata, open(args.brain_data, "w"))
elif args.poem:
    w = args.poem

    print (w)
    while w:
        try:
            next = random.choice(bdata.get(w, []))
            print (next, end=' ')
            w = next
        except:
            print()
            break
else:
    if args.verbose:
        print("Guess mode")
    with open(args.input, "r") as fin:
        prev=None
        for w in tokenizer(fin):
            if bdata.get(w, None):
                guess = random.choice(bdata[w])
            else:
                guess = None
            print("{} [{}]".format(w, guess), end='')

