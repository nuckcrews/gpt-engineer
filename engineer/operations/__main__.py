from dotenv import load_dotenv

load_dotenv()

import os
import json
from gptop import OperationUtils

namespace = "engineer"

def main():
    OperationUtils.remove_namespace(namespace=namespace)
    print("Cleared namespace:", namespace)

    for subdir, dirs, files in os.walk("./engineer/operations/manifests"):
        for file in files:
            file_path = subdir + os.sep + file

            if file_path.endswith(".json"):
                print("Uploading operation at", file_path)
                file = open(file_path, "r")
                obj = file.read()
                obj = json.loads(obj)
                file.close()

                id = obj.get("id")
                type = obj.get("type")
                name = obj.get("name")
                description = obj.get("description")
                metadata = json.dumps(
                    obj.get("metadata"), separators=(',', ': '))
                schema = json.dumps(obj.get("schema"), separators=(',', ': '))

                OperationUtils.update_operation(namespace, id, type, name,
                                                description, metadata, schema)


if __name__ == "__main__":
    main()
