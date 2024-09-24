import json
from typing import List
from otomoto_resolver.api_scraper.execute_scraper import execute_api_scraper
from otomoto_resolver.factories.otomot_resolver_factory import create_otomoto_api_resolver
from otomoto_resolver.logging.logger import InternalLogger
from otomoto_resolver.response_models.resolver_response import ResolverResponse
from otomoto_resolver.seed_data_resolvers.seed_data_resolver import SeedDataResolver
from otomoto_resolver.services.ResultWriterService import ResultWriterService


def startup_api_scraper(seed_data_resolver: SeedDataResolver, result_writer_service: ResultWriterService) -> None:
    seed_data = seed_data_resolver.get_seed_data()
    if not seed_data:
            InternalLogger.LogDebug("No seed data found. Exiting.")
            return

    InternalLogger.LogDebug(f"Starting scraper with seed data: {seed_data}")

    resolver  = create_otomoto_api_resolver()
    scraped_data = list(execute_api_scraper(resolver, seed_data["seed_data"]))

    InternalLogger.LogDebug(f"Writing result to S3")
    
    add_data = extract_add_data(scraped_data)
    
    s3_content = {
        "task_id": seed_data["task_id"],
        "content": [page for page in add_data if page]
    }
    result_writer_service.write_result(s3_content, key="{}/{}/{}.json".format(seed_data["task_id"], "otomoto", "result"))
    InternalLogger.LogDebug("Result written to S3")

    return 0

def extract_add_data(scraped_data: List[dict]) -> list:
    add_data = []
    for page in scraped_data:

        edges = page.get("data", {}).get("advertSearch", {}).get("edges")

        if not edges:
            InternalLogger.LogDebug("No edges found in page. Skipping.")
            continue

        for edge in edges:
                if edge.get("__typename") != "AdvertEdge":
                    InternalLogger.LogDebug("Node is not of type AdvertEdge. Skipping.")
                    continue

                node = edge.get("node")
                if not node:
                        InternalLogger.LogDebug("No node found in edge. Skipping.")
                        continue
                        
                add_data.append(ResolverResponse(
                    Price=node["price"]["amount"]["value"],
                    PriceCurrency=node["price"]["amount"]["currencyCode"],
                    Mileage=node["price"]["amount"]["currencyCode"],
                    ProductionYear=get_from_params(node["parameters"], "mileage"),
                    FuelType=get_from_params(node["parameters"], "fuel_type"),
                    Transmision=get_from_params(node["parameters"], "gearbox"),
                    HorsePower=get_from_params(node["parameters"], "engine_power"),
                    Capacity=get_from_params(node["parameters"], "engine_capacity")
                ).json())



    return add_data

def get_from_params(parameters: dict, key: str) -> str:
    for param in parameters:
        if param["key"] == key:
            return param["value"]
    return ""