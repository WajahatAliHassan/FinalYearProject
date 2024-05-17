# get_nav_structure.py

from flask import Blueprint, jsonify
from bs4 import BeautifulSoup
import requests
from .get_url import get_urls

get_keywords_blueprint = Blueprint('get_navStructure', __name__)

@get_keywords_blueprint.route('/get_navStructure', methods=['GET'])
def get_navStructure(api_key, cse_id, keyword):
    # Get the top 10 URLs for the specified keyword
    urls = get_urls(api_key, cse_id, keyword)

    # Extract navigation structure from each URL using BeautifulSoup
    navStructure_results = []
    for url_data in urls:
        url = url_data.get('URL')
        result_number = url_data.get('Website')

        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract navigation structure
            nav_structure = {
                "NavBars": len(soup.find_all(['nav', 'header'])),
                "Menus": len(soup.find_all('ul', class_='menu')),
                "Links": len(soup.find_all('nav','a'))
            }

            navStructure_results.append({"Website": result_number, "Navigation Structure": nav_structure})

        except requests.RequestException as e:
            return jsonify({"error": f"Failed to retrieve content from URL. {str(e)}"}), 500

    return navStructure_results, 200
