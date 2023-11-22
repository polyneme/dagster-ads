from typing import Iterable

import ads
import ads.config
import botocore
import boto3
from dagster import (
    ConfigurableResource,
    ConfigurableIOManager,
    InputContext,
    OutputContext,
    ResourceDependency,
)
from dagster_aws.s3 import S3Resource

from dagster_ads.config import ADS_FIELDS_ALL


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
            fl = ADS_FIELDS_ALL

        return ads.SearchQuery(q=q, fl=fl, rows=rows, max_pages=max_pages)


class DO_S3_Resource(ConfigurableResource):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str = "nyc3"
    endpoint_url: str = "https://nyc3.digitaloceanspaces.com"

    def get_client(self):
        session = boto3.session.Session()
        return session.client(
            "s3",
            config=botocore.config.Config(s3={"addressing_style": "virtual"}),
            region_name=self.region_name,
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )


class ADS_S3_ConfigurableIOManager(ConfigurableIOManager):
    s3_resource: ResourceDependency[DO_S3_Resource]
    s3_bucket: str

    def _get_path(self, context) -> str:
        return "/".join(["ads"] + context.asset_key.path)

    def handle_output(self, context: OutputContext, obj):
        self.s3_resource.get_client().put_object(
            Bucket=self.s3_bucket, Key=self._get_path(context), Body=obj, ACL="private"
        )

    def load_input(self, context: InputContext):
        return (
            self.s3_resource.get_client()
            .get_object(Bucket=self.s3_bucket, Key=self._get_path(context))["Body"]
            .read()
        )
