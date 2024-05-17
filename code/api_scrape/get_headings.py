# get_heading.py

from flask import Blueprint
from bs4 import BeautifulSoup
import requests
from .get_url import get_urls

get_heading_blueprint = Blueprint('get_heading', __name__)

def extract_heading(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Return only the content if the request is successful
        return response.content

    except requests.RequestException as e:
        # Return an error message if the request fails
        return f"Failed to retrieve content from URL. {str(e)}"

@get_heading_blueprint.route('/get_heading/<keyword>', methods=['GET'])
def get_heading(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract the first h1 heading from each URL using BeautifulSoup
    heading_results = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        content = extract_heading(url)

        # Parsing content with BeautifulSoup to find the first h1 heading
        soup = BeautifulSoup(content, 'html.parser')
        h1_tag = soup.find('h1')

        if h1_tag:
            heading_content = h1_tag.text.strip()
            heading_results.append({"Website": result_number, "Heading": heading_content})
        else:
            heading_results.append({"Website": result_number, "Heading": "No h1 heading found"})

    return heading_results, 200
