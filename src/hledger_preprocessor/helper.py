"""Contains uncategorised helper functions."""

from argparse import Namespace
from datetime import datetime

from typeguard import typechecked


@typechecked
def parse_date(date_string: str, date_format: str = "%d-%m-%Y") -> datetime:
    return datetime.strptime(date_string, date_format)
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError as e:
        raise ValueError(
            f"Invalid date format for {date_string}. Expected format:"
            f" {date_format}"
        ) from e


@typechecked
def format_date_to_iso(
    date_string: str,
    input_format: str = "%d-%m-%Y",
    output_format: str = "%Y-%m-%d",
) -> str:
    return datetime.strptime(date_string, input_format).strftime(output_format)


@typechecked
def assert_bank_to_account_args_are_valid(*, args: Namespace) -> None:
    if args.bank is None or args.bank == "":
        raise ValueError("Must specify bank.")
    if args.account_holder is None or args.account_holder == "":
        raise ValueError("Must specify account_holder.")

    if args.account_type is None or args.account_type == "":
        raise ValueError("Must specify account_type.")
