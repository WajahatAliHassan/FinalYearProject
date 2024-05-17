# get_inlinks.py

from flask import Blueprint
from bs4 import BeautifulSoup
import requests
from .get_url import get_urls

get_inlinks_blueprint = Blueprint('get_inlinks', __name__)

def extract_inlinks(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Return only the content if the request is successful
        return response.content

    except requests.RequestException as e:
        # Return an error message if the request fails
        return f"Failed to retrieve content from URL. {str(e)}"

@get_inlinks_blueprint.route('/get_inlinks/<api_key>/<cse_id>/<keyword>', methods=['GET'])
def get_inlinks(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract inlinks from each URL using BeautifulSoup
    inlinks_result = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        content = extract_inlinks(url)

        # Parsing content with BeautifulSoup to find inlinks
        soup = BeautifulSoup(content, 'html.parser')
        inlinks = []  # Create a list to store inlinks as strings

        # Counter to limit to top 10 inlinks per URL
        count = 0
        for link in soup.find_all('a', href=True):
            if count < 10:
                # Check if the href value is a string
                if isinstance(link['href'], str):
                    # Add the href value to the list
                    inlinks.append(link['href'])
                count += 1
            else:
                break

        # Convert inlinks list to strings
        inlinks = list(map(str, inlinks))

        # Append the result to the main inlinks_result list
        inlinks_result.append({"Website": result_number, "Inlinks/Outlinks": inlinks})

    return inlinks_result, 200
