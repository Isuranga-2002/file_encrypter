import json
import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('EncryptionJobs')


def lambda_handler(event, context):

    from boto3.dynamodb.conditions import Key

    user_id = event['queryStringParameters']['userId']

    response = table.query(
        IndexName='userId-index',
        KeyConditionExpression=Key('userId').eq(user_id)
    )    

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'http://localhost:4200'
        },
        'body': json.dumps(response['Items'])
    }