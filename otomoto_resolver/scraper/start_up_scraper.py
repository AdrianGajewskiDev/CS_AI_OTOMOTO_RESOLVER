
import os

from otomoto_resolver.factories.otomot_resolver_factory import create_otomoto_resolver
from otomoto_resolver.logging.logger import InternalLogger
from otomoto_resolver.scraper.execute_scraper import execute_scraper
from otomoto_resolver.seed_data_resolvers.seed_data_resolver import SeedDataResolver

def startup_scraper(event: dict, seed_data_resolver: SeedDataResolver) -> None:
    seed_data = seed_data_resolver.get_seed_data()
    InternalLogger.LogInfo(f"Starting scraper with seed data: {seed_data}")

    resolver = create_otomoto_resolver()
    InternalLogger.LogInfo(f"Resolver created: {resolver.__dict__}")

    return execute_scraper(event["task_id"], resolver, transform_seed_data(seed_data))

def transform_seed_data(seed_data: dict) -> dict:
    return {
        "Type": seed_data["Type"],
        "Make": seed_data["Make"],
        "Model": seed_data["Model"],
        "ProductionYearFrom": int(seed_data["ProductionYear"]) - 2,
        "ProductionYearTo": int(seed_data["ProductionYear"]) + 2,
        "FuelType": seed_data["FuelType"],
        "MileageFrom": 20000,
        "MileageTo": 500000,
        "Generation": seed_data["Generation"] if "Generation" in seed_data else None
    }

