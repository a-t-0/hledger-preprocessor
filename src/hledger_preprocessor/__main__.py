"""Entry point for the project."""

import csv
import os
from argparse import Namespace
from typing import Any, Dict, List

from typeguard import typechecked

from hledger_preprocessor.arg_parser import create_arg_parser, verify_args
from hledger_preprocessor.create_start import ask_user_for_starting_info
from hledger_preprocessor.dir_reading_and_writing import (
    assert_dir_exists,
    generate_output_path,
)
from hledger_preprocessor.file_reading_and_writing import (
    assert_file_exists,
    convert_input_csv_encoding,
    detect_file_encoding,
    write_to_file,
)
from hledger_preprocessor.generate_rules_content import RulesContentCreator
from hledger_preprocessor.parser_logic_structure import Transaction
from hledger_preprocessor.triodos_logic import (
    TriodosParserSettings,
    parse_triodos_transaction,
)


@typechecked
def write_processed_csv(
    transactions: List[Transaction], file_name: str
) -> None:
    # Get fieldnames dynamically from the first object in the list
    if transactions:
        fieldnames = transactions[0].to_dict().keys()
        # TODO: change to ensure the fields are not sorted by the .keys() function.
        # So that they preserve the same order.
        print(f"fieldnames={fieldnames}")

        with open(file_name, mode="w", encoding="utf-8", newline="") as outfile:
            # writer = csv.writer(outfile)
            writer = csv.DictWriter(
                outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL
            )
            writer.writeheader()

            # Write each transaction as a row in the CSV
            for txn in transactions:
                writer.writerow(txn.to_dict())


@typechecked
def process_transactions(
    rows: List[List[str]],
    account_holder: str,
    bank: str,
    account_type: str,
) -> List[Transaction]:
    transactions: List[Transaction] = []
    for index, row in enumerate(
        reversed(rows), start=1
    ):  # Process rows from bottom to top
        transaction = parse_triodos_transaction(
            row,
            index,
            account_holder=account_holder,
            bank=bank,
            account_type=account_type,
        )
        transactions.append(transaction)
    return transactions


@typechecked
def parse_encoded_input_csv(
    input_csv_filepath: str,
    account_holder: str,
    bank: str,
    account_type: str,
) -> List[Transaction]:
    updated_encoding = detect_file_encoding(input_csv_filepath)
    with open(
        input_csv_filepath,
        encoding=updated_encoding,
        errors="replace",
    ) as infile:
        reader = csv.reader(infile)
        rows = list(reader)
    transactions = process_transactions(
        rows,
        account_holder=account_holder,
        bank=bank,
        account_type=account_type,
    )

    return transactions


@typechecked
def get_years(*, transactions: List[Transaction]) -> List[int]:
    years: List[int] = [transaction.get_year() for transaction in transactions]
    return years


def sort_transactions_on_years(
    *, transactions: List[Transaction]
) -> Dict[int, List[Transaction]]:
    years = get_years(transactions=transactions)
    return {
        year: [t for t in transactions if t.get_year() == year]
        for year in years
    }


@typechecked
def pre_process_csvs(*, args: Namespace) -> None:
    # Hardcoded parameters.
    csv_encoding: str = "utf-8"

    # Convert the input csv file encoding.
    convert_input_csv_encoding(
        input_csv_filepath=args.input_file, output_encoding=csv_encoding
    )
    total_transactions: List[Transaction] = parse_encoded_input_csv(
        input_csv_filepath=args.input_file,
        account_holder=args.account_holder,
        bank=args.bank,
        account_type=args.account_type,
    )
    transactions_per_year: Dict[int, List[Transaction]] = (
        sort_transactions_on_years(transactions=total_transactions)
    )

    # Output the pre-processed .csv files per year.
    for year, transactions in transactions_per_year.items():
        output_filepath: str = generate_output_path(
            root_path=args.start_path,
            account_holder=args.account_holder,
            bank=args.bank,
            account_type=args.account_type,
            pre_processed_output_dir=args.pre_processed_output_dir,
            year=year,
            input_filename=os.path.basename(args.input_file),
        )
        write_processed_csv(
            transactions=transactions, file_name=output_filepath
        )


@typechecked
def generate_rules_file(*, args: Namespace) -> None:
    if args.bank is None or args.bank == "":
        raise ValueError("Must specify bank.")
    if args.account_holder is None or args.account_holder == "":
        raise ValueError("Must specify account_holder.")

    if args.account_type is None or args.account_type == "":
        raise ValueError("Must specify account_type.")

    # Generate rules file.
    triodosParserSettings: TriodosParserSettings = TriodosParserSettings()
    triodosRules: RulesContentCreator = RulesContentCreator(
        parserSettings=triodosParserSettings,
        currency="EUR",
        account_holder=args.account_holder,
        bank_name=args.bank,
        account_type=args.account_type,
        status="*",  # TODO: get from Triodos logic.
    )

    rules_output_dir: str = (
        f"{args.start_path}/import/{args.account_holder}/{args.bank}/"
        + f"{args.account_type}"
    )
    rules_filepath = f"{rules_output_dir}/{args.bank}-{args.account_type}.rules"

    assert_dir_exists(dirpath=rules_output_dir)

    write_to_file(
        content=triodosRules.create_rulecontent(),
        file_name=rules_filepath,
    )
    assert_file_exists(filepath=rules_filepath)


@typechecked
def main() -> None:

    # Parse input arguments
    parser = create_arg_parser()
    args: Any = verify_args(parser=parser)

    # TODO: determine which bank is used and get logic accordingly.
    if args.new:
        ask_user_for_starting_info(
            root_finance_path=args.start_path,
            account_holder=args.account_holder,
            bank=args.bank,
            account_type=args.account_type,
            csv_filepath=args.csv_filepath,
        )
    # TODO: determine if elif is needed.
    if args.generate_rules:
        generate_rules_file(args=args)
    if args.pre_processed_output_dir:
        pre_process_csvs(args=args)
