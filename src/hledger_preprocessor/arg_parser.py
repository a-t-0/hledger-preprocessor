"""Parses the CLI args."""

import argparse
import re
from argparse import ArgumentParser
from typing import Any

from typeguard import typechecked


@typechecked
def create_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Triodos Bank CSV to custom format."
    )

    # Required args.
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
        "-t",
        "--account-type",
        type=str,
        required=True,
        help="Account type, e.g. checkings/savings etc..",
    )

    parser.add_argument(
        "-n",
        "--new",
        action="store_true",
        help=(
            "Use this flag if you want to add a new account for double-entry"
            " book keeping."
        ),
    )
    parser.add_argument(
        "-c",
        "--csv-filepath",
        type=str,
        help="Specify the path to the input csv.",
    )

    # Optional args.
    parser.add_argument(
        "-i",
        "--input-file",
        type=str,
        required=False,
        help="Path to the input CSV file containing Triodos bank data.",
    )
    parser.add_argument(
        "-g",
        "--generate-rules",
        action="store_true",
        help="Generates the .rules file for hledger flow imports.",
    )
    parser.add_argument(
        "-s",
        "--start-path",
        type=str,
        required=True,
        help="Path to root of the finance repo/folder.",
    )
    parser.add_argument(
        "-p",
        "--pre-processed-output-dir",
        type=str,
        required=False,
        help="The dir name containing the pre-processed csv files..",
    )

    return parser


@typechecked
def verify_args(*, parser: ArgumentParser) -> Any:
    args: Any = parser.parse_args()
    print(f"args={args}")
    if args.account_holder or args.bank or args.account_type:
        if (
            not args.generate_rules
            and args.pre_processed_output_dir is None
            and not args.new
        ):
            raise ValueError(
                "Must either create rules, preprocess csv's or start a new"
                " hledger-flow import setup."
            )
    if not args.new and args.csv_filepath or not args.new and args.csv_filepath:
        parser.error(
            "If you start, the --csv-filepath and the --new arg flags must be"
            " used."
        )

    assert_has_only_valid_chars(input_string=args.account_holder)
    assert_has_only_valid_chars(input_string=args.bank)
    assert_has_only_valid_chars(input_string=args.account_type)

    return args


def assert_has_only_valid_chars(*, input_string: str) -> None:
    # a-Z, underscore, \, /.
    valid_chars = re.compile(r"^[a-zA-Z0-9_/\\]*$")
    assert valid_chars.match(
        input_string
    ), f"Invalid characters found in: {input_string}"
