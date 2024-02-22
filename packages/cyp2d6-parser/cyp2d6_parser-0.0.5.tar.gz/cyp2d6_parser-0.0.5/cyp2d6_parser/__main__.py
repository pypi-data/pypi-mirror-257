import argparse
from .parser import parse_genotype, get_phenotype, get_activity_score
from .utils import (
    validate_caller,
    validate_genotype,
    validate_file,
    validate_directory,
    validate_activity_score,
)


def call_genotype(args):
    validate_caller(args.caller, strict=not args.genotype_call)
    if args.genotype_call:
        validate_genotype(args.genotype_call)
    elif args.file:
        validate_file(args.file)
    elif args.dir:
        validate_directory(args.dir)
    _ = parse_genotype(
        genotype=args.genotype_call,
        file=args.file,
        dir_=args.dir,
        caller=args.caller,
        output_file=args.output,
        mask_retired_alleles=args.mask,
    )


def call_phenotype(args):
    if args.genotype_call:
        validate_genotype(args.genotype_call)
        validate_caller(args.caller)
    elif args.activity_score:
        validate_activity_score(args.activity_score)
    get_phenotype(
        genotype=args.genotype_call,
        activity_score=args.activity_score,
        caller=args.caller,
    )


def call_activity(args):
    validate_genotype(args.genotype_call)
    validate_caller(args.caller)
    get_activity_score(genotype=args.genotype_call, caller=args.caller)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organizes CYP2D6 haplotypes according to PharmVar recommendations",
    )
    subparsers = parser.add_subparsers(required=True)

    # Genotype
    subparser_genotype = subparsers.add_parser("genotype", help="Genotype parsing")
    subparser_genotype.set_defaults(func=call_genotype)
    group_genotype = subparser_genotype.add_mutually_exclusive_group(required=True)
    group_genotype.add_argument(
        "-f", "--file", help="File which contains CYP2D6 call from a tool", type=str
    )
    group_genotype.add_argument(
        "-d",
        "--dir",
        help="Directory which contains CYP2D6 calls. Accepts glob patterns",
        type=str,
    )
    group_genotype.add_argument(
        "-g",
        "--genotype_call",
        help='CYP2D6 genotype to convert. Must be in form of "hap1/hap2" comma separated',
        type=str,
    )
    subparser_genotype.add_argument(
        "-o",
        "--output",
        help="Output file to write output. Default is current working directory as results.tsv",
        type=str,
    )
    subparser_genotype.add_argument(
        "-m",
        "--mask",
        help="Mask retired alleles. Default is True",
        action="store_true",
    )

    # Phenotype
    subparser_phenotype = subparsers.add_parser("phenotype", help="Phenotype reporting")
    subparser_phenotype.set_defaults(func=call_phenotype)
    group_phenotype = subparser_phenotype.add_mutually_exclusive_group(required=True)
    group_phenotype.add_argument(
        "-g",
        "--genotype_call",
        help="Genotype input for phenotype determination. Must be in for hap1/hap2",
    )
    group_phenotype.add_argument(
        "-a", "--activity_score", help="Activity score to convert to phenotype"
    )

    # Activity
    subparser_activity = subparsers.add_parser(
        "activity", help="Activity score reporting"
    )
    subparser_activity.set_defaults(func=call_activity)
    subparser_activity.add_argument(
        "-g",
        "--genotype_call",
        help="Genotype input for phenotype determination. Must be in for hap1/hap2",
        required=True,
    )

    parser.add_argument(
        "--caller",
        help="Caller used to generate the CYP2D6 call. Required if using file or directory",
        type=str,
    )

    args = parser.parse_args()
