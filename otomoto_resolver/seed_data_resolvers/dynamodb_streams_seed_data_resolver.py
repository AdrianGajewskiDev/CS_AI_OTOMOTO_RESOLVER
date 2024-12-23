import json
from cs_ai_common.logging.internal_logger import InternalLogger
from cs_ai_common.seed_data.seed_data_resolver import SeedDataResolver

class DynamoDBStreamsSeedDataResolver(SeedDataResolver):
    def __init__(self, event: dict):
        self.event = event

    def get_seed_data(self) -> dict:
        InternalLogger.LogDebug("Getting seed data from DynamoDB Streams event. {}".format(json.dumps(self.event)))        
        record = self.event["Records"][0]
        event_type = record["eventName"]

        if event_type != "INSERT":
            InternalLogger.LogDebug("Event type is not INSERT. Skipping event processing.")
            return {}
        
        data = record["dynamodb"]["NewImage"]
        seed_data = json.loads(data["seed_data"]["S"])
        return {
            "seed_data": {
                "Type": seed_data["Type"],
                "Make": seed_data["Make"],
                "Model": seed_data["Model"],
                "ProductionYear": seed_data["ProductionYear"],
                "FuelType": seed_data["FuelType"],
                "Mileage": seed_data["Mileage"],
                "Capacity": seed_data["Capacity"],
                "Transmission": seed_data["Transmision"],
                "HorsePower": seed_data["HorsePower"],
                "Generation": seed_data["Generation"] if "Generation" in seed_data else None,
            },
            "task_id": data["task_id"]["S"],
            "created_date": data["created_date"]["S"]
        }
