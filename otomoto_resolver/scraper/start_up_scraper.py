
from itertools import chain
import json
import os

from otomoto_resolver.factories.otomot_resolver_factory import create_otomoto_resolver
from otomoto_resolver.logging.logger import InternalLogger
from otomoto_resolver.scraper.execute_scraper import execute_scraper
from otomoto_resolver.seed_data_resolvers.seed_data_resolver import SeedDataResolver
from otomoto_resolver.services.ResultWriterService import ResultWriterService

def startup_scraper(seed_data_resolver: SeedDataResolver, result_writer_service: ResultWriterService) -> None:
    seed_data = seed_data_resolver.get_seed_data()

    if not seed_data:
        InternalLogger.LogDebug("No seed data found. Exiting.")
        return

    InternalLogger.LogDebug(f"Starting scraper with seed data: {seed_data}")

    resolver = create_otomoto_resolver()
    InternalLogger.LogDebug(f"Resolver created: {resolver.__dict__}")

    scraped_data = execute_scraper(resolver, transform_seed_data(seed_data))

    InternalLogger.LogDebug(f"Scraped data: {len(scraped_data)}")

    s3_content = build_s3_content_from_scraped_data(seed_data["task_id"], scraped_data)

    InternalLogger.LogDebug(f"Writing result to S3")
    result_writer_service.write_result(s3_content, key="{}/{}/{}.json".format(seed_data["task_id"], "otomoto", "result"))

def build_s3_content_from_scraped_data(task_id: str, scraped_data: list) -> dict:
    return {
        "task_id": task_id,
        "content": [json.dumps(page) for page in scraped_data if page]
    }

def transform_seed_data(seed_data: dict) -> dict:
    return {
        "Type": seed_data["seed_data"]["Type"],
        "Make": seed_data["seed_data"]["Make"],
        "Model": seed_data["seed_data"]["Model"],
        "ProductionYearFrom": int(seed_data["seed_data"]["ProductionYear"]) - 2,
        "ProductionYearTo": int(seed_data["seed_data"]["ProductionYear"]) + 2,
        "FuelType": seed_data["seed_data"]["FuelType"],
        "MileageFrom": 20000,
        "MileageTo": 500000,
        "Generation": seed_data["seed_data"]["Generation"] if "Generation" in seed_data["seed_data"] else None
    }

