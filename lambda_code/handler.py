from utils import util
import openpyxl
import boto3
from io import BytesIO

def lambda_handler(event, context):
    print(util.test_message())
    
    print(f"Event: {event}")
    get_excel_file_from_s3("dynamorawdatabucket", "Book1.xlsx")

def get_excel_file_from_s3(bucket_name, file_name):
    s3 = boto3.client('s3')
    
    try:

        excel_data = s3.get_object(Bucket=bucket_name, Key=file_name)['Body'].read()
        
        workbook = openpyxl.load_workbook(BytesIO(excel_data), data_only=True)
        sheet = workbook.active
        
        for row in sheet.iter_rows(values_only=True):
            print(row)
            
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    lambda_handler({}, None)

    get_excel_file_from_s3("dynamorawdatabucket", "Book1.xlsx")
