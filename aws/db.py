import os
import boto3 as boto

__all__ = ["DBTable"]

REGION = os.getenv('AWS_REGION')

dynamodb = boto.resource(
    "dynamodb",
    region_name=REGION
)


class DBTable:

    def __init__(self, table_name, key, sort_key=None):
        self.table = dynamodb.Table(table_name)
        self.key = key
        self.sort_key = sort_key

    def put(self, item):
        self.table.put_item(Item=item)

    def update(self, key, sort_key, attr, newValue):
        self.table.update_item(
            Key={self.key: key, self.sort_key: sort_key},
            UpdateExpression='SET ' + attr + ' = :val1',
            ExpressionAttributeValues={':val1': newValue}
        )


    def get(self, key, sort_key):
        r = self.table.get_item(Key={self.key: key, self.sort_key: sort_key})
        return r.get('Item')

    def delete(self, key, sort_key):
        self.table.delete_item(Key={self.key: key, self.sort_key: sort_key})

    def batch_write(self, items):
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    def batch_get(self, key, sort_keys):
        results = []
        for sort_key in sort_keys:
            results.append(self.get_sort(self.key, key, self.sort_key, sort_key))

        return results