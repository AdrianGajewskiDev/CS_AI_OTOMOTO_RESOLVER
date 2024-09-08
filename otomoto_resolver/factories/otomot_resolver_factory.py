from collections import defaultdict
import json
import os
from typing import List

from otomoto_resolver.models.resolver_rules import ResolverRule, ResolverStrategy, TypedResolverRule
from otomoto_resolver.resolver.otomoto_resolver import OtomotoResolver

definition_file_path = os.environ["LAMBDA_TASK_ROOT"] + "/otomoto_resolver/definition/ResolverDefinition.json"

def create_otomoto_resolver() -> OtomotoResolver:
    with open(definition_file_path, "r") as file:
        definition = json.load(file)

    if not definition:
        raise Exception("Resolver definition is empty")
    
    return OtomotoResolver(
        base_url=definition["SearchUrl"],
        rs_rules=_get_rules(definition["SearchRules"]),
        desired_tag=definition["DesiredTag"],
        desired_attributes=_get_desired_attributes(definition["DesiredAttributes"]),
        strategy=_get_strategy(definition["Strategy"]),
        info_selectors=definition["AdInfoSelectors"]
    )

def _get_rules(rules: dict):
    for key in rules.keys():
        _details = rules[key]
        yield TypedResolverRule(
            Field=key,
            Rule=ResolverRule(**_details)
        )

def _get_desired_attributes(attributes: dict) -> dict:
    _new_dict: defaultdict = defaultdict(str)

    for key in attributes.keys():
        _new_dict.setdefault(key, attributes[key])

    return _new_dict

def _get_strategy(strategy: dict) -> ResolverStrategy:
    iterations = int(strategy["Iterations"])
    rules = strategy["Rules"]
    _rules: List[ResolverRule] = []
    for rule in rules:
        _rules.append(ResolverRule(
            Type=rule["Type"],
            Value=rule["Value"],
            Static=rule["Static"] if "Static" in rule else False
        ))
    
    return ResolverStrategy(
        Iterations=iterations,
        Rules=_rules
    )