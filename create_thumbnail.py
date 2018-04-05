import boto3
import os
import sys
import urllib
from PIL import Image
import PIL.Image

s3_client = boto3.client('s3')

'''
A simple utility to resize an image from one S3 bucket to S3 bucket. This sits in an lambda function.
'''

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128,128))
        image.save(resized_path)

def handler(event, context):
    '''
    the lambda function downloads to a local, resizes and uploads the resized image to the resized bucket.
    :param event : each record contains the name of the incoming object
    '''
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        raw_key = urllib.parse.unquote_plus(key)
        download_path = '/tmp/{}'.format(key)
        upload_path = '/tmp/resized-{}'.format(key)

        s3_client.download_file(bucket, raw_key, download_path)
        resize_image(download_path, upload_path)
        s3_client.upload_file(upload_path,
             '{}-resized'.format(bucket),
             'thumbnail-{}'.format(raw_key),
             ExtraArgs={'ContentType': 'image/jpeg'})
