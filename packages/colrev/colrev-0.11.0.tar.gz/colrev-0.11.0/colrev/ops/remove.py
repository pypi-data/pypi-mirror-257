#!/usr/bin/env python3
"""Remove records, ... from CoLRev projects."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import colrev.env.utils
import colrev.operation
from colrev.constants import Fields

if TYPE_CHECKING:
    import colrev.review_manager


# pylint: disable=too-few-public-methods


class Remove(colrev.operation.Operation):
    """Remove records, ... from CoLRev projects."""

    def __init__(
        self,
        *,
        review_manager: colrev.review_manager.ReviewManager,
    ) -> None:
        super().__init__(
            review_manager=review_manager,
            operations_type=colrev.operation.OperationsType.check,
            notify_state_transition_operation=False,
        )

    @colrev.operation.Operation.decorate()
    def remove_records(self, *, ids: str) -> None:
        """Remove records from CoLRev project."""

        records = self.review_manager.dataset.load_records_dict()

        for record_id in ids.split(","):
            if record_id in records:
                self.review_manager.logger.info(f" remove {record_id}")
                origins = records[record_id][Fields.ORIGIN]
                if Fields.FILE in records[record_id]:
                    print(f"manually remove file: {records[record_id]['file']}")
                del records[record_id]
                for origin in origins:
                    file, origin_id = origin.split("/")

                    filepath = self.review_manager.search_dir / Path(file)

                    origin_file_content = filepath.read_text()
                    origin_records = self.review_manager.dataset.load_records_dict(
                        load_str=origin_file_content
                    )
                    if origin_id in origin_records:
                        del origin_records[origin_id]
                    self.review_manager.dataset.save_records_dict_to_file(
                        records=origin_records, save_path=filepath
                    )
                    self.review_manager.dataset.add_changes(path=filepath)

        self.review_manager.dataset.save_records_dict(records=records)
        self.review_manager.create_commit(msg="Remove records", manual_author=False)
