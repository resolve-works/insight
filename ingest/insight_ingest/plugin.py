import re
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ocrmypdf import hookimpl
from ocrmypdf.builtin_plugins.tesseract_ocr import TesseractOcrEngine
from .models import Page

engine = create_engine(os.environ.get("POSTGRES_URI"))


def get_page_number(output_text):
    # /tmp/ocrmypdf.io.20wy83mv/000003_ocr_tess.txt
    return re.search(r"^.+/(\d+)_ocr_tess.txt$", str(output_text)).group(1)


class InsightEngine(TesseractOcrEngine):
    @staticmethod
    def generate_pdf(input_file, output_pdf, output_text, options):
        TesseractOcrEngine.generate_pdf(input_file, output_pdf, output_text, options)

        with Session(engine) as session:
            page_number = get_page_number(output_text)
            index = int(options.from_page) + int(page_number) - 1
            page = Page(
                pagestream_id=options.pagestream_id,
                index=index,
                contents=output_text.read_text(),
            )
            session.add(page)
            session.commit()


@hookimpl
def get_ocr_engine():
    return InsightEngine()


@hookimpl
def add_options(parser):
    parser.add_argument("--pagestream-id", help="UUID identifying pagestream")
    parser.add_argument("--from-page", help="Start of document in pagestream")
