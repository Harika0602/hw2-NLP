from typing import Optional, Type, Any  # Add Any here
from pydantic import BaseModel, Field
import requests
import PyPDF2
from io import BytesIO
from gentopia.tools.basetool import BaseTool


class PDFReaderArgs(BaseModel):
    url: str = Field(..., description="URL of the PDF file")


class PDFReader(BaseTool):
    """Tool that reads a PDF file from a URL and extracts text content."""

    name = "pdf_reader"
    description = ("Reads a PDF file from a given URL and extracts its text content. "
                   "Input should be the URL of the PDF file.")

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    def _run(self, url: str) -> str:
        """Extract text from the specified PDF URL."""
        text = self.extract_text_from_pdf(url)
        return text

    def extract_text_from_pdf(self, url: str) -> str:
        """Download the PDF from the URL and return its text content."""
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            with BytesIO(response.content) as file:
                reader = PyPDF2.PdfReader(file)
                text = self.concatenate_text(reader)
            return text.strip()  # Trim whitespace
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    def concatenate_text(self, reader: PyPDF2.PdfReader) -> str:
        """Concatenate text from all pages in the PDF reader."""
        text = ''
        for page in reader.pages:
            page_text = page.extract_text() or ''  # Handle None case
            text += page_text + '\n'
        return text

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    pdf_reader = PDFReader()
    extracted_text = pdf_reader._run("hhttps://arxiv.org/pdf/2407.02067")
    print("Extracted Text from PDF:")
    print(extracted_text)
