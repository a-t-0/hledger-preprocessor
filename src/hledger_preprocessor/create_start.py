import os
import shutil
from datetime import datetime
from typing import Tuple

from typeguard import typechecked


@typechecked
def get_script_path() -> str:
    """Gets the path of the current script."""
    return os.path.dirname(os.path.abspath(__file__))


@typechecked
def assert_dir_exists(dir_path: str) -> None:
    """Asserts that the given directory exists.

    Args:
      dir_path: The path to the directory.

    Raises:
      FileNotFoundError: If the directory does not exist.
    """

    if not os.path.isdir(dir_path):
        raise FileNotFoundError(f"Directory '{dir_path}' does not exist.")


def assert_file_exists(file_path: str) -> None:
    """Asserts that the given file exists.

    Args:
      file_path: The path to the file.

    Raises:
      FileNotFoundError: If the file does not exist.
    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' does not exist.")


def ask_user_for_starting_info(
    *,
    root_finance_path: str,
    account_holder: str,
    bank: str,
    account_type: str,
    csv_filepath: str,
) -> Tuple[str, str, str, str, str]:
    """Prompts the user for necessary information to set up the import
    directory structure.

    Returns:
      A tuple containing:
        - base_dir: The base directory for the import structure.
        - account_holder: The name of the account holder.
        - bank: The name of the bank.
        - account_type: The type of the account.
        - year: The year of the transactions.
    """
    path_to_account_type, current_year_path = build_directory_structure(
        root_finance_path, account_holder, bank, account_type
    )

    current_path: str = get_script_path()
    copy_script_to_target_dir(
        path_to_account_type=path_to_account_type,
        source_script_path=f"{current_path}/createRules",
    )
    copy_script_to_target_dir(
        path_to_account_type=path_to_account_type,
        source_script_path=f"{current_path}/preprocess",
    )
    copy_script_to_target_dir(
        path_to_account_type=f"{current_year_path}",
        source_script_path=csv_filepath,
    )

    return root_finance_path, account_holder, bank, account_type


@typechecked
def copy_script_to_target_dir(
    path_to_account_type: str, source_script_path: str
) -> None:
    script_filename: str = os.path.basename(source_script_path)
    assert_dir_exists(path_to_account_type)
    assert_file_exists(source_script_path)

    # copy the script into the account holder path.
    shutil.copy(source_script_path, path_to_account_type)
    assert_file_exists(f"{path_to_account_type}/{script_filename}")


@typechecked
def build_directory_structure(
    root_finance_path: str, account_holder: str, bank: str, account_type: str
) -> Tuple[str, str]:
    """Creates the required directory structure for the specified account
    details.

    Args:
        root_finance_path: The root directory for finance-related files.
        account_holder: The name of the account holder.
        bank: The name of the bank.
        account_type: The type of account.

    Returns:
        The path to the "1-in" directory.
    """
    # Assert the root directory exists
    assert os.path.exists(
        root_finance_path
    ), f"Root directory '{root_finance_path}' does not exist."

    import_path = os.path.join(root_finance_path, "import")
    create_dir(import_path)

    account_holder_path = os.path.join(import_path, account_holder)
    create_dir(account_holder_path)

    bank_path = os.path.join(account_holder_path, bank)
    create_dir(bank_path)

    account_type_path = os.path.join(bank_path, account_type)
    create_dir(account_type_path)

    one_in_path = os.path.join(account_type_path, "1-in")
    create_dir(one_in_path)

    current_year_path = os.path.join(one_in_path, str(datetime.now().year))
    create_dir(current_year_path)

    return account_type_path, current_year_path


def create_dir(path: str) -> None:
    """Creates a directory at the specified path.

    Args:
        path: The path to the directory to create.

    Raises:
        FileNotFoundError: If the parent directory does not exist.
    """
    assert os.path.exists(
        os.path.dirname(path)
    ), f"Parent directory '{os.path.dirname(path)}' does not exist."
    os.makedirs(path, exist_ok=True)
    assert os.path.isdir(path), f"Failed to create directory '{path}'"


@typechecked
def get_account_info_from_dir(root_dir: str) -> list[dict]:
    """Scans the given root directory for subdirectories representing account
    holders, banks, and account types.

    Args:
        root_dir: The root directory to scan.

    Returns:
        A list of dictionaries, each containing 'account', 'bank', and 'account_type' keys.
    """

    account_info = []
    for account_holder in os.listdir(root_dir):
        account_holder_dir = os.path.join(root_dir, account_holder)
        if os.path.isdir(account_holder_dir):
            for bank in os.listdir(account_holder_dir):
                bank_dir = os.path.join(account_holder_dir, bank)
                if os.path.isdir(bank_dir):
                    for account_type in os.listdir(bank_dir):
                        account_type_dir = os.path.join(bank_dir, account_type)
                        if os.path.isdir(account_type_dir):
                            account_info.append(
                                {
                                    "account": account_holder,
                                    "bank": bank,
                                    "account_type": account_type,
                                }
                            )
    return account_info


# # Example usage:
# root_finance_path = "path/to/your/finance/repository"
# account_info_list = get_account_info_from_dir(root_finance_path)

# # Print the account information in a user-friendly format
# for info in account_info_list:
#     print(f"{info['account']} - {info['bank']} - {info['account_type']}")
