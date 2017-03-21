from __future__ import print_function
import boto3
import uuid
import re
from PIL import Image
import PIL.Image
from StringIO import StringIO
import base64

s3 = boto3.client('s3')

def handler(event, context):
    bucket = event['params']['bucket']
    key = event['params']['key']
    image_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
    
    sizeRegex = re.compile('_\w{2}')
    size = sizeRegex.search(key)
    ext = size.group()
    newkey = key.replace(ext,'')
    
    if ext == '_th':
        maxsize = (233,233)
    elif ext == '_sm':
        maxsize = (360,360)
    elif ext == '_md': 
        maxsize = (600,600)
    elif ext == '_lg':
        maxsize = (780,780)
    
    s3.download_file(bucket,newkey,image_path)
    
    image = Image.open(image_path)
    image.thumbnail(maxsize, PIL.Image.ANTIALIAS)
    output = StringIO()
    image.save(output,'PNG')
    output.seek(0)
    output_str = output.read()
    imageb64 = base64.b64encode(output_str)
    
    return imageb64
   