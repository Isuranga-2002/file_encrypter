import json
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('EncryptionJobs')


def lambda_handler(event, context):

    response = table.scan()

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'http://localhost:4200'
        },
        'body': json.dumps(response['Items'])
    }