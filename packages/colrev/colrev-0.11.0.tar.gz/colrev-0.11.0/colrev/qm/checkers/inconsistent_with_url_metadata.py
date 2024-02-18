#! /usr/bin/env python
"""Checker for inconsistent-with-url-metadata."""
from __future__ import annotations

from rapidfuzz import fuzz

import colrev.ops.built_in.search_sources.website as website_connector
import colrev.qm.quality_model
from colrev.constants import DefectCodes
from colrev.constants import Fields

# pylint: disable=too-few-public-methods


class InconsistentWithURLMetadataChecker:
    """The InconsistentWithURLMetadataChecker"""

    msg = DefectCodes.INCONSISTENT_WITH_URL_METADATA
    __fields_to_check = [
        Fields.AUTHOR,
        Fields.TITLE,
        Fields.JOURNAL,
        Fields.YEAR,
        Fields.VOLUME,
        Fields.NUMBER,
    ]

    def __init__(self, quality_model: colrev.qm.quality_model.QualityModel) -> None:
        self.quality_model = quality_model

        self.__url_connector = website_connector.WebsiteConnector(
            review_manager=quality_model.review_manager
        )

    def run(self, *, record: colrev.record.Record) -> None:
        """Run the inconsistent-with-url-metadata checks"""

        if Fields.URL not in record.data or record.ignored_defect(
            field=Fields.URL, defect=self.msg
        ):
            return
        if any(x in record.data[Fields.URL] for x in ["search.ebscohost.com/login"]):
            return
        if "md_curated.bib" in record.data[Fields.D_PROV][Fields.URL]["source"]:
            return

        if self.__url_metadata_conflicts(record=record):
            record.add_masterdata_provenance_note(key=Fields.URL, note=self.msg)
        else:
            record.remove_masterdata_provenance_note(key=Fields.URL, note=self.msg)

    def __url_metadata_conflicts(self, *, record: colrev.record.Record) -> bool:
        url_record = record.copy_prep_rec()
        self.__url_connector.retrieve_md_from_website(record=url_record)
        for key, value in url_record.data.items():
            if key not in self.__fields_to_check:
                continue
            if not isinstance(value, str):
                continue
            if key in record.data:
                if len(url_record.data[key]) < 5 or len(record.data[key]) < 5:
                    continue
                if (
                    fuzz.partial_ratio(
                        record.data[key].lower(), url_record.data[key].lower()
                    )
                    < 70
                ):
                    return True

        return False


def register(quality_model: colrev.qm.quality_model.QualityModel) -> None:
    """Register the checker"""
    quality_model.register_checker(InconsistentWithURLMetadataChecker(quality_model))
