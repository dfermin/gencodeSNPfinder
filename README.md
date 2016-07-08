# gencodeSNPfinder.py 

This is a python script that, given a human dbSNP identifier, will return a list of all
the genes near to it. The script takes in a bunch of parameters, some are required and
others are optional. This README goes through how to install and use the script.


## 1. Create necessary backend files
Creating the backend database files takes the longest amount of time.
Depending upon your machine it can take **up to 1 hour** to do just this part.
However, once created, the files can be used repeatedly.

You need to create *two* files before this script will work:
1. Gene coordinate database (called *genes_v19.db* in from here on)
2. dbSNP database (called *dbSNP.db* from here on)


### 1.1 Gene coordinate database
You need to download the GENCODE **gff3** annotation file for the genome you want to use.
I used [gencode.v19.annotation.gff3.gz](ftp://ftp.sanger.ac.uk/pub/gencode/Gencode_human/release_19/gencode.v19.annotation.gff3.gz)

After you download this file use the python script called **parseGFF3intoDB.py** to make 
an SQLite3 database out of the GFF3 file:
```
python parseGFF3intoDB.py gencode.v24lift37.annotation.gff3.gz genes_v19.db
```

### 1.2 dbSNP database
You need to download the NCBI dbSNP VCF file. I used 
[All_20160601.vcf.gz](ftp://ftp.ncbi.nih.gov/snp/organisms/human_9606_b147_GRCh37p13/VCF/All_20160601.vcf.gz) 

After you download this file use the bash script called **create_dbSNP_sqlite_DB.sh** to make
an SQLite3 database out of the VCF file:
```
bash create_dbSNP_sqlite_DB.sh All_20160601.vcf.gz dbSNP.db
```


## 2. Running gencodeSNPfinder.py
At this point you now have everything you need to use the gencodeSNPfinder.py.
To get a usage statement run this command at the shell:
```
python gencodeSNPfinder.py -h
```

#### 2.1 As an example of the output, run:
```
python gencodeSNPfinder.py --geneDB genes_v19.db --snpDB dbSNP.db --id rs1799963
```

This should produce this output:

<pre>
Connecting to SQLite3 db: genes_v19.db
Connecting to SQLite3 db: dbSNP_b147.db
dbSNP id:    rs1799963
FLANK: (+/-) 500000 NT
topN:        100000

dbSNP id:    rs1799963
FLANK: (+/-) 500000 NT
topN:        100000

rsID	SNP_pos	delta_NT	ensgID	geneSymbol	geneType	gene_coord (chr:start-end,strand)
rs1799963	chr11:46761055	1	ENSG00000180210.10	F2	protein_coding	chr11:46740730-46761056,1
rs1799963	chr11:46761055	3543	ENSG00000175216.10	CKAP5	protein_coding	chr11:46764598-46867847,-1
rs1799963	chr11:46761055	13620	ENSG00000263540.1	MIR5582	miRNA	chr11:46774675-46774742,-1
rs1799963	chr11:46761055	19261	ENSG00000252427.1	SNORD67	snoRNA	chr11:46780316-46780423,-1
rs1799963	chr11:46761055	22884	ENSG00000212135.1	SNORD67	snoRNA	chr11:46783939-46784049,-1
rs1799963	chr11:46761055	33593	ENSG00000175213.2	ZNF408	protein_coding	chr11:46722368-46727462,1
rs1799963	chr11:46761055	38890	ENSG00000175220.7	ARHGAP1	protein_coding	chr11:46698630-46722165,-1
rs1799963	chr11:46761055	64687	ENSG00000175224.12	ATG13	protein_coding	chr11:46638826-46696368,1
rs1799963	chr11:46761055	106908	ENSG00000247675.2	LRP4-AS1	antisense	chr11:46867963-46895947,1
rs1799963	chr11:46761055	117364	ENSG00000134569.5	LRP4	protein_coding	chr11:46878419-46940193,-1
rs1799963	chr11:46761055	121596	ENSG00000180423.4	HARBI1	protein_coding	chr11:46624411-46639459,-1
rs1799963	chr11:46761055	145380	ENSG00000110497.10	AMBRA1	protein_coding	chr11:46417964-46615675,-1
rs1799963	chr11:46761055	197185	ENSG00000149179.9	C11orf49	protein_coding	chr11:46958240-47185936,1
rs1799963	chr11:46761055	287616	ENSG00000265014.1	MIR3160-2	miRNA	chr11:46473355-46473439,-1
rs1799963	chr11:46761055	301523	ENSG00000271350.1	CTD-2384B9.1	pseudogene	chr11:47062578-47063496,-1
rs1799963	chr11:46761055	310355	ENSG00000244313.2	RP11-425L10.1	pseudogene	chr11:46450163-46450700,-1
rs1799963	chr11:46761055	352948	ENSG00000180720.6	CHRM4	protein_coding	chr11:46406640-46408107,-1
rs1799963	chr11:46761055	355680	ENSG00000110492.11	MDK	protein_coding	chr11:46402306-46405375,1
rs1799963	chr11:46761055	358951	ENSG00000149091.11	DGKZ	protein_coding	chr11:46354455-46402104,1
rs1799963	chr11:46761055	363021	ENSG00000264102.1	MIR4688	miRNA	chr11:46397952-46398034,1
rs1799963	chr11:46761055	383600	ENSG00000255520.1	RP11-390K5.3	antisense	chr11:47144655-47152352,-1
rs1799963	chr11:46761055	418083	ENSG00000157613.6	CREB3L1	protein_coding	chr11:46299212-46342972,1
rs1799963	chr11:46761055	424793	ENSG00000149182.10	ARFGAP2	protein_coding	chr11:47185848-47198676,-1
rs1799963	chr11:46761055	428777	ENSG00000270060.1	RP11-390K5.6	sense_intronic	chr11:47189832-47191114,-1
rs1799963	chr11:46761055	438021	ENSG00000165912.11	PACSIN3	protein_coding	chr11:47199076-47207994,-1
rs1799963	chr11:46761055	451677	ENSG00000243802.2	RP11-390K5.1	pseudogene	chr11:47212732-47213093,-1
rs1799963	chr11:46761055	464957	ENSG00000255007.1	CTD-2589M5.4	antisense	chr11:46277906-46296098,-1
rs1799963	chr11:46761055	466341	ENSG00000266540.1	RN7SL772P	misc_RNA	chr11:47227396-47227672,1
rs1799963	chr11:46761055	475438	ENSG00000134574.7	DDB2	protein_coding	chr11:47236493-47260767,1
rs1799963	chr11:46761055	480714	ENSG00000256897.1	RP11-17G12.2	antisense	chr11:47241769-47243302,-1</pre>

The first 5 lines of output are STDERR information. It tells you the what database files the script used, what dbSNP ID you gave it and the flank and topN parameters that were used. Here is a description of the FLANK and topN fields:

- **FLANK**: the script will look for genes in a window that is +/- *k* nucleotides (NT) around the chromosomal position of the SNP (i.e 'f' NT *flanking* the SNP locus). The default value is 1000000.  So the SNP locus is flanked on either side by 500000 NTs. 
- **topN**: You can limit the output to just the top *N* genes. Genes are *always* sorted from closest to furthest from the SNP locus. 

#### 2.2 Example restricting the flank size to 0.5Mb (megabases)
```
python gencodeSNPfinder.py --geneDB genes_v19.db --snpDB dbSNP.db --id rs1799963 --flank 500000
```
<pre>
Connecting to SQLite3 db: genes_v19.db
Connecting to SQLite3 db: dbSNP_b147.db
dbSNP id:    rs1799963
FLANK: (+/-) 250000 NT
topN:        100000

rsID	SNP_pos	delta_NT	ensgID	geneSymbol	geneType	gene_coord (chr:start-end,strand)
rs1799963	chr11:46761055	1	ENSG00000180210.10	F2	protein_coding	chr11:46740730-46761056,1
rs1799963	chr11:46761055	3543	ENSG00000175216.10	CKAP5	protein_coding	chr11:46764598-46867847,-1
rs1799963	chr11:46761055	13620	ENSG00000263540.1	MIR5582	miRNA	chr11:46774675-46774742,-1
rs1799963	chr11:46761055	19261	ENSG00000252427.1	SNORD67	snoRNA	chr11:46780316-46780423,-1
rs1799963	chr11:46761055	22884	ENSG00000212135.1	SNORD67	snoRNA	chr11:46783939-46784049,-1
rs1799963	chr11:46761055	33593	ENSG00000175213.2	ZNF408	protein_coding	chr11:46722368-46727462,1
rs1799963	chr11:46761055	38890	ENSG00000175220.7	ARHGAP1	protein_coding	chr11:46698630-46722165,-1
rs1799963	chr11:46761055	64687	ENSG00000175224.12	ATG13	protein_coding	chr11:46638826-46696368,1
rs1799963	chr11:46761055	106908	ENSG00000247675.2	LRP4-AS1	antisense	chr11:46867963-46895947,1
rs1799963	chr11:46761055	117364	ENSG00000134569.5	LRP4	protein_coding	chr11:46878419-46940193,-1
rs1799963	chr11:46761055	121596	ENSG00000180423.4	HARBI1	protein_coding	chr11:46624411-46639459,-1
</pre>


#### 2.3 Example restricting the output to just the top 3 closest genes
```
python gencodeSNPfinder.py --geneDB genes_v19.db --snpDB dbSNP.db --id rs1799963 --topN 3
```
<pre>
Connecting to SQLite3 db: genes_v19.db
Connecting to SQLite3 db: dbSNP_b147.db
dbSNP id:    rs1799963
FLANK: (+/-) 500000 NT
topN:        3

rsID	SNP_pos	delta_NT	ensgID	geneSymbol	geneType	gene_coord (chr:start-end,strand)
rs1799963	chr11:46761055	1	ENSG00000180210.10	F2	protein_coding	chr11:46740730-46761056,1
rs1799963	chr11:46761055	3543	ENSG00000175216.10	CKAP5	protein_coding	chr11:46764598-46867847,-1
rs1799963	chr11:46761055	13620	ENSG00000263540.1	MIR5582	miRNA	chr11:46774675-46774742,-1
</pre>


## 3. Output Fields
The output of the script can be written to disk by redirection:
```
python gencodeSNPfinder.py --geneDB genes_v19.db --snpDB dbSNP.db --id rs1799963 --topN 3 > output.tab
```

The STDERR info gets printed to the screen but the rest of the data is written to a text file called 'output.tab'. The data is tab-delimited and looks like this:
<pre>
rsID	SNP_pos	delta_NT	ensgID	geneSymbol	geneType	gene_coord (chr:start-end,strand)
rs1799963	chr11:46761055	1	ENSG00000180210.10	F2	protein_coding	chr11:46740730-46761056,1
rs1799963	chr11:46761055	3543	ENSG00000175216.10	CKAP5	protein_coding	chr11:46764598-46867847,-1
rs1799963	chr11:46761055	13620	ENSG00000263540.1	MIR5582	miRNA	chr11:46774675-46774742,-1
</pre>

Here is a description of the fields generated:

<table>
<tr><th>Field</th><th>Description</th></tr>
<tr><td>rsID</td><td>This is the original rsID value you gave at the shell</td></tr>
<tr><td>SNP_pos</td><td>Genomic locus for the SNP</td></tr>
<tr><td>delta_NT</td><td>The distance of the SNP locus (in NTs) from the gene reported on this row</td></tr>
<tr><td>ensgID</td><td>ENSEMBL gene identifier</td></tr>
<tr><td>geneSymbol</td><td>HGNC Gene Symbol, 'NA' if not available</td><tr>
<tr><td>geneType</td><td>Gene classification (protein_coding, psuedo_gene, etc...)</td></tr>
<tr><td>gene_coord (chr:start-end,strand)</td><td>The genomic coordinates (and strand orientation) for the gene</td></tr>
</table>
