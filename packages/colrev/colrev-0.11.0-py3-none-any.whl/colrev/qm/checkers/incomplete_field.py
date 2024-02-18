#! /usr/bin/env python
"""Checker for incomplete fields."""
from __future__ import annotations

import colrev.qm.quality_model
from colrev.constants import DefectCodes
from colrev.constants import Fields
from colrev.constants import FieldValues

# pylint: disable=too-few-public-methods


class IncompleteFieldChecker:
    """The IncompleteFieldChecker"""

    msg = DefectCodes.INCOMPLETE_FIELD

    def __init__(self, quality_model: colrev.qm.quality_model.QualityModel) -> None:
        self.quality_model = quality_model

    def run(self, *, record: colrev.record.Record) -> None:
        """Run the missing-field checks"""

        for key in [
            Fields.TITLE,
            Fields.JOURNAL,
            Fields.BOOKTITLE,
            Fields.AUTHOR,
            Fields.ABSTRACT,
        ]:
            if (
                self.__institutional_author(key=key, record=record)
                or record.data.get(key, FieldValues.UNKNOWN) == FieldValues.UNKNOWN
                or record.ignored_defect(field=key, defect=self.msg)
            ):
                continue
            if self.__incomplete_field(record=record, key=key):
                record.add_masterdata_provenance_note(key=key, note=self.msg)
            else:
                record.remove_masterdata_provenance_note(key=key, note=self.msg)

    def __incomplete_field(self, *, record: colrev.record.Record, key: str) -> bool:
        """check for incomplete field"""
        if record.data[key].endswith("...") or record.data[key].endswith("…"):
            return True
        return key == Fields.AUTHOR and (
            # heuristics for missing first names:
            ", and " in record.data[key]
            or record.data[key].rstrip().endswith(",")
            or "," not in record.data[key]
        )

    def __institutional_author(self, *, key: str, record: colrev.record.Record) -> bool:
        if key != Fields.AUTHOR or Fields.AUTHOR not in record.data:
            return False
        if record.data[Fields.AUTHOR].startswith("{") and record.data[
            Fields.AUTHOR
        ].endswith("}"):
            return True
        return False


def register(quality_model: colrev.qm.quality_model.QualityModel) -> None:
    """Register the checker"""
    quality_model.register_checker(IncompleteFieldChecker(quality_model))
