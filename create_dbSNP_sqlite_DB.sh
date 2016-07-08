#!/usr/bin/sh

# Date 2016.Jul.8
## This bash script will take in a given VCF file and create an SQLite3 database
## out of it. The script is specifically for the human dbSNP database and may
## not work for other VCF files.

if [ "$#" -ne 2 ]; then
		echo -e "\nUSAGE: create_dbSNP_sqlite_DB.sh <dbSNP_VCF_file> <output_fileName>\n";
		exit
fi

vcf=$1
outF=$2

## change these based upon your operating system
ZGREP=/usr/bin/zgrep
CUT=/usr/bin/cut
SQLITE3=/usr/bin/sqlite3
SED=/usr/bin/sed
DATE=/bin/date
TMPDIR=/tmp

TS=$(/bin/date +%s) ## timestamp

## dump temporary tab-delimited file to temporary folder
$ZGREP -v '#' $vcf | $CUT -f1,2,3 | $SED -e 's|rs||g' > $TMPDIR/tmp4sqlite.$TS


## these are the sqlite3 command to create and populate the databases
echo "
CREATE TABLE dbSNP (chrom TEXT, pos INT, dbId INT); 
.mode tabs
.import $TMPDIR/tmp4sqlite.$TS dbSNP
CREATE INDEX rsid_index ON dbSNP(dbId);
" > $TMPDIR/cmds.$TS

cat /dev/null > $outF
$SQLITE3 $outF < $TMPDIR/cmds.$TS

## clean up
rm -rf $TMPDIR/*.$TS

echo "Done"


