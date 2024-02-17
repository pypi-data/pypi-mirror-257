import csv
import os
import re
from collections import Counter
from itertools import permutations

from common import BAD_GENOTYPES
from utils import assign_activity, assign_phenotype, determine_copy_number


class CYP2D6Data:
    def __init__(
        self,
        genotypes_raw=None,
        cyrius_filter=None,
        sample_id=None,
        stellarpgx_flag=None,
        mask_retired_alleles=True,
        caller=None,
    ):
        self.sample_id = sample_id
        self.cyrius_filter = cyrius_filter
        self.caller = caller
        self.stellarpgx_flag = stellarpgx_flag
        self.genotype_data = CYP2D6Genotype(
            genotypes_raw=genotypes_raw,
            stellarpgx_flag=stellarpgx_flag,
            mask_retired_alleles=mask_retired_alleles,
            caller=caller,
        )
        self.phenotype_data = CYP2D6Phenotype(
            self.genotype_data.genotype, self.genotype_data.possible_genotype
        )
        self.cn = determine_copy_number(self.genotype_data.genotype)

    @classmethod
    def from_cyrius(cls, file, mask_retired_alleles=True):
        caller = "Cyrius"
        with open(file) as f:
            csv_reader = csv.reader(f, delimiter="\t")
            for i, line in enumerate(csv_reader):
                if i == 1:
                    sample_id = line[0]
                    cyrius_filter = line[2]
                    genotypes_raw = line[1].split(";")
        return cls(
            sample_id=sample_id,
            caller=caller,
            cyrius_filter=cyrius_filter,
            genotypes_raw=genotypes_raw,
            mask_retired_alleles=mask_retired_alleles,
        )

    @classmethod
    def from_aldy(cls, file, sample_id=None, mask_retired_alleles=True):
        caller = "Aldy"
        with open(file) as f:
            if sample_id is None:
                sample_id = os.path.basename(file)
            csv_reader = csv.reader(f, delimiter="\t")
            genotypes_raw = set()
            for line in csv_reader:
                if line[0] == sample_id:
                    genotype = line[3]
                    genotypes_raw.add(genotype)
        if os.path.getsize(file) == 0:
            # Couldn't call the sample
            genotypes_raw = {"Indeterminate/Indeterminate"}
        elif len(genotypes_raw) == 0:
            # https://github.com/0xTCG/aldy/issues/45#issuecomment-1368169564
            genotypes_raw = {"*5/*5"}
        return cls(
            sample_id=sample_id,
            caller=caller,
            genotypes_raw=list(genotypes_raw),
            mask_retired_alleles=mask_retired_alleles,
        )

    @classmethod
    def from_pypgx(cls, file, sample_id=None, mask_retired_alleles=True):
        caller = "PyPGx"
        if sample_id is None:
            sample_id = file
        with open(file) as f:
            csv_reader = csv.reader(f, delimiter="\t")
            for i, line in enumerate(csv_reader):
                if i == 1:
                    genotype_raw = line[1]
        return cls(
            sample_id=sample_id,
            caller=caller,
            genotypes_raw=[genotype_raw],
            mask_retired_alleles=mask_retired_alleles,
        )

    @classmethod
    def from_stargazer(cls, file, mask_retired_alleles=True):
        caller = "Stargazer"
        pass

    @classmethod
    def from_stellarpgx(cls, file, sample_id=None, mask_retired_alleles=True):
        caller = "StellarPGx"
        stellarpgx_flag = None
        if sample_id is None:
            sample_id = file
        with open(file) as f:
            csv_reader = csv.reader(f)
            next_line = False
            next_line_background = False
            for line in csv_reader:
                if next_line:
                    genotype_raw = line
                    next_line = False
                elif next_line_background:
                    possible_genotypes = [genotype.strip("[]") for genotype in line]
                    break
                elif len(line) == 0:
                    continue
                elif line[0] == "Result:":
                    next_line = True
                elif "CN" in line[0]:
                    cn = int(line[0].split("= ")[-1])
                elif line[0] == "Likely background alleles:":
                    next_line_background = True
        if re.search(r"\d or", genotype_raw[0]) is not None:
            genotype_new = (
                genotype_raw[0].replace("Duplication present", "").strip().split(" or ")
            )
            if "Duplication" in genotype_raw[0]:
                genotype_raw = [genotype + "xN" for genotype in genotype_new]
            else:
                genotype_raw = genotype_new
        elif "Possible" not in genotype_raw[0]:
            stellarpgx_flag = None
        elif cn in {0, 1, 2}:
            genotype_raw = possible_genotypes
            stellarpgx_flag = "Novel flag"
        else:
            genotype_raw = possible_genotypes
            stellarpgx_flag = "Novel flag with CN"
        return cls(
            sample_id=sample_id,
            caller=caller,
            genotypes_raw=genotype_raw,
            stellarpgx_flag=stellarpgx_flag,
            mask_retired_alleles=mask_retired_alleles,
        )


class CYP2D6Genotype:
    # Parsing and reporting of CYP2D6 genotype calls will be made according to PharmVar reccommendations
    # See Table 2 https://pubmed.ncbi.nlm.nih.gov/37669183/

    def __init__(
        self,
        genotypes_raw=None,
        stellarpgx_flag=None,
        mask_retired_alleles=True,
        caller=None,
    ):
        self.genotypes_raw = genotypes_raw
        self.stellarpgx_flag = stellarpgx_flag
        self.mask_retired_alleles = mask_retired_alleles
        self.caller = caller
        self._haplotypes = []
        self.parse_genotypes()

    @staticmethod
    def convert_retired_alleles(genotype):
        # Some tools still report old structural variants
        # https://a.storyblok.com/f/70677/x/45cd028f4f/cyp2d6_structural-variation_v2-4.pdf
        genotype = re.sub(r"\*(16|66|67|76|77|78|79|80)(?!\d)", "*13", genotype)
        genotype = genotype.replace("*57", "*36")
        return genotype

    @staticmethod
    def determine_haplotype_order(haplotype):
        # Haplotypes are now correctly grouped but need to correct the order
        # I.e *10x2+*36 -> *36+*10x2

        alleles = [allele[1] for allele in haplotype]
        special_variants = [13, 36, 61, 63, 68, 83, 90]
        if any(spec_var in alleles for spec_var in special_variants):
            # Index 2 refers to the allele index which determines order
            return sorted(haplotype, key=lambda x: x[2])
        # Index 1 refers to allele number. I.e 10
        # Ex: *1+*10+*2/*27+*2 -> *1+*2+*10/*2+*27
        return sorted(haplotype, key=lambda x: x[1])

    @staticmethod
    def get_allele_index(allele):
        # This is an odd index order, but needed to get the alleles in correct order
        # as defined by the pharmvar table
        # General guideline is that structural variants come first followed by regular alleles
        # I.e *68+*4 or *13+*1
        # Structural variants: *13, *61, *63, *68
        allele_index_order = {
            "*36": 0,
            "*10": 2,
            "*13": 0,
            "*68": 1,
            "*4": 2,
            "*2": 3,
            "*1": 3,
            "*90": 4,
            "*83": 4,
            "*63": 1,
            "*61": 1,
        }
        try:
            return allele_index_order[allele]
        except KeyError:
            # Remaining alleles will be sorted according to the allele number
            # After the above alleles
            return int(allele.replace("*", "")) + 5

    @staticmethod
    def parse_haplotypes(genotype):
        haplotypes = []
        for haplotype in genotype.split("/"):
            haplotype = CYP2D6Genotype.parse_haplotype(haplotype)
            haplotypes.append(haplotype)
        return haplotypes

    @staticmethod
    def decouple_alleles(haplotype):
        # Callers can report alleles with total copies I.e *68x2
        # Need to split these up into individual components for indexing
        # I.e *68x2+4 -> [*68, *68, *4]
        alleles = []
        for allele in haplotype.split("+"):
            if "x" in allele:
                copies = int(re.findall(r"(?<=x)\d+", allele)[0])
                allele = re.findall(r"\*\d+", allele)[0]
                alleles.extend([allele] * copies)
            else:
                alleles.append(allele)
        return alleles

    @staticmethod
    def parse_haplotype(haplotype):
        if "+" in haplotype:
            # Groups same alleles within a haplotype together
            # Order within the haplotype is corrected in the next step
            # I.e *10+*10+*36 -> *10x2+*36
            alleles = CYP2D6Genotype.decouple_alleles(haplotype)

            allele_counts = Counter(alleles)

            # List of tuples (allele_string, allele, allele_index)
            # Allele string includes copies if > 1
            haplotype_new = []
            for allele, count in allele_counts.items():
                allele_index = CYP2D6Genotype.get_allele_index(allele)
                allele_num = int(allele.replace("*", ""))
                if count == 1:
                    haplotype_new.append((allele, allele_num, allele_index))
                else:
                    haplotype_new.append(
                        (f"{allele}x{count}", allele_num, allele_index)
                    )
            if len(haplotype_new) != 1:
                haplotype_ordered = CYP2D6Genotype.determine_haplotype_order(
                    haplotype_new
                )
                haps = [hap[0] for hap in haplotype_ordered]
                haplotype = "+".join(haps)
            else:
                haplotype = haplotype_new[0][0]
        return haplotype

    def adjust_xn_genotypes(self, genotypes_raw):
        genotypes_new = set()
        for genotype in genotypes_raw:
            if "xN" in genotype:
                self.stellarpgx_flag = "Allele Copies Unknown"
                genotypes_raw = ["Indeterminate/Indeterminate"]
                break
        return genotypes_raw

    def parse_genotypes(self):
        genotypes_raw = self.genotypes_raw
        genotypes_raw = self.adjust_xn_genotypes(genotypes_raw)
        genotypes = set()
        if self.caller == "Cyrius":
            genotypes_raw = self.adjust_cyrius_slash_genotype(genotypes_raw)
        for genotype in genotypes_raw:
            if self.mask_retired_alleles:
                genotype = self.convert_retired_alleles(genotype)
            if self.caller in {"Aldy", "Cyrius"} and genotype not in BAD_GENOTYPES:
                genotype = self.remove_subs(genotype)

            genotype = self.parse_genotype(genotype)
            genotypes.add(genotype)
        if len(genotypes) == 1:
            self.genotype = next(iter(genotypes))
            if (
                genotype == "Indeterminate/Indeterminate"
                and genotypes_raw[0] not in BAD_GENOTYPES
                and self.stellarpgx_flag is None
            ):
                self.possible_genotype = ";".join(genotypes_raw)
            else:
                self.possible_genotype = None
        else:
            self.genotype = "Indeterminate/Indeterminate"
            self.possible_genotype = ";".join(sorted(list(genotypes)))

    def parse_genotype(self, genotype):
        if (
            genotype in BAD_GENOTYPES
            or genotype is None
            or (self.stellarpgx_flag is not None and "CN" in self.stellarpgx_flag)
        ):
            # Copy number state from stellarpgx of each allele cannot be determined
            self._haplotypes.append(["Indeterminate", "Indeterminate"])
            return "Indeterminate/Indeterminate"
        haplotypes = self.parse_haplotypes(genotype)
        self._haplotypes.append(haplotypes)

        idx1, idx2 = self.determine_genotype_order(haplotypes)
        genotype = f"{haplotypes[idx1]}/{haplotypes[idx2]}"
        return genotype

    @staticmethod
    def adjust_cyrius_slash_genotype(genotypes_raw):
        # This will create way more genotypes than needed because of order
        # All will be fixed later when ordering the haplotypes and genotypes
        # Generally no genotype can be reported from this because haplotypes
        # cannot be determined. However, possible activity score and phenotypes
        # can be reflective of the CYP2D6 function because usually the alleles have
        # been identified, just not the haplotype configuration
        genotypes_raw_fixed = set()
        for genotype in genotypes_raw:
            if "_" in genotype:
                # Ex. *1_*1_*13 -> *1/*1+*13 or *1+*1/*13
                # Ex. *1_*4_*4.013_*68 -> *1/*68+*4+*4 or *1+*4/*68+*4 or *1+*4+*4/*68 etc.
                # https://github.com/Illumina/Cyrius/issues/32#issuecomment-1352402456
                alleles = genotype.split("_")
                num_alleles = len(alleles)
                possible_combos = set()
                for combo in permutations(alleles, num_alleles):
                    for i in range(1, num_alleles):
                        hap1 = "+".join(combo[:i])
                        hap2 = "+".join(combo[i:])
                        genotype = f"{hap1}/{hap2}"
                        genotypes_raw_fixed.add(genotype)
            genotypes_raw_fixed.add(genotype)
        return list(genotypes_raw_fixed)

    def remove_subs(self, genotype):
        # Removes excess data from suballele names
        # Examples:
        # *4.001 -> *4
        # *4C -> *4
        # *2/*41+rs368858603 -> *2/*41
        # *2/*68:2 -> *2/*68
        # *1/*6B -> *1/*6
        # *4.021.ALDY_2 -> *4
        # *4N.ALDY -> *4
        # *141.1001 -> *141
        # *2+42129056.C>G -> *2
        if self.caller == "Aldy":
            pattern = r"\.\d{3,4}|[A-Z]|\+rs\d+|:2|\.ALDY(?:_2)?|\+\d+\.[ACGT]>[ACGT]"
        elif self.caller == "Cyrius":
            pattern = r"\.\d{3}"
        return re.sub(pattern, "", genotype)

    @staticmethod
    def get_haplotype_cnv_status(hap):
        hap_cn = False
        hap_tandem = False
        if "x" in hap:
            hap_cn = True
        if "+" in hap:
            hap_tandem = True
        return hap_cn, hap_tandem

    @staticmethod
    def determine_genotype_order(haplotypes):
        # Order is all about the downstream allele
        hap1, hap2 = haplotypes
        allele1_downstream = int(
            re.sub(r"x\d", "", hap1.split("+")[-1]).replace("*", "")
        )
        allele2_downstream = int(
            re.sub(r"x\d", "", hap2.split("+")[-1]).replace("*", "")
        )
        if allele1_downstream == allele2_downstream:
            hap1_cn, hap1_tandem = CYP2D6Genotype.get_haplotype_cnv_status(hap1)
            hap2_cn, hap2_tandem = CYP2D6Genotype.get_haplotype_cnv_status(hap2)

            if not any([hap1_cn, hap1_tandem, hap2_cn, hap2_tandem]):
                # No tandems or cn in any
                return 0, 1
            elif (hap1_tandem and not hap2_tandem) or (hap1_cn and not hap2_cn):
                # Hap1 has the tandem or cn
                return 1, 0
            elif (not hap1_tandem and hap2_tandem) or (not hap1_cn and hap2_cn):
                # Hap2 has the tandem or cn
                return 0, 1
            elif all([hap1_cn, hap2_cn]):
                # If both alleles have cn, then lower goes first
                cn1 = int(re.findall(r"(?<=x)\d+", hap1)[0])
                cn2 = int(re.findall(r"(?<=x)\d+", hap2)[0])
                if cn1 <= cn2:
                    return 0, 1
                return 1, 0
            elif all([hap1_tandem, hap2_tandem]):
                # Both have a tandem and same downstream allele
                # Order will now be based on the second most downstream allele
                hap1_new = "+".join(hap1.split("+")[:-1])
                hap2_new = "+".join(hap2.split("+")[:-1])
                return CYP2D6Genotype.determine_genotype_order([hap1_new, hap2_new])
        elif allele1_downstream < allele2_downstream:
            return 0, 1
        return 1, 0


class CYP2D6Phenotype:
    def __init__(self, genotype, possible_genotype):
        self.genotype = genotype
        self.possible_genotype = possible_genotype

        self.activity_score = assign_activity(self.genotype)
        self.phenotype = assign_phenotype(self.activity_score)

        self._possible_activity_scores = None
        self.possible_activity_score = self.assign_possible_activity_score()

        self.possible_phenotype = self.assign_possible_phenotype()

    def assign_possible_activity_score(self):
        if self.possible_genotype is not None and self.stellarpgx_flag is None:
            possible_activity_scores = set()
            for possible_genotype in self.possible_genotype.split(";"):
                if "_" in possible_genotype:
                    # Helps with parsing the alleles
                    possible_genotype = possible_genotype.replace("_", "+")
                possible_activity_score = CYP2D6Phenotype.assign_activity(
                    possible_genotype
                )
                possible_activity_scores.add(possible_activity_score)
            if len(possible_activity_scores) == 1:
                self._possible_activity_scores = possible_activity_scores
                return next(iter(possible_activity_scores))
            else:
                self._possible_activity_scores = possible_activity_scores
        return None

    def assign_possible_phenotype(self):
        # Need to handle multiple possible activity scores
        if self._possible_activity_scores is not None:
            possible_phenotypes = set()
            for possible_activity_score in self._possible_activity_scores:
                possible_phenotype = CYP2D6Phenotype.assign_phenotype(
                    possible_activity_score
                )
                possible_phenotypes.add(possible_phenotype)
            if len(possible_phenotypes) == 1:
                return next(iter(possible_phenotypes))
        return None
