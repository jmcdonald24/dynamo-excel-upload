from utils import util
import openpyxl
import boto3
from io import BytesIO

s3_client = boto3.client('s3')
ddb_client = boto3.client('dynamodb')

bucket_name = 'dynamorawdatabucket'

def lambda_handler(event, context):
    
    print("Deleting all rows from the table")
    util.delete_all_rows("example_table")
    
    print(f"Event: {event}")

    sheet = util.read_excel_from_s3(s3_client, "bucket_name", "Book1.xlsx")


if __name__ == "__main__":
    lambda_handler({}, None)


