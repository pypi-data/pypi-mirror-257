import argparse
from .utils import validate_caller, validate_genotype, validate_file, validate_directory


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organizes CYP2D6 haplotypes according to PharmVar recommendations",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--file", help="File which contains CYP2D6 call from a tool", type=str
    )
    group.add_argument(
        "-d",
        "--dir",
        help="Directory which contains CYP2D6 calls. Accepts glob patterns",
        type=str,
    )
    group.add_argument(
        "-g",
        "--genotype",
        help='CYP2D6 genotype to convert. Must be in form of "hap1/hap2" comma separated',
        type=str,
    )

    parser.add_argument(
        "--caller",
        help="Caller used to generate the CYP2D6 call",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Location to write output. Default is current working directory",
        type=str,
    )
    args = parser.parse_args()

    if args.call:
        validate_genotype(args.call)
        validate_caller(args.caller)
    elif args.file:
        validate_file(args.file)
        validate_caller(args.caller, strict=True)
    else:
        validate_directory(args.dir)
        validate_caller(args.caller, strict=True)
