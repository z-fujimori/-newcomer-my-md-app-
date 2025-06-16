from pdf2image import convert_from_bytes
from PIL import Image
from io import BytesIO
import boto3
from django.conf import settings

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

    # url = store_local(cropped, title)
    url = store_s3(cropped, title)

    print("URL: ", url)
    
    return url

def store_local(cropped, title):
    cropped.save(f"{title}.jpeg")
    return 

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
