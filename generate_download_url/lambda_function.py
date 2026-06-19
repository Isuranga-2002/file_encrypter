import json
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('EncryptionJobs')

s3_client = boto3.client('s3')

DESTINATION_BUCKET = 'isuranga-destination-bucket-file-encrypter'


def lambda_handler(event, context):

    job_id = event['pathParameters']['jobId']

    response = table.get_item(
        Key={
            'jobId': job_id
        }
    )

    item = response.get('Item')

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': 'Job not found'
            })
        }

    if item.get('status') != 'COMPLETED':
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'File not ready'
            })
        }

    download_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': DESTINATION_BUCKET,
            'Key': item['encryptedKey']
        },
        ExpiresIn=300
    )

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'http://localhost:4200'
        },
        'body': json.dumps({
            'downloadUrl': download_url
        })
    }