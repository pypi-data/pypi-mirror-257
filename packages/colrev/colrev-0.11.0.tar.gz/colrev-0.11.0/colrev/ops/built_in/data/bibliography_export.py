#! /usr/bin/env python
"""Export of references in different bibliographical formats as a data operation"""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

import click
import requests
import zope.interface
from dataclasses_jsonschema import JsonSchemaMixin

import colrev.constants as c
import colrev.env.package_manager
import colrev.env.utils
import colrev.exceptions as colrev_exceptions
import colrev.record
from colrev.constants import Fields

if TYPE_CHECKING:
    import colrev.ops.data


@dataclass
class BibFormats(Enum):
    """Enum of available bibliography formats"""

    # pylint: disable=invalid-name
    endnote = "endnote"
    zotero = "zotero"
    jabref = "jabref"
    mendeley = "mendeley"
    citavi = "citavi"
    rdf_bibliontology = "rdf_bibliontology"


@zope.interface.implementer(colrev.env.package_manager.DataPackageEndpointInterface)
@dataclass
class BibliographyExport(JsonSchemaMixin):
    """Export the sample references in Endpoint format"""

    settings: BibliographyExportSettings

    ZOTERO_FORMATS = [
        BibFormats.endnote,
        BibFormats.mendeley,
        BibFormats.rdf_bibliontology,
    ]
    PYBTEX_FORMATS = [BibFormats.citavi, BibFormats.jabref, BibFormats.zotero]

    ci_supported: bool = False

    @dataclass
    class BibliographyExportSettings(
        colrev.env.package_manager.DefaultSettings, JsonSchemaMixin
    ):
        """Settings for BibliographyExport"""

        endpoint: str
        version: str
        bib_format: BibFormats

    # A challenge for the incremental mode is that data is run every time
    # the status runs (potentially creating very small increments)

    settings_class = BibliographyExportSettings

    def __init__(
        self,
        *,
        data_operation: colrev.ops.data.Data,
        settings: dict,
    ) -> None:
        self.review_manager = data_operation.review_manager

        if "bib_format" not in settings:
            settings["bib_format"] = "endnote"
        settings["bib_format"] = BibFormats[settings["bib_format"]]
        if "version" not in settings:
            settings["version"] = "0.1"

        self.settings = self.settings_class.load_settings(data=settings)
        self.endpoint_path = self.review_manager.output_dir

        if not self.review_manager.in_ci_environment():
            self.review_manager.get_zotero_translation_service()

    def __pybtex_conversion(self, *, selected_records: dict) -> None:
        self.review_manager.logger.info(f"Export {self.settings.bib_format.name}")

        if self.settings.bib_format is BibFormats.zotero:
            export_filepath = self.endpoint_path / Path("zotero.bib")

        elif self.settings.bib_format is BibFormats.jabref:
            export_filepath = self.endpoint_path / Path("jabref.bib")

        elif self.settings.bib_format is BibFormats.citavi:
            export_filepath = self.endpoint_path / Path("citavi.bib")

        self.review_manager.dataset.save_records_dict_to_file(
            records=selected_records, save_path=export_filepath
        )
        self.review_manager.dataset.add_changes(path=export_filepath)
        self.review_manager.create_commit(
            msg=f"Create {self.settings.bib_format.name} bibliography",
        )

    def __zotero_conversion(self, *, selected_records: dict) -> None:
        self.review_manager.logger.info(f"Export {self.settings.bib_format.name}")

        # https://github.com/zotero/translation-server/blob/master/src/formats.js
        if self.settings.bib_format is BibFormats.endnote:
            # Note: endnote .enl file is a binary:
            # https://docs.fileformat.com/misc/enl/
            export_filepath = self.endpoint_path / Path("endnote.xml")
            selected_format = "endnote_xml"
            self.review_manager.logger.info(
                "Import as Endnote-generated XML into an existing database"
            )

        elif self.settings.bib_format is BibFormats.mendeley:
            export_filepath = self.endpoint_path / Path("mendeley.ris")
            selected_format = "ris"

        else:
            self.review_manager.logger.info(
                f"Format {self.settings.bib_format} not supported."
            )
            return

        content = self.review_manager.dataset.parse_bibtex_str(
            recs_dict_in=selected_records
        )

        zotero_translation_service = (
            self.review_manager.get_zotero_translation_service()
        )
        zotero_translation_service.start()

        headers = {"Content-type": "text/plain"}
        ret = requests.post(
            "http://127.0.0.1:1969/import",
            headers=headers,
            files={Fields.FILE: str.encode(content)},
            timeout=30,
        )
        headers = {"Content-type": "application/json"}
        if ret.content.decode("utf-8") == "No suitable translators found":
            raise colrev_exceptions.ImportException(
                "Zotero translators: No suitable translators found"
            )

        try:
            json_content = json.loads(ret.content)
            export = requests.post(
                f"http://127.0.0.1:1969/export?format={selected_format}",
                headers=headers,
                json=json_content,
                timeout=30,
            )
            # overwrite the file if it exists
            with open(export_filepath, "w", encoding="utf-8") as export_file:
                export_file.write(export.content.decode("utf-8"))
            self.review_manager.dataset.add_changes(path=export_filepath)

            self.review_manager.create_commit(
                msg=f"Create {self.settings.bib_format.name} bibliography",
            )

        except Exception as exc:
            raise colrev_exceptions.ImportException(
                f"Zotero translators failed ({exc})"
            )

    @classmethod
    def add_endpoint(cls, operation: colrev.ops.data.Data, params: str) -> None:
        """Add bibliography as an endpoint"""

        add_source = {
            "endpoint": "colrev.bibliography_export",
            "version": "0.1",
            "bib_format": "endnote",
        }

        if params:
            add_source["bib_format"] = params
        else:
            choice = click.prompt(
                "Select a bibliography format",
                type=click.Choice([b.value for b in BibFormats]),
            )
            add_source["bib_format"] = choice

        operation.review_manager.settings.data.data_package_endpoints.append(add_source)

    # pylint: disable=unused-argument
    def update_data(
        self,
        records: dict,
        synthesized_record_status_matrix: dict,
        silent_mode: bool,
    ) -> None:
        """Update the data/bibliography"""

        self.endpoint_path.mkdir(exist_ok=True, parents=True)

        selected_records_original = {
            ID: r
            for ID, r in records.items()
            if r[Fields.STATUS]
            in [
                colrev.record.RecordState.rev_included,
                colrev.record.RecordState.rev_synthesized,
            ]
        }
        selected_records = copy.deepcopy(selected_records_original)
        for record in selected_records.values():
            for key_candidate in list(record.keys()):
                if key_candidate not in c.FieldSet.IDENTIFYING_FIELD_KEYS + [
                    Fields.ENTRYTYPE,
                    Fields.ID,
                    Fields.FILE,
                    "link",
                    Fields.URL,
                ]:
                    del record[key_candidate]
            # TBD: maybe resolve file paths (symlinks to absolute paths)?

        if any(self.settings.bib_format is x for x in self.ZOTERO_FORMATS):
            self.__zotero_conversion(selected_records=selected_records)

        elif any(self.settings.bib_format is x for x in self.PYBTEX_FORMATS):
            self.__pybtex_conversion(selected_records=selected_records)

        else:
            self.review_manager.logger.info(
                f"Not yet implemented ({self.settings.bib_format})"
            )

    def update_record_status_matrix(
        self,
        synthesized_record_status_matrix: dict,
        endpoint_identifier: str,
    ) -> None:
        """Update the record_status_matrix"""
        # Note : automatically set all to True / synthesized
        for syn_id in list(synthesized_record_status_matrix.keys()):
            synthesized_record_status_matrix[syn_id][endpoint_identifier] = True

    def get_advice(
        self,
    ) -> dict:
        """Get advice on the next steps (for display in the colrev status)"""

        data_endpoint = "Data operation [bibliography export data endpoint]: "

        advice = {
            "msg": f"{data_endpoint}"
            + f"\n    - The references are updated automatically ({self.endpoint_path})",
            "detailed_msg": "TODO",
        }
        return advice
