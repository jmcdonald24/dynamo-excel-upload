provider "aws" {
    region = "us-east-1"  # Replace with your desired region
}

resource "aws_dynamodb_table" "example_table" {
    name           = "example_table"
    billing_mode   = "PAY_PER_REQUEST"
    hash_key       = "id"
    attribute {
        name = "id"
        type = "S"
    }
}

resource "aws_s3_bucket" "dynamo_raw_data_bucket" {
    bucket = "dynamorawdatabucket"
}

resource "aws_s3_object" "object" {
    bucket = aws_s3_bucket.dynamo_raw_data_bucket.bucket
    key = "Book1.xlsx"
    source = "../python/Book1.xlsx"
}

resource "aws_lambda_function" "example_lambda" {
    function_name = "test-lambda"
    handler = "handler.lambda_handler"
    runtime = "python3.12"
    role = aws_iam_role.example_role.arn
    filename = "../test-lambda.zip"
    timeout = 60
    memory_size = 256
}

resource "aws_iam_role" "example_role" {
    name = "example_role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17",
        Statement = [
            {
                Effect = "Allow",
                Principal = {
                    Service = "lambda.amazonaws.com"
                },
                Action = "sts:AssumeRole"
            }
        ]
    })
}




# See also the following AWS managed policy: AWSLambdaBasicExecutionRole
data "aws_iam_policy_document" "lambda_logging" {
  statement {
    effect = "Allow"

    actions = [
        "s3:GetObject",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "dynamodb:Scan",
        "dynamodb:DeleteItem",
        "dynamodb:PutItem",
        "dynamodb:BatchWriteItem"
    ]

    resources = [
        "${aws_s3_bucket.dynamo_raw_data_bucket.arn}/*",
        "arn:aws:logs:*:*:*",
        "${aws_dynamodb_table.example_table.arn}"
        ]
  }
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_logging.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.example_role.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}