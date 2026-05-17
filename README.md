# GO Enrichment 

Clone the repository:

```bash
git clone https://github.com/satyanarayan-rao/CBB-Projects
```

Navigate to the `gene_ontology` folder.

From the README, complete all installations and set up the environment. Also download the human genome dataset from the link provided and extract it.

## Objective
To map a gene to its biological function.

The aim is to find:
- Which genes are regulated by a transcription factor (`NRF1`)

This is done by:
- Checking whether the `NRF1` binding motif exists in gene promoters.

After identifying those genes, the next step is:
- Determining which biological processes are enriched in those genes.

This process is known as GO enrichment.

# Task 1

To begin, a standard format (`.bed`) file is required.

## Creating `.bed` from `.tsv` 

1. Extract `human_gene_annotation.tsv.gz`.

2. After extraction, filter the dataset to keep only those rows which contain desired chromosomes in the `chromosome_name` column of `human_gene_annotation.tsv`.

   There may be chromosomes such as `MT`, `KI270711.1`, etc. which are not required.

   A dictionary is used for `chromosome_name` filtering because its average lookup complexity is `O(1)`.

   This filtering step must be performed using a Python script which takes input from `stdin` (terminal input) and prints only those rows which contain the desired chromosomes. Direct this output to a TSV file.

```bash
cat human_gene_annotation.tsv | python filter.py > filtered.tsv
```

The reason for using terminal input instead of something like pandas is that pandas loads the complete file into memory before processing, whereas this approach processes the file line by line.

3. After filtering, convert the filtered dataset into a BED file with the columns specified in the README section of CBB-Projects\gene_onotology_analysis

This transformation step can be performed as follows:

Read `filtered.tsv` from `stdin`, transform the columns into the required BED format, store them in a list, and print the contents separated by `\t`. Direct this output to a file named `output.bed`.

### Columns of the BED file

- **Col1:** Chromosome name  
- **Col2:** Transcription Start Site (TSS)  
- **Col3:** Col2 + 1  
- **Col4:** Col1@Col2-Col3|geneName  
- **Col5:** "." (placeholder for score)  
- **Col6:** Strand (`+` if strand value is `1`, `-` if strand value is `-1` in `human_gene_annotation.tsv`)  

```bash
cat filtered.tsv | python transform.py > output.bed
```

# Task 2

After generating the BED file, the next step is to extend the coordinates (`Col2` or `Col3`) by 500 bases in a strand-aware manner.

Install `bedtools` and refer to the `bedtools slop` command.

After installation, run:

```bash
wget https://hgdownload.soe.ucsc.edu/goldenpath/hg38/bigZips/hg38.chrom.sizes
```

This file is required to prevent coordinate overflow or underflow while extending regions.

Run the following command 

```bash
bedtools slop -l 500 -r 0 -s -g hg38.chrom.sizes < input.bed > output.bed
```

The next step is to obtain promoter sequences using `bedtools getfasta`.

Run the following command:

```bash
bedtools getfasta -fi hg38.fa -bed output.bed -fo promoterSeq.fa -name
```

After obtaining the promoter sequences, use `dreg` to perform regex searching.

```bash
dreg -sequence promoterSeq.fa -pattern "GCGC..GCGC" -outfile dreg_hits.txt
```

This command was taking too long to run on my system so I was not able to complete the visualisation part after this part

## Files

- `filter.py`  
  Filters the dataset to retain only the required chromosomes.

- `transform.py`  
  Converts the filtered TSV dataset into BED format.

- `filtered.tsv`  
  Contains the filtered dataset after chromosome selection.

- `input.bed`  
  BED file generated after transformation.

- `output.bed`  
  BED file containing extended promoter coordinates.

- `hg38.chrom.sizes`  
  Contains chromosome size information required by `bedtools slop`.

- `promoterSeq.fa`  
  FASTA file containing promoter sequences extracted using `bedtools getfasta`.

- `dreg_hits.txt`  
  Stores motif matches obtained using `dreg`.
