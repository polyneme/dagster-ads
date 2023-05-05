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
