import os
import boto3 as boto

__all__ = ["DBTable"]

REGION = os.getenv("AWS_REGION")

dynamodb = boto.resource("dynamodb", region_name=REGION)


class DBTable:
def __init__(self, table_name, partition_key, sort_key=None):
        """
        Initializes the DBTable class.

        Parameters:
        table_name (str): The name of the table.
        partition_key (str): The partition key for the table.
        sort_key (str, optional): The sort key for the table. Defaults to None.
        """
        self.table = dynamodb.Table(table_name)
        self.partition_key = partition_key
        self.sort_key = sort_key

def put(self, item):
        """
        Inserts an item into the table. The item is a dictionary where the keys are the attribute names and the values are the attribute values.

        Parameters:
        item (dict): The item to insert.
        """
        self.table.put_item(Item=item)


def update(self, key_value, sort_key_value, attrs):
        """
        Updates an item in the table.

        Parameters:
        key_value (str): The value of the partition key for the item.
        sort_key_value (str): The value of the sort key for the item.
        attrs (dict): A dictionary where the keys are the attribute names and the values are the new attribute values.
        """
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
        """
        Retrieves an item from the table.

        Parameters:
        key_value (str): The value of the partition key for the item.
        sort_key_value (str): The value of the sort key for the item.

        Returns:
        dict: The retrieved item.
        """
        r = self.table.get_item(
            Key={self.partition_key: key_value, self.sort_key: sort_key_value}
        )
        return r.get("Item")

def delete(self, key_value, sort_key_value):
        """
        Deletes an item from the table.

        Parameters:
        key_value (str): The value of the partition key for the item.
        sort_key_value (str): The value of the sort key for the item.
        """
        self.table.delete_item(
            Key={self.partition_key: key_value, self.sort_key: sort_key_value}
        )

def batch_write(self, items):
        """
        Inserts multiple items into the table.

        Parameters:
        items (list): A list of items to insert. Each item is a dictionary where the keys are the attribute names and the values are the attribute values.
        """
        with self.table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

def batch_get(self, key_value, sort_key_values):
        """
        Retrieves multiple items from the table.

        Parameters:
        key_value (str): The value of the partition key for the items.
        sort_key_values (list): A list of the values of the sort key for the items.

        Returns:
        list: The retrieved items.
        """
        results = []
        for sort_key_value in sort_key_values:
            results.append(self.get_sort(key_value, sort_key_value))

        return results
