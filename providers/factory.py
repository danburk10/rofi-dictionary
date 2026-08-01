# providers/factory.py

#from providers.api_provider import ApiProvider
#from providers.cache_provider import CacheProvider
#from providers.json_provider import JsonProvider
from providers.sqlite_2_provider import SqliteProvider


class ProviderFactory:

    @staticmethod
    def create(provider_type: str):
        provider_type = provider_type.lower()



        if provider_type == "sqlite_wordnet31_provider":
            return SqliteProvider("data/wordnet31.db")

        """
        if provider_type == "api":
            return ApiProvider("https://api.dictionaryapi.dev")

        if provider_type == "json":
            return JsonProvider("data/dictionary.json")

        if provider_type == "cached_api":
            return CacheProvider(
                ApiProvider("https://api.dictionaryapi.dev")
            )
        """
        raise ValueError(f"Unknown provider type: {provider_type}")
