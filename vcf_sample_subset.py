#! /usr/bin/python3

# ------------------------------------------------------------
# Name: Sabrina Akter
# Course: HSC 4933 - Introduction to Biocomputing
# Assignment: VCF Sample Subset
# Date: October 24, 2026
#
# Description:
# This program reads a VCF file and a list of sample IDs.
# It creates a new VCF file containing only the samples whose
# IDs are included in the sample list. The VCF metadata,
# required columns, and overall VCF format are preserved.
# ------------------------------------------------------------

import sys
import gzip

if len(sys.argv) < 4:
    print('Usage: vcf_sample_subset.py infile.vcf.gz samplelist.txt outfile.vcf')
    sys.exit()
else:
    InfileName = sys.argv[1]
    ListName = sys.argv[2]
    OutfileName = sys.argv[3]


# Read sample IDs
SampleFile = open(ListName, 'r')

SampleList = []

for Line in SampleFile:
    Line = Line.strip()

    if Line == '':
        continue

    SampleList.append(Line)

SampleFile.close()


# Open the VCF file
if InfileName.endswith('.gz'):
    Infile = gzip.open(InfileName, 'rt')
else:
    Infile = open(InfileName, 'r')

Outfile = open(OutfileName, 'w')

SampleColumns = []
KeepColumns = []


# Read the VCF file
for Line in Infile:

    # Keep VCF meta-information lines
    if Line.startswith('##'):
        Outfile.write(Line)
        continue

    # Process the VCF header
    if Line.startswith('#CHROM'):

        Columns = Line.strip('\n').split('\t')

        # Keep the first 9 VCF columns
        KeepColumns = list(range(9))

        # Find the requested sample columns
        for Number in range(9, len(Columns)):
            if Columns[Number] in SampleList:
                KeepColumns.append(Number)
                SampleColumns.append(Columns[Number])

        NewColumns = []

        for Number in KeepColumns:
            NewColumns.append(Columns[Number])

        Outfile.write('\t'.join(NewColumns) + '\n')
        continue

    # Process VCF variant lines
    Columns = Line.strip('\n').split('\t')

    NewColumns = []

    for Number in KeepColumns:
        NewColumns.append(Columns[Number])

    Outfile.write('\t'.join(NewColumns) + '\n')


Infile.close()
Outfile.close()

print('Samples written:', len(SampleColumns))
print('Samples:', '\t'.join(SampleColumns))