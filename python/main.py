import boto3
import openpyxl

session = boto3.Session(profile_name='default')
ddb_client = session.client('dynamodb')

item = {
    'id': {'N': '1'},
    'name': {'S': 'John Doe'}
}

def write_to_dynamodb(client, table_name, item: dict):
    response = ddb_client.put_item(
        TableName=table_name,
        Item=item
    )
    
    print(response)


def generate_random_ddbdata():
    import random
    import string


    id = random.randint(1, 100000)
    name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    item = {
        'id': {'N': str(id)},
        'name': {'S': name}
    }

    return item

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

def compare_header_with_fixed_values(file_path, fixed_values):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    header_row = sheet[1]
    header_values = [cell.value for cell in header_row]

    if header_values == fixed_values:
        print("Header matches fixed values")
    else:
        print("Header does not match fixed values")


def read_excel_and_write_to_dynamodb(file_path, table_name):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    header_row = sheet[1]
    header_values = [cell.value for cell in header_row]



    for row in sheet.iter_rows(min_row=2):




        item = {}
        for index, cell in enumerate(row):
            field_name = header_values[index]
            field_value = cell.value

            print(field_name, field_value)

            item[field_name] = {'S': str(field_value)}

        write_to_dynamodb(ddb_client, table_name, item)


# Example usage:
#fixed_values = ["Name", "Email", "Age"]
#compare_header_with_fixed_values("Book1.xlsx", fixed_values)


# for i in range(10):
#     write_to_dynamodb(ddb_client, 'example_table', generate_random_ddbdata())

#delete_all_rows('example_table')

read_excel_and_write_to_dynamodb("Book1.xlsx", "example_table")