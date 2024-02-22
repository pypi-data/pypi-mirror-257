import unittest
from cyp2d6_parser import genotype
from cyp2d6_parser.common import BAD_GENOTYPES


class TestGenotype(unittest.TestCase):

    def test_tandem_order(self):
        # *36+*10
        result = genotype.CYP2D6Genotype(genotypes_raw=["*36+*10/*1"])
        self.assertEqual(result.genotype, "*1/*36+*10")

        # *68+*4
        result = genotype.CYP2D6Genotype(genotypes_raw=["*2/*4+*68"])
        self.assertEqual(result.genotype, "*2/*68+*4")

        # *13+*68+*4
        result = genotype.CYP2D6Genotype(genotypes_raw=["*2/*13+*68+*4"])
        self.assertEqual(result.genotype, "*2/*13+*68+*4")

    def test_genotype_order(self):
        # Genotype order is all about downstream allele
        result = genotype.CYP2D6Genotype(genotypes_raw=["*68+*4/*9x2"])
        self.assertEqual(result.genotype, "*68+*4/*9x2")
        result = genotype.CYP2D6Genotype(genotypes_raw=["*68+*4/*4+*1"])
        self.assertEqual(result.genotype, "*1+*4/*68+*4")

        # Allele with no tandem or cn is always first
        result = genotype.CYP2D6Genotype(genotypes_raw=["*2x3/*2"])
        self.assertEqual(result.genotype, "*2/*2x3")

        # Genotype order is number based not string based
        result = genotype.CYP2D6Genotype(genotypes_raw=["*11/*2"])
        self.assertEqual(result.genotype, "*2/*11")

    def test_retired_alleles(self):
        result = genotype.CYP2D6Data(
            genotypes_raw=["*57/*1"], mask_retired_alleles=False
        )
        self.assertEqual(result.genotype_data.genotype, "*1/*57")
        self.assertEqual(result.phenotype_data.activity_score, 1)

    def test_bad_genotypes(self):
        for bad_genotype in BAD_GENOTYPES:
            result = genotype.CYP2D6Genotype(genotypes_raw=[bad_genotype])
            self.assertEqual(result.genotype, "Indeterminate/Indeterminate")


class TestPhenotype(unittest.TestCase):

    def test_phenotype_with_genotype(self):
        result = genotype.CYP2D6Phenotype(genotype="*1/*36+*10", possible_genotype=None)
        self.assertEqual(result.activity_score, 1.25)
        self.assertEqual(result.phenotype, "CYP2D6 Normal Metabolizer")

        result = genotype.CYP2D6Phenotype(genotype="*5/*5", possible_genotype=None)
        self.assertEqual(result.activity_score, 0)
        self.assertEqual(result.phenotype, "CYP2D6 Poor Metabolizer")

        result = genotype.CYP2D6Phenotype(
            genotype="Indeterminate/Indeterminate", possible_genotype=None
        )
        self.assertEqual(result.activity_score, "n/a")
        self.assertEqual(result.phenotype, "CYP2D6 Indeterminate Metabolizer")

    def test_phenotype_with_possible_genotypes(self):
        result = genotype.CYP2D6Phenotype(
            genotype="Indeterminate/Indeterminate", possible_genotype="*1/*1;*1/*2"
        )
        self.assertEqual(result.activity_score, "n/a")
        self.assertEqual(result.phenotype, "CYP2D6 Indeterminate Metabolizer")
        self.assertEqual(result.possible_activity_score, 2.0)
        self.assertEqual(result.possible_phenotype, "CYP2D6 Normal Metabolizer")

        result = genotype.CYP2D6Phenotype(
            genotype="Indeterminate/Indeterminate", possible_genotype="*1/*1;*1/*4"
        )
        self.assertEqual(result.activity_score, "n/a")
        self.assertEqual(result.phenotype, "CYP2D6 Indeterminate Metabolizer")
        self.assertEqual(result.possible_activity_score, None)
        self.assertEqual(result.possible_phenotype, None)

        result = genotype.CYP2D6Phenotype(
            genotype="Indeterminate/Indeterminate", possible_genotype="*1/*1;*1/*10"
        )
        self.assertEqual(result.activity_score, "n/a")
        self.assertEqual(result.phenotype, "CYP2D6 Indeterminate Metabolizer")
        self.assertEqual(result.possible_activity_score, None)
        self.assertEqual(result.possible_phenotype, "CYP2D6 Normal Metabolizer")
