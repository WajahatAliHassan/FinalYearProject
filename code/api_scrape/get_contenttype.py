# get_contenttype.py

from flask import Blueprint
import requests
from .get_url import get_urls

get_contenttype_blueprint = Blueprint('get_contenttype', __name__)

@get_contenttype_blueprint.route('/get_contenttype/<api_key>/<cse_id>/<keyword>', methods=['GET'])
def get_content_types(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract content types from each URL using requests.head() method
    content_types = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        try:
            # Send a HEAD request to the URL to get only the headers
            response = requests.head(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            # Extract Content-Type from response headers
            content_type = response.headers.get('Content-Type')
            content_types.append({"Website": result_number, "Content-Type": content_type})

        except requests.RequestException as e:
            content_types.append({"Website": result_number, "Content-Type": f"Failed to retrieve content type. {str(e)}"})

    return content_types, 200
