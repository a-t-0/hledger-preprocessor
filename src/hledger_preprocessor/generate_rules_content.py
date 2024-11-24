"""Contains the logic for preprocessing Triodos .csv files to prepare them for
hledger."""

from dataclasses import dataclass

from typeguard import typechecked

from hledger_preprocessor.parser_logic_structure import ParserSettings


@dataclass
class RulesContentCreator:
    parserSettings: ParserSettings
    currency: str
    account_holder: str
    bank_name: str
    account_type: str
    status: str

    @typechecked
    def create_rulecontent(self) -> str:
        content = ""
        # Write skip rule
        content += (
            "# If your `.csv` file contains a header row, you skip 1 row, if"
            " it does not have a header row, skip 0 rows.\n"
        )
        if self.parserSettings.uses_header():
            content += "skip 1\n\n"
        else:
            content += "skip 0\n\n"

        # Write fields
        content += (
            f"fields {', '.join(self.parserSettings.get_field_names())}\n\n"
        )

        # Write currency
        content += f"currency {self.currency}\n"

        # Write status
        content += f"status {self.status}\n\n"

        # Write account1 and description format
        content += (
            "account1"
            " Assets:current:"
            f"{self.account_holder}:{self.bank_name}:{self.account_type}\n"
        )

        # TODO: include tag/category in this perhaps.
        # Original: description %desc1/%desc2/%desc3
        content += "description %description"
        return content
