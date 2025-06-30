from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
import boto3
from django.conf import settings
import os

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

    # imgを作成してローカルに保存
    # url = store_local(cropped, title)
    # S3に保存
    url = store_s3(cropped, title)
    print("URL: ", url)
    
    return url

def generate_image_from_pdf_local(bytes_pdf, title, name):
    images = convert_from_bytes(bytes_pdf, dpi=200, first_page=1, last_page=1)
    full_img = images[0]
    width, height = full_img.size
    cropped = full_img.crop((0, 150, width, 1400))
    url = store_local(cropped, title, name)
    
    return url

def store_local(cropped, title, name):
    directory = "mdapp/static/mdapp/img/thumbs"
    os.makedirs(directory, exist_ok=True)
    cropped.save(os.path.join(directory, f"{title}_{name}.jpeg"))
    return f"http://127.0.0.1:8000/img/{title}_{name}.jpeg"

def store_s3(cropped, title):
    buffer = BytesIO()
    cropped.save(buffer, format='JPEG')
    buffer.seek(0)

    s3 = boto3.client('s3', region_name='ap-northeast-1')
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    object_key = f"images/{title}.jpeg"
    res = s3.upload_fileobj(
        Fileobj=buffer,
        Bucket = bucket_name,
        Key = object_key,
        ExtraArgs = {'ContentType': 'image/jpeg'}
    )
    print(res)

    url = f"https://{bucket_name}.s3.{s3.meta.region_name}.amazonaws.com/{object_key}"

    return url
