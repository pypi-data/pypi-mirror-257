from .diffbot import diffbot_analyze
from .fts import fts_ingest_document

import os, requests, json
def web_search(search_query: str, fast: bool = True, get_content: bool = True, links_to_read: int = 2, ingest_into_fts: bool = True, exclusions: list = ['rich_snippet', 'snippet', 'cached_links', 'hourly_forecast', 'precipitation_forecast', 'wind_forecast', 'forecast'], additional_serp_pages: int = 2):
    base_url = 'https://brainchain--search-service-v2.modal.run'
    resp = requests.get(base_url + '/search' + f'?q={search_query}')
    jsonpayload = json.loads(resp.content)
    print(jsonpayload)
    if fast:
        return jsonpayload
    
    if 'content' not in jsonpayload:
        jsonpayload["content"] = {}
        jsonpayload["content"]["by_link"] = {}
    
    
    if additional_serp_pages > 0:
        extra_links = web_scanner(search_query, additional_serp_pages=additional_serp_pages, shorten_links = False)
        jsonpayload["extra_links"] = extra_links
        
    import numpy as np
    unique_links = np.unique(jsonpayload["links"] + jsonpayload["extra_links"])

    if ingest_into_fts:
        ingested_links = [fts_ingest_document(url=link) for link in unique_links[0:links_to_read]]
        jsonpayload["ingested_links"] = ingested_links
    
    cached_links = jsonpayload['cached_links'] if 'cached_links' in jsonpayload else None
    links = jsonpayload['links'] if 'links' in jsonpayload else None

    if 'answer_box' in jsonpayload and jsonpayload['answer_box']:
        for item in jsonpayload['answer_box'].keys():
            if item in exclusions:
                jsonpayload['answer_box'][item] = None
            else:
                print(jsonpayload['answer_box'][item])
        
    if get_content:
        for link in jsonpayload["links"]:
            content = diffbot_analyze(link)
            print(content)
            jsonpayload["content"]["by_link"][link] = content
            
    return jsonpayload

def web_scanner(query: str, additional_serp_pages: int = 4, shorten_links: bool = False):
    url = 'https://brainchain--search-service-v2.modal.run'
    params = {
        "query": query,
        "additional_pages": additional_serp_pages,
        "shorten": shorten_links
    }
    response = requests.get(url + '/scanner', params=params)
    if response.status_code == 200:
        jsonpayload = response.json()

        # Deduplication logic starts here
        # Assuming the JSON payload structure is a list of dictionaries, and each dictionary represents a search result.
        # The deduplication criterion needs to be defined. Let's assume we want to dedupe based on a unique 'url' field in each dictionary.
        seen_urls = set()
        deduped_results = []
        for url in jsonpayload:
            # Adjust the following line according to the actual structure of your JSON payload.
            # Here, it is assumed that each item in the payload has a 'url' field.
            if url not in seen_urls:
                seen_urls.add(url)
                deduped_results.append(url)

        # Replace the original payload with the deduped results
        # Deduplication logic ends here

        return deduped_results
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}

def web_cache(url, get_content: bool = True):
    # figure out google web cache link
    google_cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{url}"
    if get_content:
        content = diffbot_analyze(google_cache_url)
        return {
            "url": url,
            "google_cache_url": google_cache_url,
            "content": content
        }
    else:
        return {
            "url": url,
            "google_cache_url": google_cache_url
        }

def web_content(url, ephemeral=True, use_google_web_cache=False, tags=None, exclude_tags=None):
    base_url = "https://brainchain--carnivore.modal.run"

    """Scrape content from the given URL."""
    if tags is None:
        tags = ["*"]
    if exclude_tags is None:
        exclude_tags = ["html", "script", "style"]
        
    data = {
        "url": url,
        "ephemeral": ephemeral,
        "use_google_web_cache": use_google_web_cache,
        "tags": tags,
        "exclude_tags": exclude_tags
    }

    response = requests.post(f"{base_url}/carnivore", json=data)
    return response.json()