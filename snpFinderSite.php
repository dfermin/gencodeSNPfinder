<?php

	$flank = 1000000; ## total number of NT to flank SNP position by
	$topN = 10000; ## top number of genes to return

	if( $_GET["snpID"] ) { $id = $_GET['snpID']; }
	if( $_GET["flank"] ) { $flank = $_GET['flank']; }
	if( $_GET["topN"] ) { $topN = $_GET['topN']; }


	if( strlen($id) == 0 ) {
		echo "ERROR: You must provide a dbSNP identifier. Example: rs255";
		exit();
	}

	$PYTHON='/usr/bin/python'; ## change this based upon the system you are on
	$GENEDB='genes_v19-withSymbols.db';
	$SNPDB='dbSNP_b147.db';

	## command to be executed
	$cmd = "$PYTHON gencodeSNPfinder.py --geneDB $GENEDB --snpDB $SNPDB --id $id --flank $flank --topN $topN 2>/dev/null";
	exec($cmd, $retval);
	
	foreach($retval as $line) {
			echo "$line" . "\t<br/>\n";
	}

?>
