#! /usr/bin/env python
"""Consolidation of metadata based on CiteAs API as a prep operation"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

import requests
import zope.interface
from dataclasses_jsonschema import JsonSchemaMixin

import colrev.env.package_manager
import colrev.exceptions as colrev_exceptions
import colrev.ops.search_sources
import colrev.record
from colrev.constants import Fields

if TYPE_CHECKING:
    import colrev.ops.prep

# pylint: disable=too-few-public-methods
# pylint: disable=duplicate-code


@zope.interface.implementer(colrev.env.package_manager.PrepPackageEndpointInterface)
@dataclass
class CiteAsPrep(JsonSchemaMixin):
    """Prepares records based on citeas.org metadata"""

    settings_class = colrev.env.package_manager.DefaultSettings

    source_correction_hint = "Search on https://citeas.org/ and click 'modify'"
    always_apply_changes = False
    ci_supported: bool = True

    def __init__(
        self,
        *,
        prep_operation: colrev.ops.prep.Prep,
        settings: dict,
    ) -> None:
        self.settings = self.settings_class.load_settings(data=settings)
        self.prep_operation = prep_operation
        self.review_manager = prep_operation.review_manager
        self.same_record_type_required = (
            prep_operation.review_manager.settings.is_curated_masterdata_repo()
        )
        self.session = prep_operation.review_manager.get_cached_session()
        _, self.email = prep_operation.review_manager.get_committer()

    def __cite_as_json_to_record(
        self, *, json_str: str, url: str
    ) -> colrev.record.PrepRecord:
        retrieved_record: dict = {}
        data = json.loads(json_str)

        if Fields.AUTHOR in data["metadata"]:
            authors = data["metadata"][Fields.AUTHOR]
            authors_string = ""
            for author in authors:
                authors_string += author.get("family", "") + ", "
                authors_string += author.get("given", "") + " "
            authors_string = authors_string.lstrip().rstrip().replace("  ", " ")
            retrieved_record.update(author=authors_string)
        if "container-title" in data["metadata"]:
            container_title = data["metadata"]["container-title"]
            if isinstance(data["metadata"]["container-title"], list):
                container_title = "".join(data["metadata"]["container-title"])
            retrieved_record.update(title=container_title)
        if "URL" in data["metadata"]:
            retrieved_record.update(url=data["metadata"]["URL"])
        if "note" in data["metadata"]:
            retrieved_record.update(note=data["metadata"]["note"])
        if "type" in data["metadata"]:
            retrieved_record.update(ENTRYTYPE=data["metadata"]["type"])
        if Fields.YEAR in data["metadata"]:
            retrieved_record.update(year=data["metadata"][Fields.YEAR])
        if "DOI" in data["metadata"]:
            retrieved_record.update(doi=data["metadata"]["DOI"])

        record = colrev.record.PrepRecord(data=retrieved_record)
        record.add_provenance_all(source=url)
        return record

    def prepare(self, record: colrev.record.PrepRecord) -> colrev.record.Record:
        """Prepare the record based on citeas"""

        if record.data.get(Fields.ENTRYTYPE, "NA") not in ["misc", "software"]:
            return record
        if Fields.TITLE not in record.data:
            return record

        try:
            url = (
                f"https://api.citeas.org/product/{record.data['title']}?"
                + f"email={self.email}"
            )
            ret = self.session.request(
                "GET",
                url,
                headers=self.prep_operation.requests_headers,
                timeout=self.prep_operation.timeout,
            )
            ret.raise_for_status()

            retrieved_record = self.__cite_as_json_to_record(json_str=ret.text, url=url)

            similarity = colrev.record.PrepRecord.get_retrieval_similarity(
                record_original=retrieved_record,
                retrieved_record_original=retrieved_record,
                same_record_type_required=self.same_record_type_required,
            )
            if similarity > self.prep_operation.retrieval_similarity:
                record.merge(merging_record=retrieved_record, default_source=url)

        except (requests.exceptions.RequestException, colrev_exceptions.InvalidMerge):
            pass
        except UnicodeEncodeError:
            self.review_manager.logger.error(
                "UnicodeEncodeError - this needs to be fixed at some time"
            )

        return record
