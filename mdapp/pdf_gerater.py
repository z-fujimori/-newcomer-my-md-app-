from django.contrib.staticfiles.finders import find as find_static
from django.http import HttpResponse
from weasyprint import HTML as HTMLtoPDF
# import pdfkit
# from spire.doc import Document
# from spire.doc import FileFormat
import io

def generater(html_text):
    css_path = find_static('mdapp/css/mdfile.css')
    if not css_path:
        return HttpResponse(
            f"CSSファイル処理エラー(ECSS1)",
            status=505
        )
        
    css_content = None
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        return HttpResponse(
            f"CSSファイル処理エラー(ECSS3): {e}",
            status=500
        )

    html_content = f"""<!DOCTYPE html><html><head><meta charset='utf-8'><title>PDF</title><style>{css_content}</style></head><body>{html_text}</body></html>"""
    pdf_buffer = io.BytesIO()
    try:
        # pdf_buffer = pdfkit.from_string(html_content, False)
        HTMLtoPDF(string=html_content).write_pdf(target=pdf_buffer)
        HTMLtoPDF(string=html_content).write_pdf(target="pdf_buffer.pdf")
        # print(html_content)
        # HTMLtoPDF(string=html_content).
        print("pdf が正常に生成されました")
        print(pdf_buffer)
        # print(pdf_data.write_pdf("test.pdf", stylesheets=[]))
    except Exception as e:
        print(f"PDF生成中にエラーが発生しました: {e}")
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()
