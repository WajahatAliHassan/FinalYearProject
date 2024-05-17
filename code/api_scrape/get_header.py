# get_footer.py

from flask import Blueprint
from bs4 import BeautifulSoup
import requests
from .get_url import get_urls

get_footer_blueprint = Blueprint('get_header', __name__)

def extract_header(url):
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
def get_header(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract the content of the footer element from each URL using BeautifulSoup
    header_result = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        content = extract_header(url)

        # Parsing content with BeautifulSoup to find the footer element
        soup = BeautifulSoup(content, 'html.parser')
        header_element = soup.find('footer')

        if header_element:
            header_content = header_element.text.strip()
            header_result.append({"Website": result_number, "Header": header_content})
        else:
            header_result.append({"Website": result_number, "Header": "No footer element found"})

    return header_result, 200
