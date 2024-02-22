import unittest
from cyp2d6_parser import phenotype


class TestPhenotype(unittest.TestCase):

    def test_phenotype_with_genotype(self):
        result = phenotype.CYP2D6Phenotype(
            genotype="*1/*36+*10", possible_genotype=None
        )
        self.assertEqual(result.activity_score, 1.25)
        self.assertEqual(result.phenotype, "CYP2D6 Normal Metabolizer")

        result = phenotype.CYP2D6Phenotype(genotype="*5/*5", possible_genotype=None)
        self.assertEqual(result.activity_score, 0)
        self.assertEqual(result.phenotype, "CYP2D6 Poor Metabolizer")

        result = phenotype.CYP2D6Phenotype(
            genotype="Indeterminate/Indeterminate", possible_genotype=None
        )
        self.assertEqual(result.activity_score, "n/a")
        self.assertEqual(result.phenotype, "CYP2D6 Indeterminate Metabolizer")

    def test_phenotype_with_possible_genotypes(self):
        result = phenotype.CYP2D6Phenotype(
            genotype="Indeterminate/Indeterminate", possible_genotype="*1/*1;*1/*2"
        )
        self.assertEqual(result.activity_score, "n/a")
        self.assertEqual(result.phenotype, "CYP2D6 Indeterminate Metabolizer")
        self.assertEqual(result.possible_activity_score, 2.0)
        self.assertEqual(result.possible_phenotype, "CYP2D6 Normal Metabolizer")

        result = phenotype.CYP2D6Phenotype(
            genotype="Indeterminate/Indeterminate", possible_genotype="*1/*1;*1/*4"
        )
        self.assertEqual(result.activity_score, "n/a")
        self.assertEqual(result.phenotype, "CYP2D6 Indeterminate Metabolizer")
        self.assertEqual(result.possible_activity_score, None)
        self.assertEqual(result.possible_phenotype, None)

        result = phenotype.CYP2D6Phenotype(
            genotype="Indeterminate/Indeterminate", possible_genotype="*1/*1;*1/*10"
        )
        self.assertEqual(result.activity_score, "n/a")
        self.assertEqual(result.phenotype, "CYP2D6 Indeterminate Metabolizer")
        self.assertEqual(result.possible_activity_score, None)
        self.assertEqual(result.possible_phenotype, "CYP2D6 Normal Metabolizer")
