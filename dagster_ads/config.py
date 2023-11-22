import os

# List of allowed values for query-string parameter `fl` at
#   https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/search/query
#   plus cross-referencing with
#   https://ui.adsabs.harvard.edu/help/search/comprehensive-solr-term-list
ADS_FIELDS_ALL = (
    "abstract",
    "ack",
    "aff",
    "aff_id",
    "alternate_bibcode",
    "alternate_title",
    "arxiv_class",
    "author",
    "author_count",
    "author_norm",
    "bibcode",
    "bibgroup",
    "bibstem",
    "caption",  # recently added?
    "citation",
    "citation_count",
    "cite_read_boost",
    "classic_factor",
    "comment",
    "copyright",
    "data",
    "database",
    "date",
    "doctype",
    "doi",
    "eid",
    "entdate",
    "entry_date",
    "esources",
    "facility",
    "first_author",
    "first_author_norm",
    "grant",
    "grant_agencies",  # deprecated?
    "grant_id",  # deprecated?
    "id",
    "identifier",
    "indexstamp",
    "inst",  # retrievable?
    "isbn",
    "issn",
    "issue",
    "keyword",
    "keyword_norm",
    "keyword_schema",
    "lang",
    "links_data",
    "nedid",
    "nedtype",
    "orcid_other",
    "orcid_pub",
    "orcid_user",
    "page",
    "page_count",
    "page_range",  # deprecated?
    "property",
    "pub",
    "pub_raw",
    "pubdate",
    "pubnote",
    "read_count",
    "reference",
    "simbid",
    "title",
    "vizier",
    "volume",
    "year",
)

ADS_CONFIG_TOKEN = os.getenv("ADS_CONFIG_TOKEN")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
