import re

import numpy as np
import pandas as pd

from .common import ALLELE_FXN_PATH


class CYP2D6Phenotype:
    def __init__(self, genotype, possible_genotype, stellarpgx_flag=None):
        self.genotype = genotype
        self.possible_genotype = possible_genotype
        self.stellarpgx_flag = stellarpgx_flag

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
                possible_activity_score = assign_activity(possible_genotype)
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
                possible_phenotype = assign_phenotype(possible_activity_score)
                possible_phenotypes.add(possible_phenotype)
            if len(possible_phenotypes) == 1:
                return next(iter(possible_phenotypes))
        return None


def assign_activity(genotype):
    if genotype == "Indeterminate/Indeterminate":
        return "n/a"
    elif genotype is np.nan:
        return np.nan
    total_activity = 0
    na_activity = False
    allele_to_activity = _get_allele_activity()
    for hap in genotype.split("/"):
        for allele in hap.split("+"):
            copies = 1
            if "x" in allele:
                copies = int(re.findall(r"x\d", allele)[0].strip("x"))
                allele = re.findall(r"\*\d+", allele)[0]
            allele_activity = allele_to_activity[allele]
            try:
                total_activity += float(allele_activity) * copies
            except ValueError:
                na_activity = True
    if na_activity:
        return f">= {total_activity}"
    return total_activity


def assign_phenotype(activity_score):
    # https://pubmed.ncbi.nlm.nih.gov/31647186/
    try:
        if activity_score == "n/a" or ">=" in activity_score:
            return "CYP2D6 Indeterminate Metabolizer"
    except TypeError:
        # activity is already a float
        if activity_score == 0:
            return "CYP2D6 Poor Metabolizer"
        elif activity_score >= 0.25 and activity_score <= 1:
            return "CYP2D6 Intermediate Metabolizer"
        elif activity_score >= 1.25 and activity_score <= 2.25:
            return "CYP2D6 Normal Metabolizer"
        elif activity_score > 2.25:
            return "CYP2D6 Ultrarapid Metabolizer"


def _get_allele_activity():
    allele_fxn = pd.read_csv(ALLELE_FXN_PATH, comment="#")

    allele_to_activity = allele_fxn.set_index("allele").to_dict()["activity_score"]
    allele_to_activity["Indeterminate"] = "n/a"
    return allele_to_activity
