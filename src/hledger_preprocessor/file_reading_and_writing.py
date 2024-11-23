"""Handles file reading and writing."""

import chardet
from typeguard import typechecked


@typechecked
def write_to_file(*, content: str, file_name: str) -> None:
    with open(file_name, mode="w", encoding="utf-8") as file:
        file.write(content)


@typechecked
def detect_file_encoding(file_path: str) -> str:
    with open(file_path, "rb") as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return str(result["encoding"])


@typechecked
def convert_input_csv_encoding(
    input_csv_filepath: str, output_encoding: str
) -> None:
    detected_encoding = detect_file_encoding(input_csv_filepath)
    # Read the file with the detected encoding and save it as UTF-8
    with open(
        input_csv_filepath,
        encoding=detected_encoding,
        errors="replace",
    ) as infile:
        content = infile.read()

    with open(
        input_csv_filepath, mode="w", encoding=output_encoding
    ) as outfile:
        outfile.write(content)
