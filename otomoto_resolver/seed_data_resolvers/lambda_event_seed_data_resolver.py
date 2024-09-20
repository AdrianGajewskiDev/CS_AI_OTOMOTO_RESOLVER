import json
from otomoto_resolver.logging.logger import InternalLogger
from otomoto_resolver.seed_data_resolvers.seed_data_resolver import SeedDataResolver


class LambdaEventSeedDataResolver(SeedDataResolver):
    def __init__(self, event: dict):
        self.event = event

    def get_seed_data(self) -> dict:
        InternalLogger.LogDebug("Getting seed data from lambda event. {}".format(json.dumps(self.event)))        
        seed_data = self.event["seed_data"]
        task_id = self.event["task_id"]
        created_date = self.event["created_date"]

        return {
            "seed_data": {
                "Type": "osobowe",
                "Make": seed_data["Make"],
                "Model": seed_data["Model"],
                "ProductionYear": seed_data["ProductionYear"],
                "FuelType": seed_data["FuelType"],
                "Mileage": seed_data["Mileage"],
                "EngineCapacity": seed_data["EngineCapacity"],
                "Transmission": seed_data["Transmission"],
                "EnginePower": seed_data["EnginePower"],
                "Generation": seed_data["Generation"] if "Generation" in seed_data and seed_data else None,
            },
            "task_id": task_id,
            "created_date": created_date
        }
