#!/usr/bin/python

"""
This script takes a GFF3 file and makes an SQLite3 Database out of it.
The database contains one table per chromosome and can be queried by coordinates.
"""

import gzip
import argparse ## for parsing command line options
import sys
import sqlite3 as lite



## Define the commandline argument parser fields
parser = argparse.ArgumentParser()
parser.add_argument("gff3", help="path to the GFF3 file you want to use")
parser.add_argument("out", help="name of output database file")

args = parser.parse_args()

con = None ## ultimately SQLite database connection

try:
    con = lite.connect(args.out) ## create database
    sys.stderr.write("Creating database file: %s\n" % args.out)
except lite.Error, e:
    print "Error %s: " % e.args[0]
    sys.exit(1)


cur = con.cursor()


chromosomes = list()

## open the file for parsing
fh = gzip.open(args.gff3, 'r')

i = 0
for line in fh:
    line = line.rstrip()

    if line[0] == '#': continue;

    data = line.split("\t")

    if data[2] != 'gene': continue; ## only record gene coordinates

    chrom  = data[0]
    start  = data[3]
    end    = data[4]
    strand = data[6]
    info   = data[8]

    if strand == '+': strand = 1;
    else: strand = -1;

    ## gene Id
    geneId = info.split(";")[0]
    geneId = geneId[3:]

    ## gene type
    gene_type = "NA"
    if 'gene_type' in info:
        for x in info.split(";"):
            if "gene_type" in x:
                gene_type = x
                f = gene_type.find('=') + 1
                gene_type = gene_type[f:]
                break

    ## gene_name
    gene_name = "NA"
    if 'gene_name' in info:
        for x in info.split(";"):
            if "gene_name" in x:
                gene_name = x
                f = gene_name.find('=') + 1
                gene_name = gene_name[f:]
                break


    ## check to see if this chromosome table is in the database
    q = "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table' AND name = '" + chrom + "' "
    cur.execute(q)
    res = int(cur.fetchone()[0])

    ## if the table doesn't exist, create it
    if res == 0:
        q = "CREATE TABLE " + chrom + "(start INT, end INT, strand INT, geneId TEXT, geneName TEXT, geneType TEXT)"
        sys.stderr.write("%s\n" % chrom)
        chromosomes.append(chrom)
        cur.execute(q)

        #q = "CREATE INDEX " + chrom + "_idx ON " + chrom + " (start)"
		#cur.execute(q)

    ## insert this record
    q = "INSERT INTO " + chrom + " VALUES(" + start + ", " + end + ", " + str(strand) + ", '" + geneId + "', '" + gene_name + "', '" + gene_type + "' )"

    #print q ## debugging
    cur.execute(q)
    con.commit()


## create indexes
for chrom in chromosomes:
    q = "CREATE INDEX " + chrom + "_idx_coord ON " + chrom + " (start, end)"
    cur.execute(q)


if con: con.close()
