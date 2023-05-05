from typing import Iterable

import ads
import ads.config
from dagster import ConfigurableResource

from dagster_ads.config import ADS_FIELDS


class ADSSearchQueryResource(ConfigurableResource):
    config_token: str

    def find(
        self, q: str, fl: list[str], rows: int = 2000, max_pages: int = 2
    ) -> Iterable:
        """
        setting rows=2000 (max) and max_pages=10_000 can mine the entire db, with
        the caveat that we currently have a limit of 5k queries/days so this will fail
        unless you have had your rate limits increased

        for a full list of fl field values you want to get back from the API,
        see: http://adsabs.github.io/help/search/comprehensive-solr-term-list

        query = "*:*" # gets everything
        """
        ads.config.token = self.config_token
        if q is None:
            q = """database:astronomy year:1996-2010"""
        if fl is None:
            fl = ADS_FIELDS

        return ads.SearchQuery(q=q, fl=fl, rows=rows, max_pages=max_pages)
