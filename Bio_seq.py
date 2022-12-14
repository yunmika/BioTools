#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Email       :   h2624366594@163.com
@Author      :   Fuchuan Han 
@Time        :   2022/12/07 15:51:53
"""

from Bio import SeqIO
import argparse
import time

def Argparse():
    '''
    Adding parameters
    '''
    parser = argparse.ArgumentParser(description='Obtain fasta and pep from genbank')
    parser.add_argument('-g', '--genbank', help='Please input the genbank file', type=str, required=True)
    parser.add_argument('-f', '--faa', help='output file of fasta', type=str, required=False)
    parser.add_argument('-p', '--pep', help='output file of pep', type=str, required=False)
    parser.add_argument('-c', '--cds', help='output file of cds', type=str, required=False)
    return parser.parse_args()

def Gb2Fasta(output_faa):
    '''
    obtain fasta from genbank file
    '''
    for seq_record in SeqIO.parse(args.genbank, 'genbank'):
        output_faa.write(">{}\n{}\n".format(seq_record.id, seq_record.seq))

def Gb2Pep(output_pep):
    '''
    obtain Amino acid from genbank file
    '''
    for seq_record in SeqIO.parse(args.genbank, 'genbank'):
        for seq_feature in seq_record.features:
            if seq_feature.type == "CDS" :
                assert len(seq_feature.qualifiers['translation']) == 1
                output_pep.write(">{}\n{}\n".format(seq_feature.qualifiers['gene'][0], seq_feature.qualifiers['translation'][0]))

def Gb2cds(output_cds):
    '''
    obtain cds from genbank file
    '''
    geneNM = []
    for seq_record in SeqIO.parse(args.genbank, 'genbank'):
        for seq_feature in seq_record.features:

            if seq_feature.type == 'CDS':
                if 'gene' in seq_feature.qualifiers:
                    if seq_feature.qualifiers['gene'][0] not in geneNM:
                        output_cds.write(">{}\n".format(seq_feature.qualifiers['gene'][0]))
                        geneNM.append(seq_feature.qualifiers['gene'][0])
                        for n, seq_location in enumerate(seq_feature.location.parts):
                            if n != len(seq_feature.location.parts)-1:
                                if seq_location.strand == 1:
                                    output_cds.write("{}".format(seq_record.seq[seq_location.start:seq_location.end]))
                                else:
                                    output_cds.write("{}".format(seq_record.seq[seq_location.start:seq_location.end].reverse_complement()))
                            else:
                                if seq_location.strand == 1:
                                    output_cds.write("{}\n".format(seq_record.seq[seq_location.start:seq_location.end]))
                                else:
                                    output_cds.write("{}\n".format(seq_record.seq[seq_location.start:seq_location.end].reverse_complement()))

                    else:
                        output_cds.write(">{}_copy\n".format(seq_feature.qualifiers['gene'][0]))
                        for n, seq_location in enumerate(seq_feature.location.parts):
                            if n != len(seq_feature.location.parts)-1:
                                if seq_location.strand == 1:
                                    output_cds.write("{}".format(seq_record.seq[seq_location.start:seq_location.end]))
                                else:
                                    output_cds.write("{}".format(seq_record.seq[seq_location.start:seq_location.end].reverse_complement()))
                            else:
                                if seq_location.strand == 1:
                                    output_cds.write("{}\n".format(seq_record.seq[seq_location.start:seq_location.end]))
                                else:
                                    output_cds.write("{}\n".format(seq_record.seq[seq_location.start:seq_location.end].reverse_complement()))


if __name__ == "__main__":
    args = Argparse()
    # start_time = time.time()
    # print("\033[1;32;40mWaiting...\033[0m")
    if args.faa:
        with open(args.faa, 'w') as output_faa:
            Gb2Fasta(output_faa)

    if args.pep:
        with open(args.pep, 'w') as output_pep:
            Gb2Pep(output_pep)

    if args.cds:
        with open(args.cds, 'w') as output_cds:
            Gb2cds(output_cds)

    end_time = time.time()
    # print('Took %f second' % (end_time - start_time))
