import os

ADS_FIELDS = [
    "id",
    "identifier",
    "bibcode",
    "title",
    "author",
    "abstract",
    "bibstem",
    "pub",
    "doi",
    "pubdate",
    "doctype",
    "keyword",
    "keyword_schema",
    "keyword_norm",
    "institution",
]

ADS_CONFIG_TOKEN = os.getenv("ADS_CONFIG_TOKEN")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
