"""Contains uncategorised helper functions."""

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
