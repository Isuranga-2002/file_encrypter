import json
import boto3
import uuid

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EncryptionJobs')

# S3
s3_client = boto3.client('s3')

SOURCE_BUCKET = 'isuranga-source-bucket-file-encrypter'


def lambda_handler(event, context):

    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))

        filename = body.get('filename')

        if not filename:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': 'http://localhost:4200',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'POST, OPTIONS'
                },
                'body': json.dumps({
                    'message': 'filename is required'
                })
            }

        # Generate Job ID
        job_id = str(uuid.uuid4())

        # Create unique S3 object key
        file_key = f"uploads/{job_id}/{filename}"

        # Save record in DynamoDB
        table.put_item(
            Item={
                'jobId': job_id,
                'fileName': filename,
                'fileKey': file_key,
                'status': 'PROCESSING'
            }
        )

        # Generate pre-signed upload URL
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
                'jobId': job_id,
                'uploadUrl': upload_url,
                'fileKey': file_key
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': 'http://localhost:4200',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'message': str(e)
            })
        }