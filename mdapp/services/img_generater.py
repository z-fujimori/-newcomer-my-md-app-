from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
import boto3

def generate_image_from_pdf(bytes_pdf, title):
    """
    PDFファイルから画像を生成する関数
    :param pdf_file: PDFファイルのバイナリデータ
    :return: 生成された画像のバイナリデータ
    """
    # images = convert_from_bytes(pdf_file.read())
    images = convert_from_bytes(bytes_pdf, dpi=200, first_page=1, last_page=1)
    full_img = images[0]
    width, height = full_img.size

    # 上部200ピクセルをトリミング
    cropped = full_img.crop((0, 150, width, 1400))

    buffer = BytesIO()
    cropped.save(buffer, format='JPEG')
    buffer.seek(0)

    s3 = boto3.client('s3')  # region_name を明示しても良い

    s3.upload_fileobj(
        Fileobj=buffer,
        Bucket='your-bucket-name',
        Key='images/output.png',
        ExtraArgs={'ContentType': 'image/png'}
    )

    url = "aa"
    
    return url
