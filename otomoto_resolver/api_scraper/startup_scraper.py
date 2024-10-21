import json
from typing import Any, List
from otomoto_resolver.api_scraper.execute_scraper import execute_api_scraper
from otomoto_resolver.factories.otomot_resolver_factory import create_otomoto_api_resolver
from cs_ai_common.logging.internal_logger import InternalLogger
from cs_ai_common.seed_data.seed_data_resolver import SeedDataResolver
from cs_ai_common.typings.car_utils import Transmisions, FuelTypes
from cs_ai_common.services.result_writer_service import ResultWriterService
from cs_ai_common.resolver_cache.try_get_cache import try_get_cache
from cs_ai_common.dynamodb.resolver_task_table import insert_resolver_result_task
from cs_ai_common.models.resolvers import ResolverResponse

def startup_api_scraper(seed_data_resolver: SeedDataResolver, result_writer_service: ResultWriterService) -> None:
    seed_data = seed_data_resolver.get_seed_data()
    if not seed_data:
            InternalLogger.LogDebug("No seed data found. Exiting.")
            return

    InternalLogger.LogDebug(f"Starting scraper with seed data: {seed_data}")
    InternalLogger.LogDebug("Trying to get cache")
    cache_key, cache_result = try_get_cache(seed_data["seed_data"], "otomoto")
    InternalLogger.LogDebug(f"Cache key: {cache_key}")
    if cache_result:
        InternalLogger.LogDebug("Cache found. Returning cached result.")
        ads_found = len(cache_result["content"])
        InternalLogger.LogDebug(f"Writing statistics to Dynamodb: {ads_found}")
        insert_resolver_result_task(seed_data["task_id"], "otomoto", ads_found=str(ads_found))
        InternalLogger.LogDebug("Statistics written to Dynamodb")
        result_writer_service.write_result(cache_result, key="{}/{}/{}.json".format(seed_data["task_id"], "otomoto", "result"))
        return 0

    resolver  = create_otomoto_api_resolver()
    scraped_data = list(execute_api_scraper(resolver, seed_data["seed_data"]))

    InternalLogger.LogDebug(f"Writing result to S3")
    
    add_data = extract_add_data(scraped_data, seed_data["seed_data"])
    
    s3_content = {
        "task_id": seed_data["task_id"],
        "content": [page for page in add_data if page]
    }
    InternalLogger.LogDebug("Writing statistics to Dynamodb")
    insert_resolver_result_task(seed_data["task_id"], "otomoto", ads_found=str(len(add_data)))
    InternalLogger.LogDebug("Statistics written to Dynamodb")

    InternalLogger.LogDebug("Writing result to S3")
    result_writer_service.write_result(s3_content, key="{}/{}/{}.json".format(seed_data["task_id"], "otomoto", "result"))
    InternalLogger.LogDebug("Result written to S3")

    InternalLogger.LogDebug("Writing cache to S3")
    result_writer_service.write_cache(s3_content, cache_key, "otomoto")
    InternalLogger.LogDebug("Cache written to S3")
    
    InternalLogger.LogDebug("Exiting.")
    return 0

def extract_add_data(scraped_data: List[dict], seed_data: dict) -> list:
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
                InternalLogger.LogDebug(f"Extracting data from node: {node}")
                ad_link = node.get("url")

                if any(ad_link in json.loads(ad)["AdvertisementLink"] for ad in add_data):
                    InternalLogger.LogDebug("Ad already in list. Skipping.")
                    continue

                add_data.append(ResolverResponse(
                    Price=node["price"]["amount"]["value"],
                    PriceCurrency=node["price"]["amount"]["currencyCode"],
                    Mileage=get_from_params(node["parameters"], "mileage"),
                    ProductionYear=get_from_params(node["parameters"], "year"),
                    FuelType=FuelTypes.to_common(get_from_params(node["parameters"], "fuel_type", FuelTypes.PETROL)),
                    Transmision=Transmisions.to_common(get_from_params(node["parameters"], "gearbox", Transmisions.MANUAL)),
                    HorsePower=get_from_params(node["parameters"], "engine_power"),
                    Capacity=get_from_params(node["parameters"], "engine_capacity"),
                    AdvertisementLink=node["url"],
                    Thumbnails=[node.get("thumbnail", {}).get("x1", ""), node.get("thumbnail", {}).get("x2", "")] if isinstance(node.get("thumbnail"), dict) else [],
                    Make=seed_data["Make"],
                    Model=seed_data["Model"],
                    SourceId="OTOMOTO",
                    LocationCountry="PL",
                    LocationCity=_get_city_details(node)
                ).json())

    return add_data

def get_from_params(parameters: dict, key: str, default: Any | str = "") -> str:
    for param in parameters:
        if param["key"] == key:
            return param["value"]

    return default

def _get_city_details(data: dict) -> str:
    location = data.get("location", {})
    if not location:
        return ""
    city = location.get("city", "")
    if not city or not isinstance(city, dict):
        return ""
    return json.dumps(city)