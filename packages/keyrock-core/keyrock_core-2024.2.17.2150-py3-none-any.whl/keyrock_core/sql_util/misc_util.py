import logging
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger('')

def parse_database_url(url):
    #
    # postgres://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
    #
    if url is None:
        return {}

    parsed = urlparse(url)
    result = {
        'type': parsed.scheme,
        'host': parsed.hostname,
        'port': parsed.port,
        'user': parsed.username,
        'pass': parsed.password,
        'db': parsed.path.lstrip('/'),
    }

    if parsed.query:
        result.update(parse_qs(parsed.query))

    return result
