import json
import boto3
import uuid

s3_client = boto3.client('s3')

SOURCE_BUCKET = 'isuranga-source-bucket-file-encrypter'

def lambda_handler(event, context):

    body = json.loads(event.get('body', '{}'))

    filename = body.get('filename')

    if not filename:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'filename is required'
            })
        }

    file_key = f"uploads/{uuid.uuid4()}-{filename}"

    upload_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket': SOURCE_BUCKET,
            'Key': file_key
        },
        ExpiresIn=300
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'http://localhost:4200',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps({
            'uploadUrl': upload_url,
            'fileKey': file_key
        })
    }