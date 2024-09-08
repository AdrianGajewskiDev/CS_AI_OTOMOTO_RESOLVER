import json
import uuid
from otomoto_resolver.scraper.start_up_scraper import startup_scraper
from otomoto_resolver.seed_data_resolvers.local_seed_data_resolver import LocalSeedDataResolver
from otomoto_resolver.services.S3WriterService import S3WriterService


def handler(event: dict, context):
    seed_data_provider = LocalSeedDataResolver()
    result_writer_service = S3WriterService()
    return startup_scraper(seed_data_provider, result_writer_service)