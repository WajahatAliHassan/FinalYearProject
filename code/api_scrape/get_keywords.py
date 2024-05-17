# get_keywords.py

from flask import Blueprint
from bs4 import BeautifulSoup
import requests
from .get_url import get_urls

get_keywords_blueprint = Blueprint('get_keywords', __name__)

def extract_keywords(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Return only the content if request is successful
        return response.content

    except requests.RequestException as e:
        # Return an error message if the request fails
        return f"Failed to retrieve content from URL. {str(e)}"

@get_keywords_blueprint.route('/get_keywords/<keyword>', methods=['GET'])
def get_keywords(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract keywords from each URL using BeautifulSoup
    keyword_results = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        content = extract_keywords(url)

        # Parsing content with BeautifulSoup to find meta keywords
        soup = BeautifulSoup(content, 'html.parser')
        meta_keywords_tag = soup.find('meta', {'name': 'Keywords'}) or soup.find('meta', {'name': 'keywords'})

        if meta_keywords_tag:
            keywords_content = meta_keywords_tag.get('content')
            keyword_results.append({"Website": result_number, "Keywords": keywords_content})
        else:
            keyword_results.append({"Website": result_number, "Keywords": "No meta keywords tag found"})

    return keyword_results, 200
