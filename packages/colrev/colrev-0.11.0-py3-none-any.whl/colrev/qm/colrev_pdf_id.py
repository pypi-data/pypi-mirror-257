#! /usr/bin/env python
"""Creates CoLRev PDF hashes."""
from __future__ import annotations

import logging
import os
from pathlib import Path

import fitz
import imagehash
from PIL import Image

import colrev.exceptions as colrev_exceptions
from colrev.constants import Colors


def get_pdf_hash(*, pdf_path: Path, page_nr: int, hash_size: int = 32) -> str:
    """Get the PDF image hash"""
    assert page_nr > 0
    assert hash_size in [16, 32]
    pdf_path = pdf_path.resolve()
    if 0 == os.path.getsize(pdf_path):
        logging.error("%sPDF with size 0: %s %s", Colors.RED, pdf_path, Colors.END)
        raise colrev_exceptions.InvalidPDFException(path=pdf_path)

    try:
        doc: fitz.Document = fitz.open(pdf_path)
    except fitz.fitz.FileDataError as exc:
        raise colrev_exceptions.InvalidPDFException(path=pdf_path) from exc

    img = None
    file_name = f".{pdf_path.stem}-{page_nr}.png"
    page_no = 0
    try:
        for page in doc:
            pix = page.get_pixmap(dpi=200)
            pix.save(file_name)  # store image as a PNG
            page_no += 1
            if page_no == page_nr:
                img = Image.open(file_name)
                break
    except RuntimeError as exc:
        raise colrev_exceptions.PDFHashError(path=pdf_path) from exc
    average_hash = imagehash.average_hash(img, hash_size=int(hash_size))
    Path(file_name).unlink()
    average_hash_str = str(average_hash).replace("\n", "")
    if len(average_hash_str) * "0" == average_hash_str:
        raise colrev_exceptions.PDFHashError(path=pdf_path)

    return average_hash_str


def create_colrev_pdf_id(*, pdf_path: Path) -> str:
    """Get the PDF hash"""

    return "cpid2:" + get_pdf_hash(pdf_path=pdf_path, page_nr=1, hash_size=32)
