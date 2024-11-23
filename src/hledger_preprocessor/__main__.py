"""Entry point for the project."""

import csv
import os
from typing import Dict, List

from typeguard import typechecked

from src.hledger_preprocessor.arg_parser import create_arg_parser
from src.hledger_preprocessor.dir_reading_and_writing import (
    generate_output_path,
)
from src.hledger_preprocessor.file_reading_and_writing import (
    convert_input_csv_encoding,
    detect_file_encoding,
    write_to_file,
)
from src.hledger_preprocessor.triodos_logic import (
    TriodosRules,
    TriodosTransaction,
    parse_tridos_transaction,
    write_processed_csv,
)


@typechecked
def process_transactions(rows: List[List[str]]) -> List[TriodosTransaction]:
    transactions: List[TriodosTransaction] = []
    for index, row in enumerate(
        reversed(rows), start=1
    ):  # Process rows from bottom to top
        transaction = parse_tridos_transaction(row, index)
        transactions.append(transaction)
    return transactions


@typechecked
def parse_encoded_input_csv(
    input_csv_filepath: str,
) -> List[TriodosTransaction]:
    updated_encoding = detect_file_encoding(input_csv_filepath)
    with open(
        input_csv_filepath,
        encoding=updated_encoding,
        errors="replace",
    ) as infile:
        reader = csv.reader(infile)
        rows = list(reader)
    transactions = process_transactions(rows)

    return transactions


@typechecked
def get_years(*, transactions: List[TriodosTransaction]) -> List[int]:
    years: List[int] = [transaction.get_year() for transaction in transactions]
    return years


def sort_transactions_on_years(
    *, transactions: List[TriodosTransaction]
) -> Dict[int, List[TriodosTransaction]]:
    years = get_years(transactions=transactions)
    return {
        year: [t for t in transactions if t.get_year() == year]
        for year in years
    }


@typechecked
def main() -> None:
    # Hardcoded parameters.
    csv_encoding: str = "utf-8"

    # Parse input arguments
    parser = create_arg_parser()
    args = parser.parse_args()

    # Generate rules file.
    triodosRules: TriodosRules = TriodosRules(
        nr_of_header_lines=1,  # TODO: get from Triodos logic.
        currency="EUR",
        account_holder=args.account_holder,
        bank_name=args.bank,
        account_type=args.account_type,
        status="*",  # TODO: get from Triodos logic.
    )
    write_to_file(
        content=triodosRules.create_rulecontent(),
        file_name=f"{args.root_path}/import/{args.bank}.rules",
    )

    # Convert the input csv file encoding.
    convert_input_csv_encoding(
        input_csv_filepath=args.input_file, output_encoding=csv_encoding
    )
    total_transactions: List[TriodosTransaction] = parse_encoded_input_csv(
        input_csv_filepath=args.input_file
    )
    transactions_per_year: Dict[int, List[TriodosTransaction]] = (
        sort_transactions_on_years(transactions=total_transactions)
    )

    # Output the pre-processed .csv files per year.
    for year, transactions in transactions_per_year.items():
        output_filepath: str = generate_output_path(
            root_path=args.root_path,
            account_holder=args.account_holder,
            bank=args.bank,
            account_type=args.account_type,
            pre_processed_output_dir=args.pre_processed_output_dir,
            year=year,
            input_filename=os.path.basename(args.input_file),
        )
        print(f"output_filepath={output_filepath}")
        write_processed_csv(
            transactions=transactions, file_name=output_filepath
        )


if __name__ == "__main__":
    main()
