import json
import os
from cs_ai_common.logging.internal_logger import InternalLogger
from cs_ai_common.models.filters import Filter
definition_file_path = os.environ["LAMBDA_TASK_ROOT"] + "/otomoto_resolver/static_files"

def build_request_body(seed_data: dict, filter: Filter, page_number: int = 1) -> dict:
    filters = [
        {
            "name": "filter_enum_make",
            "value": seed_data.get("Make")
        },
        {
            "name": "filter_enum_model",
            "value": get_model(seed_data.get("Make").lower().replace("-", "_"), seed_data.get("Model"))
        },
        {
            "name": "order",
            "value": "created_at:desc"
        }
    ]


    if filter.min_year:
        filters.append({"name": "filter_float_year:from", "value": str(filter.min_year)})

    if filter.max_year:
        filters.append({"name": "filter_float_year:to", "value": str(filter.max_year)})

    InternalLogger.LogDebug(f"Building request body with filters: {filters}")
    
    return {
            "operationName": "listingScreen",
            "query": "query listingScreen($after: ID, $click2BuyExperimentId: String!, $click2BuyExperimentVariant: String!, $experiments: [Experiment!], $filters: [AdvertSearchFilterInput!], $includeClick2Buy: Boolean!, $includePriceEvaluation: Boolean!, $includePromotedAds: Boolean!, $includeRatings: Boolean!, $includeFiltersCounters: Boolean!, $includeSortOptions: Boolean!, $includeSuggestedFilters: Boolean!, $itemsPerPage: Int, $page: Int, $parameters: [String!], $searchTerms: [String!], $sortBy: String, $maxAge: Int, $includeCepik: Boolean!, $includeNewPromotedAds: Boolean!, $promotedInput: AdSearchInput!) {\n  advertSearch(\n    criteria: {searchTerms: $searchTerms, filters: $filters}\n    sortBy: $sortBy\n    page: $page\n    after: $after\n    itemsPerPage: $itemsPerPage\n    maxAge: $maxAge\n    experiments: $experiments\n  ) {\n    ...advertSearchFields\n    edges {\n      node {\n        ...lazyAdvertFields\n        __typename\n      }\n      __typename\n    }\n    sortOptions @include(if: $includeSortOptions) {\n      searchKey\n      label\n      __typename\n    }\n    __typename\n  }\n  ...Click2BuyServiceSearch\n  ...promotedAds @include(if: $includeNewPromotedAds)\n  ...suggestedFilters @include(if: $includeSuggestedFilters)\n}\nfragment advertSearchFields on AdvertSearchOutput {\n  url\n  sortedBy\n  locationCriteriaChanged\n  subscriptionKey\n  totalCount\n  filtersCounters @include(if: $includeFiltersCounters) {\n    name\n    nodes {\n      name\n      value\n      __typename\n    }\n    __typename\n  }\n  appliedLocation {\n    city {\n      name\n      id\n      canonical\n      __typename\n    }\n    subregion {\n      name\n      id\n      canonical\n      __typename\n    }\n    region {\n      name\n      id\n      canonical\n      __typename\n    }\n    latitude\n    longitude\n    mapConfiguration {\n      zoom\n      __typename\n    }\n    __typename\n  }\n  appliedFilters {\n    name\n    value\n    canonical\n    __typename\n  }\n  breadcrumbs {\n    label\n    url\n    __typename\n  }\n  pageInfo {\n    pageSize\n    currentOffset\n    __typename\n  }\n  facets {\n    options {\n      label\n      url\n      count\n      __typename\n    }\n    __typename\n  }\n  alternativeLinks {\n    name\n    title\n    links {\n      title\n      url\n      counter\n      __typename\n    }\n    __typename\n  }\n  latestAdId\n  edges {\n    ...listingAdCardFields\n    __typename\n  }\n  topads @include(if: $includePromotedAds) {\n    ...listingAdCardFields\n    __typename\n  }\n  __typename\n}\nfragment listingAdCardFields on AdvertEdge {\n  vas {\n    isHighlighted\n    isPromoted\n    bumpDate\n    __typename\n  }\n  node {\n    ...advertFields\n    __typename\n  }\n  __typename\n}\nfragment advertFields on Advert {\n  id\n  title\n  createdAt\n  shortDescription\n  url\n  badges\n  category {\n    id\n    __typename\n  }\n  location {\n    city {\n      name\n      __typename\n    }\n    region {\n      name\n      __typename\n    }\n    __typename\n  }\n  thumbnail {\n    x1: url(size: {width: 320, height: 240})\n    x2: url(size: {width: 640, height: 480})\n    __typename\n  }\n  price {\n    amount {\n      units\n      nanos\n      value\n      currencyCode\n      __typename\n    }\n    badges\n    grossPrice {\n      value\n      currencyCode\n      __typename\n    }\n    netPrice {\n      value\n      currencyCode\n      __typename\n    }\n    __typename\n  }\n  parameters(keys: $parameters) {\n    key\n    displayValue\n    label\n    value\n    __typename\n  }\n  sellerLink {\n    id\n    name\n    websiteUrl\n    logo {\n      x1: url(size: {width: 140, height: 24})\n      __typename\n    }\n    __typename\n  }\n  brandProgram {\n    logo {\n      x1: url(size: {width: 95, height: 24})\n      __typename\n    }\n    searchUrl\n    name\n    __typename\n  }\n  dealer4thPackage {\n    package {\n      id\n      name\n      __typename\n    }\n    services {\n      code\n      label\n      __typename\n    }\n    photos(first: 5) {\n      nodes {\n        url(size: {width: 644, height: 461})\n        __typename\n      }\n      totalCount\n      __typename\n    }\n    __typename\n  }\n  priceEvaluation @include(if: $includePriceEvaluation) {\n    indicator\n    __typename\n  }\n  __typename\n}\nfragment lazyAdvertFields on Advert {\n  id\n  cepikVerified @include(if: $includeCepik)\n  sellerRatings(scope: PROFESSIONAL) @include(if: $includeRatings) {\n    statistics {\n      recommend {\n        value\n        suffix\n        __typename\n      }\n      avgRating {\n        value\n        __typename\n      }\n      total {\n        suffix\n        value\n        __typename\n      }\n      detailedRating {\n        label\n        value\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\nfragment Click2BuyServiceSearch on Query {\n  click2Buy @include(if: $includeClick2Buy) {\n    search(\n      criteria: {filters: $filters, searchTerms: $searchTerms}\n      experimentId: $click2BuyExperimentId\n      experimentVariant: $click2BuyExperimentVariant\n      itemsPerPage: 4\n      page: $page\n    ) {\n      __typename\n      ... on Click2BuySearchOutput {\n        edges {\n          node {\n            id\n            title\n            shortDescription\n            url\n            detailUrl\n            sellerLink {\n              id\n              name\n              websiteUrl\n              __typename\n            }\n            photos {\n              url\n              __typename\n            }\n            chips\n            checks\n            utmContentType\n            carDetails {\n              year\n              mileage\n              engineVolume\n              fuelType\n              make\n              model\n              __typename\n            }\n            price {\n              amount {\n                value\n                currencyCode\n                __typename\n              }\n              __typename\n            }\n            installmentPrice {\n              amount {\n                value\n                currencyCode\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n    }\n    __typename\n  }\n  __typename\n}\nfragment promotedAds on Query {\n  promoted: adSearch {\n    search(input: $promotedInput) {\n      ... on AdSearchOutput {\n        ads {\n          ...adFields\n          __typename\n        }\n        __typename\n      }\n      ... on AdSearchError {\n        message\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\nfragment adFields on Ad {\n  id\n  url\n  title\n  location {\n    cityName\n    regionName\n    __typename\n  }\n  description\n  badges\n  createdAt\n  updatedAt\n  photos\n  price {\n    currencyCode\n    ... on AdNetGrossPrice {\n      currencyCode\n      netMinorAmount\n      grossMinorAmount\n      isNet\n      __typename\n    }\n    __typename\n  }\n  attributes {\n    key\n    value\n    valueLabel\n    valueSuffix\n    __typename\n  }\n  valueAddedServices {\n    name\n    validity\n    appliedAt\n    __typename\n  }\n  brandProgram {\n    ... on BrandProgram {\n      logo {\n        url\n        __typename\n      }\n      name\n      url\n      id\n      __typename\n    }\n    __typename\n  }\n  seller {\n    ... on ProfessionalSeller {\n      name\n      uuid\n      dealerAdsUrl\n      logo {\n        url\n        __typename\n      }\n      serviceOptions {\n        label\n        code\n        url\n        __typename\n      }\n      benefits(codes: [DEALER_IDENTITY_ELEMENTS])\n      ratings {\n        statistics {\n          recommend {\n            value\n            __typename\n          }\n          avgRating {\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    ... on PrivateSeller {\n      name\n      uuid\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\nfragment suggestedFilters on Query {\n  suggestedFilters(criteria: {searchTerms: $searchTerms, filters: $filters}) {\n    key\n    name\n    values {\n      value\n      appliedFilters {\n        name\n        value\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}",
            "variables": {
                "after": None,
                "click2BuyExperimentId": "",
                "click2BuyExperimentVariant": "",
                "experiments": [
                {
                    "key": "MCTA-1463",
                    "variant": "a"
                },
                {
                    "key": "MCTA-1660",
                    "variant": "a"
                },
                {
                    "key": "MCTA-1661",
                    "variant": "a"
                }
                ],
                "filters": filters,
                "includeCepik": True,
                "includeClick2Buy": False,
                "includeFiltersCounters": False,
                "includeNewPromotedAds": False,
                "includePriceEvaluation": True,
                "includePromotedAds": False,
                "includeRatings": False,
                "includeSortOptions": False,
                "includeSuggestedFilters": False,
                "maxAge": 60,
                "page": page_number,
                "parameters": [
                    "make",
                    "offer_type",
                    "fuel_type",
                    "gearbox",
                    "country_origin",
                    "mileage",
                    "engine_capacity",
                    "engine_code",
                    "engine_power",
                    "first_registration_year",
                    "model",
                    "version",
                    "year"
                ],
                "promotedInput": {},
                "searchTerms": None,
                "sortBy": "created_at:desc"
            }
        }


def get_model(make: str, custom_model: str) -> str:
    try:
        with open(f"{definition_file_path}/{make}_models.json") as f:
            makes = json.load(f)
        
        model = [m["otomoto_key"] for m in makes if m["custom_key"] == custom_model]
        return model[0]
    except FileNotFoundError:
        raise ValueError(f"File not found for make: {make}")
    except IndexError:
        raise ValueError(f"Model not found for make: {make} and model: {custom_model}")