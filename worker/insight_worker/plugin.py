import re
import os

from ocrmypdf import hookimpl
from ocrmypdf.builtin_plugins.tesseract_ocr import TesseractOcrEngine


class InsightEngine(TesseractOcrEngine):
    @staticmethod
    def generate_pdf(input_file, output_pdf, output_text, options):
        TesseractOcrEngine.generate_pdf(input_file, output_pdf, output_text, options)


@hookimpl
def get_ocr_engine():
    return InsightEngine()


# @hookimpl
# def add_options(parser):
# parser.add_argument("--file-id", help="UUID identifying file")
# parser.add_argument("--from-page", help="Start of document in file")
