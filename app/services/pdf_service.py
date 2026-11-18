from pypdf import PdfReader
import io

class PdfService:
    
    def read(self, content: bytes):
        pdf_stream = io.BytesIO(content)
        pdf_reader = PdfReader(pdf_stream)

        pdf_content = ""
        for i, page in enumerate(pdf_reader.pages):
            page_content = page.extract_text()
            if page_content:
                pdf_content += page_content
        return pdf_content if pdf_content else None