import json
import os
from otomoto_resolver.logging.logger import InternalLogger
from otomoto_resolver.seed_data_resolvers.seed_data_resolver import SeedDataResolver
import re
import urllib.parse

class LambdaEventSeedDataResolver(SeedDataResolver):
    def __init__(self, event: dict):
        self.event = event

    def get_seed_data(self) -> dict:
        InternalLogger.LogDebug("Getting seed data from lambda event. {}".format(json.dumps(self.event)))        
        seed_data = self.event["seed_data"]
        task_id = self.event["task_id"]
        created_date = self.event["created_date"]
        make = transform(seed_data["Make"])
        model = transform(seed_data["Model"])
        return {
            "seed_data": {
                "Type": "osobowe",
                "Make": make,
                "Model": model,
                "ProductionYear": seed_data["ProductionYear"],
                "FuelType": seed_data["FuelType"],
                "Mileage": seed_data["Mileage"],
                "EngineCapacity": seed_data["EngineCapacity"],
                "Transmission": seed_data["Transmision"],
                "EnginePower": seed_data["EnginePower"],
                "Generation": transform_generation(make, model, seed_data["Generation"]) if "Generation" in seed_data and seed_data["Generation"] else None,
            },
            "task_id": task_id,
            "created_date": created_date
        }

def transform(make: str) -> str:
    _val = make.replace(" ", "")
    return re.sub(r'(?<!^)(?=[A-Z])', '-', _val).lower()

def transform_generation(make: str, model: str, generation: str | None) -> str:
    template_file_path = os.environ["LAMBDA_TASK_ROOT"] + "/otomoto_resolver/templates/{}.json".format(make.lower())

    with open(template_file_path) as f:
        template = json.load(f)

    InternalLogger.LogDebug("Loaded template file: {}".format(template))
    InternalLogger.LogDebug("Searching for generation: {}".format(generation))
    InternalLogger.LogDebug("Searching for model: {}".format(model))
    results = template["results"]
    check_model_only = lambda x: x["model"] == model.upper()
    check_model_and_generation = lambda x: x["model"] == model.upper() and x["generation"] == generation.upper()
    check = check_model_and_generation if generation else check_model_only

    url = [data["url"] for data in results if check(data)]
    if not url:
        raise Exception(f"Generation {generation} not found in template file")
    
    unquoted = urllib.parse.unquote(url[0])
    parsed = urllib.parse.urlparse(unquoted)
    return urllib.parse.parse_qs(parsed.query)["search[filter_enum_generation]"][0]

     