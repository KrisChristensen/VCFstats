# VCFstats
A script to identify some statistics about the vcf file for all individuals.  These include: missing genotype count, number of homozygous reference genotypes, number of heterozygous genotypes, number of homozygous alternative genotypes, and the average depth.

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#requirements">Requirements</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

<!-- requirements -->
## Requirements

This script has been tested with Python 3 and should work with compressed files.
The script requires a vcf file.  The vcf file can be compressed with gzip.  The depth field in the vcf file is required and the position of the field needs to be specified in the options.

<!-- usage -->
## Usage

Find Statistics:
python VCF.stats.v1.1.py -vcf file.vcf -depth 3 > stats.txt

To see the usage and get futher information: python VCF.stats.v1.1.py -h


<!-- license -->
## License 

Distributed under the MIT License.
