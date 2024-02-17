import glob

from common import SUPPORTED_CALLERS
from genotype import CYP2D6Data
from utils import (
    assign_phenotype,
    organize_output,
    validate_activity_score,
    validate_caller,
    validate_directory,
    validate_file,
    validate_genotype,
    write_output,
)


def parse_genotype(
    genotype=None,
    file=None,
    dir_=None,
    caller=None,
    output=False,
    output_file=None,
    mask_retired_alleles=True,
):
    if not any([genotype, file, dir_]):
        raise TypeError(
            "Must supply one of genotype, file, or dir_. None were provided"
        )
    if (genotype and file) or (genotype and dir_) or (file and dir_):
        raise TypeError("Must supply only one of genotype, file, or dir_")
    if genotype:
        validate_caller(caller)
        if isinstance(genotype, str):
            genotype = [genotype]
        genotype_results = []
        for geno in genotype:
            validate_genotype(geno)
            genotype_result = CYP2D6Data(
                genotypes_raw=[geno],
                caller=caller,
                mask_retired_alleles=mask_retired_alleles,
            )
            genotype_results.append(genotype_result)

    elif file:
        if caller is None:
            raise TypeError("If the input is a file, must also supply caller")
        validate_file(file)
        validate_caller(caller, strict=True)
        files = [file]
    else:
        if caller is None:
            raise TypeError("If the input is a directory, must also supply caller")
        validate_directory(dir_)
        validate_caller(caller, strict=True)
        files = glob.glob(dir_)
    if file or dir_:
        genotype_results = []
        func = getattr(CYP2D6Data, f"from_{caller.lower()}")
        for genotype_file in files:
            genotype_result = func(
                genotype_file,
                mask_retired_alleles=mask_retired_alleles,
            )
            genotype_results.append(genotype_result)
    organized_results = organize_output(genotype_results, caller)
    if output:
        write_output(organized_results, file=output_file)
    return organized_results


def get_activity_score(genotype, mask_retired_alleles=True):
    validate_genotype(genotype)
    genotype_results = CYP2D6Data([genotype], mask_retired_alleles=mask_retired_alleles)
    return genotype_results.phenotype_data.activity_score


def get_phenotype(genotype=None, activity_score=None, mask_retired_alleles=True):
    if not any([genotype, activity_score]):
        raise TypeError(
            "Must supply one of genotype or activity score. None were provided"
        )
    if genotype:
        validate_genotype(genotype)
        genotype_results = CYP2D6Data(
            [genotype], mask_retired_alleles=mask_retired_alleles
        )
        return genotype_results.phenotype_data.phenotype
    elif activity_score:
        validate_activity_score(activity_score)
        return assign_phenotype(activity_score)
