# get_footer.py

from flask import Blueprint
from bs4 import BeautifulSoup
import requests
from .get_url import get_urls

get_footer_blueprint = Blueprint('get_footer', __name__)

def extract_footer(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Return only the content if the request is successful
        return response.content

    except requests.RequestException as e:
        # Return an error message if the request fails
        return f"Failed to retrieve content from URL. {str(e)}"

@get_footer_blueprint.route('/get_footer/<api_key>/<cse_id>/<keyword>', methods=['GET'])
def get_footer(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract the content of the footer element from each URL using BeautifulSoup
    footer_result = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        content = extract_footer(url)

        # Parsing content with BeautifulSoup to find the footer element
        soup = BeautifulSoup(content, 'html.parser')
        footer_element = soup.find('footer')

        if footer_element:
            footer_content = footer_element.text.strip()
            footer_result.append({"Website": result_number, "Footer": footer_content})
        else:
            footer_result.append({"Website": result_number, "Footer": "No footer element found"})

    return footer_result, 200
