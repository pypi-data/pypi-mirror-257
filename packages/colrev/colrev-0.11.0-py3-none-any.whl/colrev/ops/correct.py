#!/usr/bin/env python3
"""Create and apply record corrections in source repositories."""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from dictdiffer import diff

import colrev.record
from colrev.constants import Fields

if TYPE_CHECKING:
    import colrev.review_manager

# pylint: disable=too-few-public-methods


class Corrections:
    """Handling corrections of metadata"""

    # pylint: disable=duplicate-code
    essential_md_keys = [
        Fields.TITLE,
        Fields.AUTHOR,
        Fields.JOURNAL,
        Fields.YEAR,
        Fields.BOOKTITLE,
        Fields.NUMBER,
        Fields.VOLUME,
        Fields.AUTHOR,
        Fields.DOI,
        Fields.ORIGIN,  # Note : for merges
    ]

    keys_to_ignore = [
        Fields.ID,
        Fields.SCREENING_CRITERIA,
        Fields.STATUS,
        "source_url",
        "metadata_source_repository_paths",
        "grobid-version",
        "colrev_pdf_id",
        Fields.FILE,
        Fields.ORIGIN,
        Fields.D_PROV,
        Fields.MD_PROV,
        Fields.SEMANTIC_SCHOLAR_ID,
        Fields.CITED_BY,
        Fields.ABSTRACT,
        Fields.PAGES,
    ]

    def __init__(
        self,
        *,
        review_manager: colrev.review_manager.ReviewManager,
    ) -> None:
        self.review_manager = review_manager
        self.local_index = self.review_manager.get_local_index()
        self.resources = self.review_manager.get_resources()

    def __record_corrected(self, *, prior_r: dict, record_dict: dict) -> bool:
        return not all(
            prior_r.get(k, "NA") == record_dict.get(k, "NA")
            for k in self.essential_md_keys
        )

    def __prep_for_change_item_creation(
        self, *, original_record: dict, corrected_record: dict
    ) -> None:
        # Cast to string for persistence
        original_record = {k: str(v) for k, v in original_record.items()}
        corrected_record = {k: str(v) for k, v in corrected_record.items()}

        # Note : removing the fields is a temporary fix
        # because the subsetting of change_items does not seem to
        # work properly
        keys_to_drop = [Fields.PAGES, Fields.STATUS]
        for k in keys_to_drop:
            original_record.pop(k, None)
            corrected_record.pop(k, None)

        # if Fields.DBLP_KEY in corrected_record:
        #     del corrected_record[Fields.DBLP_KEY]

    def __create_change_item(
        self,
        *,
        original_record: dict,
        corrected_record: dict,
    ) -> None:
        # pylint: disable=too-many-branches

        self.__prep_for_change_item_creation(
            original_record=original_record,
            corrected_record=corrected_record,
        )

        changes = diff(original_record, corrected_record)

        selected_change_items = []
        for change_item in list(changes):
            change_type, key, val = change_item

            if not isinstance(key, str):
                continue

            if change_type != "add" and key == "":
                continue

            if key.split(".")[0] in self.keys_to_ignore:
                continue

            if change_type == "add":
                for add_item in val:
                    add_item_key, add_item_val = add_item
                    if not isinstance(add_item_key, str):
                        break
                    if add_item_key.split(".")[0] in self.keys_to_ignore:
                        break
                    selected_change_items.append(
                        ("add", "", [(add_item_key, add_item_val)])
                    )

            elif change_type == "change":
                selected_change_items.append(change_item)

        if len(selected_change_items) == 0:
            return

        if len(corrected_record.get(Fields.ORIGIN, [])) > len(
            original_record.get(Fields.ORIGIN, [])
        ):
            if (
                Fields.DBLP_KEY in corrected_record
                and Fields.DBLP_KEY in original_record
            ):
                if (
                    corrected_record[Fields.DBLP_KEY]
                    != original_record[Fields.DBLP_KEY]
                ):
                    selected_change_items = {  # type: ignore
                        "merge": [
                            corrected_record[Fields.DBLP_KEY],
                            original_record[Fields.DBLP_KEY],
                        ]
                    }
            # else:
            #     selected_change_items = {
            #         "merge": [
            #             corrected_record[Fields.ID],
            #             original_record[Fields.ID],
            #         ]
            #     }

        # gh_issue https://github.com/CoLRev-Environment/colrev/issues/63
        # cover non-masterdata corrections
        if Fields.MD_PROV not in original_record:
            return

        dict_to_save = {
            # "source_url": original_record[Fields.MD_PROV],
            "original_record": {
                k: v for k, v in original_record.items() if k not in [Fields.STATUS]
            },
            "changes": selected_change_items,
        }

        filepath = self.review_manager.corrections_path / Path(
            f"{corrected_record['ID']}.json"
        )
        filepath.parent.mkdir(exist_ok=True)

        with open(filepath, "w", encoding="utf8") as corrections_file:
            json.dump(dict_to_save, corrections_file, indent=4)

        # gh_issue https://github.com/CoLRev-Environment/colrev/issues/63
        # combine merge-record corrections

    def check_corrections_of_records(self) -> None:
        """Check for corrections of records"""

        # to test run
        # colrev-hooks-report .report.log

        dataset = self.review_manager.dataset

        if not dataset.records_file.is_file():
            return

        records = self.review_manager.dataset.load_records_dict()

        prior_records_dict = next(
            self.review_manager.dataset.load_records_from_history()
        )
        # gh_issue https://github.com/CoLRev-Environment/colrev/issues/63
        # The following code should be much simpler...
        for record_dict in records.values():
            # gh_issue https://github.com/CoLRev-Environment/colrev/issues/63
            # use origin-indexed dict (discarding changes during merges)

            # identify curated records for which essential metadata is changed
            record_prior = [
                x
                for x in prior_records_dict.values()
                if any(y in record_dict[Fields.ORIGIN] for y in x[Fields.ORIGIN])
            ]

            if len(record_prior) == 0:
                self.review_manager.logger.debug("No prior records found")
                continue

            for prior_r in record_prior:
                if self.__record_corrected(prior_r=prior_r, record_dict=record_dict):
                    corrected_record = record_dict.copy()

                    # original_record = (
                    #     self.__get_original_record_from_index(prior_r=prior_r)
                    # )
                    # if not original_record:
                    #     continue

                    self.__create_change_item(
                        original_record=prior_r,
                        corrected_record=corrected_record,
                    )
