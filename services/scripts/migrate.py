from datetime import datetime

import boto3
from boto3.dynamodb.conditions import Key
import timestamp_random as tr

client = boto3.resource("dynamodb")


def get_docs(table, data_type, timestamp_from, timestamp_to):
    lower_value = tr.get_range_timestamp_random(timestamp_from)[0]
    upper_value = tr.get_range_timestamp_random(timestamp_to)[1]

    key_expression = Key('type').eq(data_type) & Key('timestamp_random').between(lower_value,
                                                                                 upper_value)

    response = table.query(KeyConditionExpression=key_expression)
    items = response['Items']

    while response.get('LastEvaluatedKey'):
        response = table.query(KeyConditionExpression=key_expression,
                               ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])

    return items


def migrate(document_type, source_table_name, target_table_name,
            regenerate_timestamp_random=False):
    source_table = client.Table(source_table_name)
    target_table = client.Table(target_table_name)

    ts_now = int(datetime.now().timestamp())
    docs = get_docs(source_table, document_type, 0, ts_now)

    items = len(docs)
    print(
        f"You are about to copy {items} documents with type = {document_type} from DynamoDB table "
        f"{source_table_name} to {target_table_name}"
    )
    if regenerate_timestamp_random:
        print("This process will regenerate the timestamp_random field of the documents")
    cont = input("Continue? [y/N] ")
    if cont.lower() != "y":
        return

    i = 0
    for doc in docs:
        timestamp = int(doc["timestamp"])
        fixed_doc = doc
        fixed_doc["timestamp_random"] = tr.get_timestamp_random(timestamp=timestamp)
        target_table.put_item(Item=fixed_doc)
        i += 1
        print(f"{i} / {items}")


def delete_documents(table_name, document_type, timestamp_from, timestamp_to):
    table = client.Table(table_name)
    docs = get_docs(table, document_type, timestamp_from, timestamp_to)
    items = len(docs)
    print(f"You are about to delete {items} documents with type = {document_type} from DynamoDB "
          f"table {table_name}")
    cont = input("Continue? [y/N] ")
    if cont.lower() != "y":
        return
    i = 0
    for doc in docs:
        timestamp_random = doc["timestamp_random"]
        table.delete_item(Key={
            "type": document_type,
            "timestamp_random": timestamp_random
        })
        i += 1
        print(f"{i} / {items}")


if __name__ == '__main__':
    # migrate("EventType", "Dataplattform-dev", "Dataplattform-test")
    # migrate("EventType", "Dataplattform-dev", "Dataplattform-test",
    #         regenerate_timestamp_random=True)
    # delete_documents("Dataplattform-test", "YeetType", 0, 100000000000)
    pass
