from otomoto_resolver.seed_data_resolvers.seed_data_resolver import SeedDataResolver


class LocalSeedDataResolver(SeedDataResolver):
    def get_seed_data(self) -> dict:
        return {
            "Type": "Osobowe",
            "Make": "Audi",
            "Model": "A3",
            "ProductionYear": 2014,
            "FuelType": "Diesel",
            "Mileage": 155000,
            "EngineCapacity": 1993,
            "Transmission": "Manualna",
            "EnginePower": 150,
            "Generation": "gen-8v-2012"
        }
