import re
from pathlib import Path

from ocrmypdf import hookimpl
from ocrmypdf.builtin_plugins.tesseract_ocr import TesseractOcrEngine


def get_page_index(output_text):
    # /tmp/ocrmypdf.io.20wy83mv/000003_ocr_tess.txt
    return int(re.search(r"^.+(\d+)_ocr_tess.txt$", str(output_text)).group(1)) - 1


class InsightEngine(TesseractOcrEngine):
    @staticmethod
    def generate_pdf(input_file, output_pdf, output_text, options):
        print(f"{options.file_id} - Page {get_page_index(output_text)}")
        TesseractOcrEngine.generate_pdf(input_file, output_pdf, output_text, options)


@hookimpl
def get_ocr_engine():
    return InsightEngine()


@hookimpl
def add_options(parser):
    parser.add_argument("--file-id", help="UUID identifying file")
