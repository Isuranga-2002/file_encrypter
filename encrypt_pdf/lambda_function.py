from pypdf import PdfReader, PdfWriter
import uuid
from urllib.parse import unquote_plus
import boto3

# S3
s3_client = boto3.client('s3')

# DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EncryptionJobs')

DESTINATION_BUCKET = "isuranga-destination-bucket-file-encrypter"


def lambda_handler(event, context):

    for record in event['Records']:

        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])

        download_path = f'/tmp/{uuid.uuid4()}.pdf'
        upload_path = f'/tmp/converted-{uuid.uuid4()}.pdf'

        if key.lower().endswith('.pdf'):

            try:

                # Extract Job ID
                # uploads/{user_id}/{jobId}/filename.pdf
                job_id = key.split('/')[2]

                # Download original PDF
                s3_client.download_file(
                    bucket,
                    key,
                    download_path
                )

                # Encrypt PDF
                encrypt_pdf(
                    download_path,
                    upload_path
                )

                # Create encrypted filename
                encrypted_key = add_encrypted_suffix(key)

                # Upload encrypted PDF
                s3_client.upload_file(
                    upload_path,
                    DESTINATION_BUCKET,
                    encrypted_key
                )

                # Update DynamoDB
                table.update_item(
                    Key={
                        'jobId': job_id
                    },
                    UpdateExpression="""
                        SET #status = :status,
                            encryptedKey = :encryptedKey
                    """,
                    ExpressionAttributeNames={
                        '#status': 'status'
                    },
                    ExpressionAttributeValues={
                        ':status': 'COMPLETED',
                        ':encryptedKey': encrypted_key
                    }
                )

                print(
                    f"Successfully encrypted and updated job {job_id}"
                )

            except Exception as e:

                print(f"Error processing file: {str(e)}")

                try:

                    table.update_item(
                        Key={
                            'jobId': job_id
                        },
                        UpdateExpression="""
                            SET #status = :status
                        """,
                        ExpressionAttributeNames={
                            '#status': 'status'
                        },
                        ExpressionAttributeValues={
                            ':status': 'FAILED'
                        }
                    )

                except Exception as db_error:

                    print(
                        f"DynamoDB update failed: {str(db_error)}"
                    )


def encrypt_pdf(
    file_path,
    encrypted_file_path
):

    reader = PdfReader(file_path)

    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt("my-secret-password")

    with open(
        encrypted_file_path,
        "wb"
    ) as file:

        writer.write(file)


def add_encrypted_suffix(original_key):

    filename, extension = original_key.rsplit('.', 1)

    return (
        f"{filename}_encrypted.{extension}"
    )