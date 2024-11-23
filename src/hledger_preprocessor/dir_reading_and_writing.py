"""Handles directory reading and writing."""

import os

from typeguard import typechecked


@typechecked
def path_exists(path: str) -> bool:
    """Check if a given path exists."""
    return os.path.exists(path)


@typechecked
def create_year_directory(base_path: str, year: int) -> str:
    """Create a directory for the given year under base_path."""
    year_path = os.path.join(base_path, str(year))
    os.makedirs(year_path, exist_ok=True)
    assert path_exists(year_path), f"Year directory {year_path} does not exist!"
    return year_path


@typechecked
def generate_output_path(
    *,
    root_path: str,
    account_holder: str,
    bank: str,
    account_type: str,
    pre_processed_output_dir: str,
    year: int,
    input_filename: str,
) -> str:
    """Generate the output path, ensure necessary directories exist."""
    base_path = (
        f"{root_path}/import/{account_holder}/"
        + f"{bank}/{account_type}/{pre_processed_output_dir}"
    )
    if not path_exists(base_path):
        os.makedirs(base_path, exist_ok=True)
        assert path_exists(base_path), f"Base path {base_path} does not exist!"
    return f"{create_year_directory(base_path, year)}/{input_filename}"
