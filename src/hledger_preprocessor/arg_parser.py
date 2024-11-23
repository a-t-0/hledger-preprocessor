"""Parses the CLI args."""

import argparse

from typeguard import typechecked


@typechecked
def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Triodos Bank CSV to custom format."
    )

    parser.add_argument(
        "-a",
        "--account-holder",
        type=str,
        required=True,
        help="Name of account holder.",
    )
    parser.add_argument(
        "-b", "--bank", type=str, required=True, help="Name of bank."
    )

    parser.add_argument(
        "-i",
        "--input-file",
        type=str,
        required=True,
        help="Path to the input CSV file containing Triodos bank data.",
    )
    parser.add_argument(
        "-r",
        "--root-path",
        type=str,
        required=True,
        help="Path to root of this repo.",
    )
    parser.add_argument(
        "-p",
        "--pre-processed-output-dir",
        type=str,
        required=True,
        help="The dir name containing the pre-processed csv files..",
    )
    parser.add_argument(
        "-t",
        "--account-type",
        type=str,
        required=True,
        help="Account type, e.g. checkings/savings etc..",
    )

    return parser
