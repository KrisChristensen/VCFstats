##########################################################
### Import Necessary Modules

import argparse                        #provides options at the command line
import sys                             #take command line arguments and uses it in the script
import gzip                            #allows gzipped files to be read
import re                              #allows regular expressions to be used

##########################################################
### Command-line Arguments

parser = argparse.ArgumentParser(description="A script to identify some statistics about the vcf file")
parser.add_argument("-vcf", help = "A vcf file", default=sys.stdin, required=True)
parser.add_argument("-depth", help = "The position of the DP character in the vcf file, default = 3", default=3)
args = parser.parse_args()

#########################################################
### Variables
class Variables():
    individuals_het = {}
    individuals_hom_ref = {}
    individuals_hom_alt = {}
    individuals_mis = {}
    individuals_dep = {}


class OpenFile():
    def __init__ (self, f, typ, fnum):
        """Opens a file (gzipped) accepted"""
        if re.search(".gz$", f):
            self.filename = gzip.open(f, 'rb')
        else:
            self.filename = open(f, 'r')
        if typ == "vcf":
            if int(fnum) == 1:
                sys.stderr.write("\n\tOpened vcf file: {}\n\n".format(f))
            OpenVCF(self.filename,fnum)

class OpenVCF():
    def __init__ (self, f, fnum):
        self.open_vcf = f
        for line in self.open_vcf:
            line = line.rstrip('\n')   
            if not re.search("^#", line):  
                self.chrom, self.pos, self.id, self.ref, self.alt, self.qual, self.filter, self.info, self.format = line.split("\t")[0:9]
		self.individuals = line.split("\t")[9:]
                for self.index, self.individual in enumerate(self.individuals):
                    self.genotype = self.individual.split(":")[0]
                    self.depth = self.individual.split(":")[int(args.depth) - 1]
                    if self.genotype == "./.":
                        if self.individuals_names[int(self.index)] in Variables.individuals_mis:
                            Variables.individuals_mis[self.individuals_names[int(self.index)]] += 1
                        else:
                            Variables.individuals_mis[self.individuals_names[int(self.index)]] = 1
                    elif self.genotype == "0/0" or self.genotype == "0/1" or self.genotype =="1/0" or self.genotype == "1/1":
                        if self.genotype == "0/0":
                            if self.individuals_names[int(self.index)] in Variables.individuals_hom_ref:
                                Variables.individuals_hom_ref[self.individuals_names[int(self.index)]] += 1
                            else:
                                Variables.individuals_hom_ref[self.individuals_names[int(self.index)]] = 1
                        elif self.genotype == "0/1" or self.genotype =="1/0":
                            if self.individuals_names[int(self.index)] in Variables.individuals_het:
                                Variables.individuals_het[self.individuals_names[int(self.index)]] += 1
                            else:
                                Variables.individuals_het[self.individuals_names[int(self.index)]] = 1
                        elif self.genotype == "1/1":
                            if self.individuals_names[int(self.index)] in Variables.individuals_hom_alt:
                                Variables.individuals_hom_alt[self.individuals_names[int(self.index)]] += 1
                            else:
                                Variables.individuals_hom_alt[self.individuals_names[int(self.index)]] = 1
                        if self.individuals_names[int(self.index)] in Variables.individuals_dep:
                            Variables.individuals_dep[self.individuals_names[int(self.index)]] += int(self.depth)
                        else:
                            Variables.individuals_dep[self.individuals_names[int(self.index)]] = int(self.depth)
                    else:
                        sys.stderr.write("\tWarning, found a non-canonical genotype: {}".format(self.genotype))
            elif re.search("^#CHROM", line):
                self.individuals_names = line.split("\t")[9:]
        print ("{}\t{}\t{}\t{}\t{}\t{}".format("#Individual","Missing", "HomRef", "Het", "HomAlt", "AvgDep"))
        for self.ind in self.individuals_names:
            self.homR = 0
            self.het = 0
            self.homA = 0
            self.mis = 0
            self.dep = "NA"
            if self.ind in Variables.individuals_hom_ref:
                self.homR = int(Variables.individuals_hom_ref[self.ind])
            if self.ind in Variables.individuals_het:
                self.het = int(Variables.individuals_het[self.ind])
            if self.ind in Variables.individuals_hom_alt:
                self.homA = int(Variables.individuals_hom_alt[self.ind])
            if self.ind in Variables.individuals_mis:
                self.mis = int(Variables.individuals_mis[self.ind])
            if self.ind in Variables.individuals_dep and self.homR + self.het + self.homA > 0:
                self.dep = float(Variables.individuals_dep[self.ind])/(self.homR + self.het + self.homA)
            print("{}\t{}\t{}\t{}\t{}\t{}".format(self.ind, self.mis, self.homR, self.het, self.homA, self.dep))
        self.open_vcf.close()

if __name__ == '__main__':
    Variables()
    open_vcf = OpenFile(args.vcf, "vcf", 1)
