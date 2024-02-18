#! /usr/bin/env python
"""Traces records and changes through history."""
from __future__ import annotations

import time
from typing import TYPE_CHECKING

import dictdiffer

import colrev.operation
from colrev.constants import Colors

if TYPE_CHECKING:
    import git.objects.commit


class Trace(colrev.operation.Operation):
    """Trace a record through history"""

    def __init__(self, *, review_manager: colrev.review_manager.ReviewManager) -> None:
        super().__init__(
            review_manager=review_manager,
            operations_type=colrev.operation.OperationsType.check,
        )

    def __lpad_multiline(self, *, s: str, lpad: int) -> str:
        lines = s.splitlines()
        return "\n".join(["".join([" " * lpad]) + line for line in lines])

    def __print_record_changes(
        self,
        *,
        commit: git.objects.commit.Commit,
        records_dict: dict,
        record_id: str,
        prev_record: dict,
    ) -> dict:
        record = records_dict[record_id]

        diffs = list(dictdiffer.diff(prev_record, record))

        if len(diffs) > 0:
            if not self.review_manager.verbose_mode:
                commit_message_first_line = str(commit.message).partition("\n")[0]
                print(
                    "\n\n"
                    + time.strftime(
                        "%Y-%m-%d %H:%M",
                        time.gmtime(commit.committed_date),
                    )
                    + f" {commit} ".ljust(40, " ")
                    + f" {commit_message_first_line} (by {commit.author.name})"
                )

            for diff in diffs:
                if diff[0] == "add":
                    print(
                        Colors.GREEN
                        + self.__lpad_multiline(
                            s=self.review_manager.p_printer.pformat(diff),
                            lpad=5,
                        )
                        + Colors.END
                    )
                if diff[0] == "change":
                    print(
                        Colors.ORANGE
                        + self.__lpad_multiline(
                            s=self.review_manager.p_printer.pformat(diff),
                            lpad=5,
                        )
                        + Colors.END
                    )
                if diff[0] == "delete":
                    print(
                        Colors.RED
                        + self.__lpad_multiline(
                            s=self.review_manager.p_printer.pformat(diff),
                            lpad=5,
                        )
                        + Colors.END
                    )

        prev_record = record
        return prev_record

    @colrev.operation.Operation.decorate()
    def main(self, *, record_id: str) -> None:
        """Trace a record (main entrypoint)"""

        self.review_manager.logger.info(f"Trace record by ID: {record_id}")

        revlist = self.review_manager.dataset.get_repo().iter_commits()

        prev_record: dict = {}
        for commit in reversed(list(revlist)):
            try:
                # Ensure the path uses forward slashes, which is compatible with Git's path handling
                records_file_path = str(
                    self.review_manager.dataset.RECORDS_FILE_RELATIVE
                ).replace("\\", "/")
                filecontents = (commit.tree / records_file_path).data_stream.read()

            except KeyError:
                continue

            commit_message_first_line = str(commit.message).partition("\n")[0]

            if self.review_manager.verbose_mode:
                print(
                    "\n\n"
                    + time.strftime(
                        "%Y-%m-%d %H:%M",
                        time.gmtime(commit.committed_date),
                    )
                    + f" {commit} ".ljust(40, " ")
                    + f" {commit_message_first_line} (by {commit.author.name})"
                )

            records_dict = self.review_manager.dataset.load_records_dict(
                load_str=filecontents.decode("utf-8")
            )

            if record_id not in records_dict:
                if self.review_manager.verbose_mode:
                    print(f"record {record_id} not in commit.")
                continue

            prev_record = self.__print_record_changes(
                commit=commit,
                records_dict=records_dict,
                record_id=record_id,
                prev_record=prev_record,
            )
