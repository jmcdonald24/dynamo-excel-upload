import boto3
import openpyxl
from io import BytesIO

def test_message():
    return "Hello from the test message function"

def read_excel_from_s3(s3_client, bucket_name, s3_file_key):

    excel_data = s3_client.get_object(Bucket=bucket_name, Key=s3_file_key)['Body'].read()
    workbook = openpyxl.load_workbook(BytesIO(excel_data), data_only=True)
    sheet = workbook.active

    return sheet

def delete_all_rows(table_name):

    TABLE = table_name
    ID = 'id'

    table = boto3.resource('dynamodb').Table(TABLE)

    scan = None

    with table.batch_writer() as batch:
        count = 0
        while scan is None or 'LastEvaluatedKey' in scan:
            if scan is not None and 'LastEvaluatedKey' in scan:
                scan = table.scan(
                    ProjectionExpression=ID,
                    ExclusiveStartKey=scan['LastEvaluatedKey'],
                )
            else:
                scan = table.scan(ProjectionExpression=ID)

            for item in scan['Items']:
                if count % 5000 == 0:
                    print(count)
                batch.delete_item(Key={ID: item[ID]})
                count = count + 1