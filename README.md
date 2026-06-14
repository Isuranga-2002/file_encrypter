# Serverless PDF File Encryptor

A serverless application built on AWS that automatically encrypts PDF files uploaded to an Amazon S3 bucket. The application uses AWS Lambda to process uploaded files and stores the encrypted versions in a separate destination bucket.

## Overview

This project demonstrates event-driven serverless architecture using AWS services. When a user uploads a PDF file to the source S3 bucket, an AWS Lambda function is automatically triggered. The function encrypts the PDF with a password and uploads the encrypted file to a destination S3 bucket.

## Architecture

```text
User Uploads PDF
        │
        ▼
Source S3 Bucket
        │
        ▼
S3 Event Trigger
        │
        ▼
AWS Lambda Function
(PDF Encryption)
        │
        ▼
Destination S3 Bucket
(Encrypted PDFs)
```

## Technologies Used

* AWS Lambda
* Amazon S3
* AWS SAM (Serverless Application Model)
* AWS CloudFormation
* Python 3.12
* Boto3
* pypdf

## Features

* Automatic PDF encryption on upload
* Event-driven serverless architecture
* Secure file processing
* Scalable and cost-effective solution
* Infrastructure as Code (IaC) using AWS SAM
* No server management required

## Project Structure

```text
file_encrypter/
│
├── lambda_function.py      # Lambda function code
├── requirements.txt        # Python dependencies
├── template.yaml           # AWS SAM template
├── samconfig.toml          # SAM deployment configuration
└── README.md
```

## How It Works

1. A PDF file is uploaded to the source S3 bucket.
2. Amazon S3 generates an ObjectCreated event.
3. The event triggers the AWS Lambda function.
4. The Lambda function:

   * Downloads the uploaded PDF.
   * Encrypts the PDF using the pypdf library.
   * Creates a new file with the `_encrypted` suffix.
   * Uploads the encrypted file to the destination bucket.
5. Users can download the encrypted PDF from the destination bucket.

## Deployment

### Prerequisites

* AWS Account
* AWS CLI configured
* AWS SAM CLI installed
* Docker installed
* Python 3.12

### Build the Application

```bash
sam build --use-container
```

### Deploy the Application

```bash
sam deploy --guided
```

After the initial deployment:

```bash
sam deploy
```

## Testing

Upload a PDF file to the source bucket:

```bash
aws s3 cp sample.pdf s3://<source-bucket-name>/
```

Verify that an encrypted version of the file appears in the destination bucket.

## Example

Input:

```text
report.pdf
```

Output:

```text
report_encrypted.pdf
```

## Default Encryption Password

```text
my-secret-password
```

### Important

For demonstration purposes, the password is hardcoded in the Lambda function.

For production deployments, use:

* AWS Secrets Manager
* AWS Systems Manager Parameter Store
* Environment Variables

instead of storing sensitive values directly in code.

## AWS Resources Created

The deployment creates:

* Source S3 Bucket
* Destination S3 Bucket
* AWS Lambda Function
* IAM Execution Role
* S3 Event Notification Configuration
* CloudFormation Stack

## Cost Considerations

This project uses AWS serverless services and is eligible for AWS Free Tier usage within applicable limits. Charges may apply if usage exceeds Free Tier quotas.

## Future Improvements

* Password generation per file
* Store passwords in AWS Secrets Manager
* Email notifications using Amazon SNS
* Support for multiple file formats
* File metadata tracking using DynamoDB
* Web frontend for uploads and downloads
* User authentication with Amazon Cognito

## Learning Outcomes

This project demonstrates:

* Serverless application development
* Event-driven architecture
* AWS Lambda function deployment
* Amazon S3 event triggers
* Infrastructure as Code using AWS SAM
* CloudFormation resource management
* Python-based file processing

## Author

**Isuranga Dasun**

Built as a hands-on AWS Serverless Computing project using AWS Lambda, Amazon S3, and AWS SAM.

