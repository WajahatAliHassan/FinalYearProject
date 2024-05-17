# get_alt_tags.py

from flask import Blueprint
from bs4 import BeautifulSoup
import requests
from .get_url import get_urls

get_alt_tags_blueprint = Blueprint('get_alt_tags', __name__)

@get_alt_tags_blueprint.route('/get_alt_tags/<api_key>/<cse_id>/<keyowrd>', methods=['GET'])
def get_alt_tags(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract navigation structure from each URL using BeautifulSoup
    alt_tags = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')
            image_alt_tags = [img.get('alt') for img in images if img.get('alt')]
            alt_tags.append({"Website": result_number, "Alt Tags": image_alt_tags})

        except requests.RequestException as e:
            alt_tags.append({"Website": result_number, "Alt Tags": f"Failed to retrieve alt tags. {str(e)}"})

    return alt_tags, 200
