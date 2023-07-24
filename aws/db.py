import os
import boto3 as boto

__all__ = ["DBTable"]

REGION = os.getenv("AWS_REGION")

dynamodb = boto.resource("dynamodb", region_name=REGION)


class DBTable:
    def __init__(self, table_name, partition_key, sort_key=None):
        self.table = dynamodb.Table(table_name)
        self.partition_key = partition_key
        self.sort_key = sort_key

    def put(self, item):
        self.table.put_item(Item=item)


    def update(self, key_value, sort_key_value, attrs):
        update_expression = "SET "
        expression_attribute_values = {}
        for key, value in attrs.items():
            update_expression += f"{key} = :{key}, "
            expression_attribute_values[f":{key}"] = value

        update_expression = update_expression[:-2]

        self.table.update_item(
            Key={self.partition_key: key_value, self.sort_key: sort_key_value},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
        )

    def get(self, key_value, sort_key_value):
        r = self.table.get_item(
            Key={self.partition_key: key_value, self.sort_key: sort_key_value}
        )
        return r.get("Item")

    def delete(self, key_value, sort_key_value):
        self.table.delete_item(
            Key={self.partition_key: key_value, self.sort_key: sort_key_value}
        )

    def batch_write(self, items):
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

    def batch_get(self, key_value, sort_key_values):
        results = []
        for sort_key_value in sort_key_values:
            results.append(self.get_sort(key_value, sort_key_value))

        return results
