import json
import os
from typing import Union
import boto3


get_bucket_name_from_arn = lambda arn: arn[13:] if arn is not None else None
BUCKET_NAME = get_bucket_name_from_arn(os.getenv("RESULTS_BUCKET_NAME", None))

def write_result_to_s3(result: dict, key: str) -> None:
    s3 = boto3.client('s3')
    object_key = key

    response = s3.put_object(
        Body=json.dumps(result),
        Bucket=BUCKET_NAME,
        Key=object_key
    )
    return response


