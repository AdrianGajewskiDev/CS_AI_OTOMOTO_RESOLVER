import json
import uuid
from otomoto_resolver.scraper import start_up_scraper
from otomoto_resolver.seed_data_resolvers.local_seed_data_resolver import LocalSeedDataResolver

seed_data_provider = LocalSeedDataResolver()
def handler(event: dict, context):
    event.setdefault("task_id", str(uuid.uuid4()))
    return start_up_scraper.startup_scraper(event, seed_data_provider)