import glob
import os
import re
import warnings

import numpy as np
import pandas as pd

from common import SUPPORTED_CALLERS


def write_output(df, file=None):
    if file is not None:
        dir_, _ = os.path.split(file)
        if not os.path.isdir(dir_) and len(dir_) != 0:
            raise FileNotFoundError(
                f"Provided directory {file} for output file does not exist"
            )
    else:
        file = os.path.join(os.getcwd(), "parsed_results.csv")
    df.to_csv(file, index=False)
    print(f"Wrote output to {file}")


def _parse_vals(call):
    vals = [
        call.sample_id,
        ";".join(call.genotype_data.genotypes_raw),
        call.genotype_data.genotype,
        call.phenotype_data.activity_score,
        call.phenotype_data.phenotype,
        call.cn,
        call.genotype_data.possible_genotype,
        call.phenotype_data.possible_activity_score,
        call.phenotype_data.possible_phenotype,
    ]
    if call.caller == "cyrius":
        vals = vals + [call.cyrius_filter]
    elif call.caller == "stellarpgx":
        vals = vals + [call.stellarpgx_flag]
    return vals


def organize_output(genotype_results, caller):
    genotype_results_clean = []
    for genotype_result in genotype_results:
        genotype_results_clean.append(_parse_vals(genotype_result))
    return compile_data(genotype_results_clean, caller=caller)


def validate_activity_score(activity_score):
    activity_score = str(activity_score)
    if re.search(r"[^n/a\d\*\.]", activity_score) or not re.search(
        r"(?:\d\.\d)|(?:\d)", activity_score
    ):
        raise ValueError(f"Activity score {activity_score} not in correct format")


def validate_caller(caller, strict=False):
    if caller is None or caller.lower() not in SUPPORTED_CALLERS:
        if strict:
            raise ValueError(
                f"Caller {caller} is not supported. Must provide supported caller from {SUPPORTED_CALLERS}"
            )
        warnings.warn(
            f"Caller {caller} is not a known caller. Defaulting to generic caller"
        )
    return True


def validate_genotype(genotype):
    if not isinstance(genotype, str):
        raise TypeError(f"Genotype must be of type str got {type(genotype)}")
    for geno in genotype.split(","):
        if geno.count("/") != 1:
            raise ValueError(
                f"Genotype {genotype} must be in the form of 'hap1/hap2' comma delimited"
            )


def validate_file(file):
    if not os.path.isfile(file):
        raise FileNotFoundError(f"File {file} not found")


def validate_directory(dir_):
    if len(glob.glob(dir_)) == 0:
        raise ValueError(
            f"Provided directory {dir_} does not exist or does not contain any files"
        )


def compile_data(compiled_data, caller=None):
    columns = [
        "person_id",
        "genotype_raw",
        "genotype",
        "activity_score",
        "phenotype",
        "copy_number",
        "possible_genotype",
        "possible_activity_score",
        "possible_phenotype",
    ]
    caller = caller.lower() if caller is not None else None
    if caller == "cyrius":
        columns.append("cyrius_filter")
    elif caller == "stellarpgx":
        columns.append("stellarpgx_flag")
    return (
        pd.DataFrame(compiled_data, columns=columns)
        .fillna(np.nan)  # Replaces None with np.nan
        .assign(
            activity_score=lambda x: "CYP2D6 Activity Score "
            + x["activity_score"].astype(str),
            possible_activity_score=lambda x: np.where(
                x["possible_activity_score"].notna(),
                "CYP2D6 Activity Score " + x["possible_activity_score"].astype(str),
                np.nan,
            ),
        )
    )


def _get_allele_activity():
    # allele_fxn = pd.read_csv(os.path.join("lib", "allele_fxn.csv"), comment="#")
    allele_fxn = pd.read_csv("allele_fxn.csv", comment="#")

    allele_to_activity = allele_fxn.set_index("allele").to_dict()["activity_score"]
    allele_to_activity["Indeterminate"] = "n/a"
    return allele_to_activity


def determine_copy_number(genotype):
    if genotype == "Indeterminate/Indeterminate":
        return np.nan
    cn = 0
    for hap in genotype.split("/"):
        for allele in hap.split("+"):
            if allele == "*5":
                continue
            if "x" in allele:
                copies = int(re.findall(r"(?<=x)\d", allele)[0])
                cn += copies
            else:
                cn += 1
    return cn


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
