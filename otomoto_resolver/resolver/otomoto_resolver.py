from collections import defaultdict
import re
from typing import Any, List

from bs4 import BeautifulSoup

from otomoto_resolver.logging.logger import InternalLogger
from otomoto_resolver.models.fuel_types import map_fuel_type
from otomoto_resolver.models.resolver_rules import FieldTypes, NamedFields, ResolverRule, ResolverStrategy, TypedResolverRule
from otomoto_resolver.models.transmissions import map_transmission
from otomoto_resolver.response_models.resolver_response import ResolverResponse

class Resolver():
    def __init__(self, base_url: str, desired_tag: str, desired_attributes: dict, info_selectors: dict, strategy: ResolverStrategy, rs_rules: List[TypedResolverRule]):
        self._resolver_rules = rs_rules
        self._base_url = base_url
        self._desired_attributes = desired_attributes
        self._desired_tag = desired_tag
        self._info_selectors = info_selectors
        self._strategy = strategy

    _resolver_rules: List[TypedResolverRule]
    _base_url: str
    _desired_tag: str
    _desired_attributes: dict
    _info_selectors: dict
    _strategy: ResolverStrategy
    _resolved_url: str
    pattern = "{}{}"

    def get_strategy(self) -> ResolverStrategy:
        return self._strategy

    def get_resolved_url(self) -> str:
        return self._resolved_url

    def resolve_url(self, seed_data: defaultdict) -> str:
        search_part = ""
        sorted_rules = sorted(self._resolver_rules, key=lambda x:x.Rule.Type, reverse=True)

        _prev_rule: TypedResolverRule = sorted_rules[0]
        for rule in sorted_rules:
            if rule.Field == NamedFields.Base:
                self._fill_base_fields(rule, seed_data)
                search_part += rule.Rule.Value
                continue
            
            if not rule.Rule.Static:
                _ptrn = seed_data[rule.Field]

            if not _ptrn and not rule.Rule.Static:
                InternalLogger.LogInfo(f"Could not find value for field: {rule.Field}")
                continue
            
            if not rule.Rule.Static:  
                rule_new_value = self._replace_value(rule.Rule.Value, f"<{rule.Field}>", _ptrn)
                rule.Rule.Value = rule_new_value
            
            first_query_in_url = rule.Rule.Type == FieldTypes.QueryString and _prev_rule.Rule.Type == FieldTypes.UrlPart 
            if first_query_in_url:
                search_part += "?"

            if not first_query_in_url and not search_part.endswith("/") and _prev_rule.Rule.Type != FieldTypes.QueryString:
                search_part += "/"
            elif not first_query_in_url:
                search_part += "&"

            search_part += rule.Rule.Value                
            _prev_rule = rule

        self._resolved_url = self.pattern.format(self._base_url, search_part)
    
    def _replace_value(self, placeholder: str, old_value: str, new_value: str) -> str:
        return placeholder.replace(old_value, str(new_value))
    
    def _fill_base_fields(self, rule: TypedResolverRule, seed_data: defaultdict) -> None:
        regex = re.compile("<([^\/]+)>")
        to_fill_data = regex.findall(rule.Rule.Value)
        if not to_fill_data:
            raise Exception("Could not extract base fields")
        
        for data in to_fill_data:
            new_value = seed_data[data]
            rule.Rule.Value = self._replace_value(rule.Rule.Value, f"<{data}>", new_value)

    def extract_desired_content(self, html_content: str, tag: str, attributes: dict) -> str:
        soup = BeautifulSoup(str(html_content), "html.parser")
        return soup.findAll(tag, attributes)

    def get_by_selector(self, html_content: str, selector: str) -> str:
        soup = BeautifulSoup(str(html_content), "html.parser")
        return soup.select_one(selector)

    def scrap_data_from_html(self, html_content: str):
        pass

    def execute_strategy(self, seed_data: dict):
        pass

class OtomotoResolver(Resolver):
    def scrap_data_from_html(self, html_content: str) -> List[dict]:
        desired_content = self.extract_desired_content(html_content, self._desired_tag, self._desired_attributes)
        result: List[dict] = []
        for count, cnt in enumerate(desired_content):
            price = self.get_by_selector(cnt, self._info_selectors["Price"])
            price_currency = self.get_by_selector(cnt, self._info_selectors["PriceCurrency"])
            mileage = self.get_by_selector(cnt, self._info_selectors["Mileage"])
            production_year = self.get_by_selector(cnt, self._info_selectors["ProductionYear"])
            fuel_type = self.get_by_selector(cnt, self._info_selectors["FuelType"])
            details = self.get_by_selector(cnt, self._info_selectors["Details"])
            transmision = self.get_by_selector(cnt, self._info_selectors["Transmision"])
            isalnum = ''.join(e for e in details.text if e.isalnum())
            horse_power = self.get_from_regex(r'\d{3}KM', isalnum)
            capacity = self.get_from_regex(r"\d+cm3", isalnum)


            if all([price, price_currency, mileage, production_year, fuel_type, details, transmision, horse_power, capacity]):
                result.append(ResolverResponse(
                    Price=price.text if price else "",
                    PriceCurrency=price_currency.text if price_currency else "",
                    Mileage=mileage.text if mileage else "",
                    ProductionYear=production_year.text if production_year else "",
                    FuelType=map_fuel_type(fuel_type.text) if fuel_type else "",
                    Transmision=map_transmission(transmision.text) if transmision else "",
                    HorsePower=horse_power if horse_power else "",
                    Capacity=capacity if capacity else ""
                ).json())

        return result


    def execute_strategy(self, seed_data: dict):
        self.append_page_index_to_url(int(seed_data["page_index"]))
    
    def append_page_index_to_url(self, index: int) -> None:
        prev_index = index - 1
        if self._resolved_url.endswith(f"page={prev_index}"):
            self._resolved_url = self._resolved_url.replace(f"page={prev_index}", f"page={index}")
            return
        else:
            self._resolved_url += f"&page={index}"

    def get_from_regex(self, regex, input) -> str:
        match = re.search(regex, input)
        if match:
            extracted_value = match.group()
            extracted_value = extracted_value.replace("cm3", "").replace("KM", "")
            return extracted_value
        else:
            return ""