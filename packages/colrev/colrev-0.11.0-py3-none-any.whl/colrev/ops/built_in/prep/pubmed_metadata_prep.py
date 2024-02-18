#! /usr/bin/env python
"""Consolidation of metadata based on the Pubmed API as a prep operation"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import zope.interface
from dataclasses_jsonschema import JsonSchemaMixin

import colrev.env.package_manager
import colrev.ops.built_in.search_sources.pubmed as pubmed_connector
import colrev.ops.search_sources
import colrev.record
from colrev.constants import Fields

# pylint: disable=duplicate-code

if TYPE_CHECKING:
    import colrev.ops.prep

# pylint: disable=too-few-public-methods
# pylint: disable=duplicate-code


@zope.interface.implementer(colrev.env.package_manager.PrepPackageEndpointInterface)
@dataclass
class PubmedMetadataPrep(JsonSchemaMixin):
    """Prepares records based on Pubmed metadata"""

    settings_class = colrev.env.package_manager.DefaultSettings
    ci_supported: bool = True

    source_correction_hint = "ask the publisher to correct the metadata"
    always_apply_changes = False
    docs_link = (
        "https://github.com/CoLRev-Environment/colrev/blob/main/"
        + "colrev/ops/built_in/search_sources/pubmed.md"
    )

    def __init__(
        self,
        *,
        prep_operation: colrev.ops.prep.Prep,
        settings: dict,
    ) -> None:
        self.settings = self.settings_class.load_settings(data=settings)
        self.prep_operation = prep_operation

        self.pubmed_source = pubmed_connector.PubMedSearchSource(
            source_operation=prep_operation
        )

        self.pubmed_prefixes = [
            s.get_origin_prefix()
            for s in prep_operation.review_manager.settings.sources
            if s.endpoint == "colrev.pubmed"
        ]

    def check_availability(
        self, *, source_operation: colrev.operation.Operation
    ) -> None:
        """Check status (availability) of the Pubmed API"""
        self.pubmed_source.check_availability(source_operation=source_operation)

    def prepare(self, record: colrev.record.PrepRecord) -> colrev.record.Record:
        """Prepare a record based on Pubmed metadata"""

        if any(
            pubmed_prefix in o
            for pubmed_prefix in self.pubmed_prefixes
            for o in record.data[Fields.ORIGIN]
        ):
            # Already linked to a pubmed record
            return record

        self.pubmed_source.get_masterdata(
            prep_operation=self.prep_operation, record=record
        )
        return record
