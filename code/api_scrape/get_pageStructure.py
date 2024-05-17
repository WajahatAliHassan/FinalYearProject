# get_keywords.py

from flask import Blueprint, jsonify
from bs4 import BeautifulSoup
import requests
from .get_url import get_urls

get_keywords_blueprint = Blueprint('get_pageStructure', __name__)

@get_keywords_blueprint.route('/get_pageStructure', methods=['GET'])
def get_pageStructure(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract keywords from each URL using BeautifulSoup
    pageStructure_results = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            soup = BeautifulSoup(response.text, 'html.parser')
            structure = {
            "Headers": len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])),
            "Paragraphs": len(soup.find_all('p')),
            "Forms": len(soup.find_all('form')),
            "Lists": len(soup.find_all(['ul', 'ol'])),
            "Tables": len(soup.find_all('table')),
            "Footer": len(soup.find_all('footer')),

            # Add more sections as needed: tables, forms, etc.
        }
            pageStructure_results.append({"Website": result_number, "Page Structure": structure})


        except requests.RequestException as e:
            return jsonify({"error": f"Failed to retrieve content from URL. {str(e)}"}), 500

    return pageStructure_results, 200
