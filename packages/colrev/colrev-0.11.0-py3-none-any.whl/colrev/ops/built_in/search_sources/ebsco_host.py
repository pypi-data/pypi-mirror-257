#! /usr/bin/env python
"""SearchSource: EBSCOHost"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import zope.interface
from dacite import from_dict
from dataclasses_jsonschema import JsonSchemaMixin

import colrev.env.package_manager
import colrev.ops.load_utils_bib
import colrev.ops.load_utils_table
import colrev.ops.search
import colrev.record
from colrev.constants import Fields
from colrev.constants import FieldValues

# pylint: disable=unused-argument
# pylint: disable=duplicate-code


@zope.interface.implementer(
    colrev.env.package_manager.SearchSourcePackageEndpointInterface
)
@dataclass
class EbscoHostSearchSource(JsonSchemaMixin):
    """EBSCOHost"""

    settings_class = colrev.env.package_manager.DefaultSourceSettings

    endpoint = "colrev.ebsco_host"
    # https://connect.ebsco.com/s/article/
    # What-is-the-Accession-Number-AN-in-EBSCOhost-records?language=en_US
    # Note : ID is the accession number.
    source_identifier = "{{ID}}"
    search_types = [colrev.settings.SearchType.DB]

    ci_supported: bool = False
    heuristic_status = colrev.env.package_manager.SearchSourceHeuristicStatus.supported
    short_name = "EBSCOHost"
    docs_link = (
        "https://github.com/CoLRev-Environment/colrev/blob/main/"
        + "colrev/ops/built_in/search_sources/ebsco_host.md"
    )
    db_url = "https://search.ebscohost.com/"

    def __init__(
        self, *, source_operation: colrev.operation.Operation, settings: dict
    ) -> None:
        self.search_source = from_dict(data_class=self.settings_class, data=settings)
        self.review_manager = source_operation.review_manager
        self.source_operation = source_operation

    @classmethod
    def heuristic(cls, filename: Path, data: str) -> dict:
        """Source heuristic for EBSCOHost"""

        result = {"confidence": 0.0}

        if data.count("@") >= 1:
            if "URL = {https://search.ebscohost.com/" in data:
                if re.match(r"@.*{\d{17}\,\n", data):
                    result["confidence"] = 1.0

        return result

    @classmethod
    def add_endpoint(
        cls,
        operation: colrev.ops.search.Search,
        params: dict,
    ) -> colrev.settings.SearchSource:
        """Add SearchSource as an endpoint"""

        return operation.add_db_source(
            search_source_cls=cls,
            params=params,
        )

    def run_search(self, rerun: bool) -> None:
        """Run a search of EbscoHost"""

        if self.search_source.search_type == colrev.settings.SearchType.DB:
            self.source_operation.run_db_search(  # type: ignore
                search_source_cls=self.__class__,
                source=self.search_source,
            )
            return

        raise NotImplementedError

    def get_masterdata(
        self,
        prep_operation: colrev.ops.prep.Prep,
        record: colrev.record.Record,
        save_feed: bool = True,
        timeout: int = 10,
    ) -> colrev.record.Record:
        """Not implemented"""
        return record

    def load(self, load_operation: colrev.ops.load.Load) -> dict:
        """Load the records from the SearchSource file"""

        if self.search_source.filename.suffix == ".bib":
            bib_loader = colrev.ops.load_utils_bib.BIBLoader(
                load_operation=load_operation, source=self.search_source
            )
            records = bib_loader.load_bib_file()
            return records

        if self.search_source.filename.suffix == ".csv":
            table_loader = colrev.ops.load_utils_table.TableLoader(
                load_operation=load_operation, source=self.search_source
            )
            table_entries = table_loader.load_table_entries()
            records = table_loader.convert_to_records(entries=table_entries)
            return records

        raise NotImplementedError

    def prepare(
        self, record: colrev.record.PrepRecord, source: colrev.settings.SearchSource
    ) -> colrev.record.Record:
        """Source-specific preparation for EBSCOHost"""

        record.format_if_mostly_upper(key=Fields.AUTHOR, case=Fields.TITLE)
        record.format_if_mostly_upper(key=Fields.TITLE, case=Fields.TITLE)

        if record.data.get(Fields.PAGES) == "N.PAG -- N.PAG":
            record.data[Fields.PAGES] = FieldValues.UNKNOWN

        record.fix_name_particles()

        return record
