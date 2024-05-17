# get_viewport.py

from flask import Blueprint
from bs4 import BeautifulSoup
import requests
from .get_url import get_urls

get_viewport_blueprint = Blueprint('get_viewport', __name__)

@get_viewport_blueprint.route('/get_viewport/<api_key>/<cse_id>/<keyword>', methods=['GET'])
def get_viewport(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract navigation structure from each URL using BeautifulSoup
    viewport = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            soup = BeautifulSoup(response.text, 'html.parser')
            viewport_tag= soup.find('meta', {'name': 'viewport'})
            if viewport_tag:
                viewport_content = viewport_tag.get('content')
                viewport.append({"Website": result_number, "Viewport Meta Tag": viewport_content})
            else:
                viewport.append({"Website": result_number, "Viewport Meta Tag":"No Viewport Meta Tag Found"})

        except requests.RequestException as e:
            viewport.append({"Website": result_number, "Viewport Meta Tag": f"Failed to retrieve viewport meta tags. {str(e)}"})

    return viewport, 200
