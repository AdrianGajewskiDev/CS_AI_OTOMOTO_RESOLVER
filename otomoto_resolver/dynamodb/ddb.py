from otomoto_resolver.logging.logger import InternalLogger
import boto3
from botocore.exceptions import ClientError


def update_task_status_failed(task_id: str, table_name: str) -> None:
    dynamodb = boto3.client('dynamodb')
    
    try:
        dynamodb.update_item(
            TableName=table_name,
            Key={
                'task_id': {
                    'S': task_id
                }
            },
            UpdateExpression="set #status = :status",
            ExpressionAttributeNames={
                "#status": "status"
            },
            ExpressionAttributeValues={
                ":status": {
                    'S': "FAILED"
                }
            }
        )
        InternalLogger.LogDebug("UpdateItem succeeded")
    except ClientError as e:
        InternalLogger.LogError(f"Unable to update item: {e.response['Error']['Message']}")
        raise e