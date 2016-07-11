
snpFlyBy <- function(snpID, topN=10000, flank=1000000) {
  ## Function retrieves data from the snpFinder website interface
  ## snpID = dbSNP identifier (must start with 'rs')
  ## topN = return only the 'topN' closests genes to the SNP locus
  ## flank = search for genes in a window of 'flank' NTs. SNP locus is the middle of this length
  
  ## Do not mess with this base_url
  ##------------------------------------------------------------------
  base_url='http://glom.sph.umich.edu/snpFinder/snpFinderSite.php?'
  ##------------------------------------------------------------------
  
  ## this just makes sure the SNPID starts with 'rs'
  if( !any(grep("^rs", snpID)) ) { snpID <- paste0('rs',snpID) }
  
  topN <- format(topN, scientific=FALSE) ## correctly format topN
  flank <- format(flank, scientific=FALSE) ## correctly format topN
  
  ## construct the URL we will actually fetch
  fetch_string = paste0(
    base_url,
    'snpID=',snpID,'&',
    'topN=',topN,'&',
    'flank=',flank)
  
  ret <- data.table::fread(
    input=fetch_string,
    sep="\t",
    stringsAsFactors=FALSE,
    drop=8 ## drop the '<br/>' HTML tag from the end of the fetched data
  )
  
  return(ret)
}



