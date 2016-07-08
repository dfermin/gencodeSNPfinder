#!/usr/bin/python

## Date: 2016.Jul.07

"""
Script takes in an dbSNP identifier (or a file of them) and returns the closest genes to them.
User can specify maximum search space (ex: 1MB or 2MB).
User can provide either a single value or a file with one dbSNP id per row.
"""

import argparse ## for parsing command line options
import sys
import sqlite3 as lite

##---------------------------------------------------------------------------------------------------------------------
class Gene :
    def __init__(self, gid, start, end, strand, chrom, gene_name, gene_type):
        self.id = gid
        self.start = start
        self.end = end
        self.strand = strand
        self.chrom = chrom
        self.distance = None
        self.targetSNP = None
        self.snpPos = None
        self.geneName = gene_name
        self.geneType = gene_type


    def record_distance(self, pos, rsid):
        rel2start = abs((pos - self.start))
        rel2end   = abs((pos - self.end))
        self.distance = min(rel2end, rel2start)
        self.targetSNP = rsid
        self.snpPos = pos

    def print_coord(self):
        print "%s\t%s:%d\t%d\t%s\t%s\t%s\t%s:%d-%d,%d" % \
              (self.targetSNP, self.chrom, self.snpPos, self.distance, self.id, self.geneName, self.geneType, self.chrom, self.start, self.end, self.strand, )

##----------------------------------------------------------------------------------------------------------------------


########################################################################################################################
## Begin Functions
########################################################################################################################
def fetchGenes(g_cur, s_cur, rsid):
    """
    Function searches for this rsID's coordinates in the SQLite database
    :param g_cur: gene DB cursor
    :param s_cur: SNP DB cursor
    :param rsid: dbSNP id to fetch
    :return:
    """
    global FLANK ## access to the global variable FLANK
    global topN  ## access to global variable topN

    ## get chromosomal coordinates for this ID
    x = rsid[2:]
    q = "SELECT * FROM dbSNP WHERE dbId = " + x
    s_cur.execute(q)

    rows = s_cur.fetchone()
    chrom = "chr" + rows[0]
    pos   = rows[1]
    rows = None

    a = int(pos - FLANK)
    b = int(pos + FLANK)


    q = "SELECT * FROM " + chrom + \
        " WHERE start >= " + str(a) + \
        " AND end <= " + str(b) + \
        " ORDER BY MIN( ABS(start - " + str(pos) + "), ABS(end - " + str(pos) + ") ) " + \
        " LIMIT " + topN
    g_cur.execute(q)
    rows = g_cur.fetchall()

    if(len(rows) > 0): ## this means you got at least 1 gene
        ret = list()
        for r in rows:
            g = Gene(r[3], r[0], r[1], r[2], chrom, r[4], r[5])
            g.record_distance(pos, rsid)
            ret.append(g)
        return ret
    else:
        return None


########################################################################################################################
## End Functions
########################################################################################################################

## Define the commandline arguemnt parser fields
parser = argparse.ArgumentParser()
parser.add_argument("--geneDB", help="path to the GENE sqlite3 database file you want to use")
parser.add_argument("--snpDB", help="path to sqlite3 file of the human dbSNP database to use")
parser.add_argument("--id", help="rsID for SNP you want to look for")
parser.add_argument("--topN", help="limit the number of genes returned to 'topN', default = 100000")
parser.add_argument("--flank", help="search space around SNP position in NTs, default = 1000000", type=int)

args = parser.parse_args()

topN = '100000' ## top number of genes to return from SQLITE query
if args.topN: topN = args.topN;

FLANK = int(1e6/2.0) ## how much to flank the SNP sequence by on either side, default +/- 0.5Mb
if args.flank:
    FLANK = float(args.flank) / 2.0
    FLANK = int(FLANK)


if args.geneDB is None:
    sys.stderr.write("\nUSAGE: python gencodeSNPfinder.py -h\n\n")
    sys.exit(0)

if args.snpDB is None:
    sys.stderr.write("\nUSAGE: python gencodeSNPfinder.py -h\n\n")
    sys.exit(0)

if args.id is None:
    sys.stderr.write("\nUSAGE: python gencodeSNPfinder.py -h\n\n")
    sys.exit(0)



## connect to local sqlite database file
con = None
try:

    gene_con = lite.connect(args.geneDB)
    gene_cur = gene_con.cursor()
    sys.stderr.write("Connecting to SQLite3 db: %s\n" % args.geneDB)

    snp_con = lite.connect(args.snpDB)
    snp_cur = snp_con.cursor()
    sys.stderr.write("Connecting to SQLite3 db: %s\n" % args.snpDB)

except lite.Error, e:
    print "Error %s: " % e.args[0]
    sys.exit(0)


## report command line options to user
sys.stderr.write("dbSNP id:    " + args.id + "\n")
sys.stderr.write("FLANK: (+/-) " + str(FLANK) + " NT\n")
sys.stderr.write("topN:        " + topN + "\n\n")

geneList = fetchGenes(gene_cur, snp_cur, args.id)

if geneList is None:
    sys.stderr.write("No genes found with given parameters\n")
else:
    print "rsID\tSNP_pos\tdelta_NT\tensgID\tgeneSymbol\tgeneType\tgene_coord (chr:start-end,strand)"  ## header line
    for g in geneList:
        g.print_coord()


gene_con.close()
snp_con.close()


