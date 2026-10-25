#! /usr/bin/python3

# ------------------------------------------------------------
# Name: Sabrina Akter
# Course: HSC 4933 - Introduction to Biocomputing
# Assignment: VCF Variant Subset
# Date: October 24, 2026
#
# Description:
# This program reads a VCF file and a list of chromosome
# coordinates. It creates a new VCF file containing only the
# variants whose chromosome and position are included in the
# coordinate list. The original VCF header and format are
# preserved in the output file.
# ------------------------------------------------------------

import sys
import gzip

if len(sys.argv) < 4:
    print('Usage: vcf_variant_subset.py infile.vcf.gz variantlist.txt outfile.vcf')
    sys.exit()
else:
    InfileName = sys.argv[1]
    ListName = sys.argv[2]
    OutfileName = sys.argv[3]


# Read chromosome and position coordinates
VariantList = open(ListName, 'r')

Coordinates = []

for Line in VariantList:
    Line = Line.strip()

    if Line == '':
        continue

    Columns = Line.split()
    Chr = Columns[0]
    Pos = Columns[1]

    Coordinates.append((Chr, Pos))

VariantList.close()


# Open the VCF file
if InfileName.endswith('.gz'):
    Infile = gzip.open(InfileName, 'rt')
else:
    Infile = open(InfileName, 'r')

Outfile = open(OutfileName, 'w')

VariantNumber = 0


# Read the VCF file
for Line in Infile:

    # Keep VCF meta-information and header lines
    if Line[0] == '#':
        Outfile.write(Line)
        continue

    Columns = Line.strip('\n').split('\t')

    Chr = Columns[0]
    Pos = Columns[1]

    # Write variants found in the coordinate list
    if (Chr, Pos) in Coordinates:
        Outfile.write(Line)
        VariantNumber += 1


Infile.close()
Outfile.close()

print('Variants written:', VariantNumber)