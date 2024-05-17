from flask import Blueprint, jsonify
import requests

descriptions_bp = Blueprint('descriptions_bp', __name__)

@descriptions_bp.route('/api_scrape/get_descriptions', methods=['POST'])
def get_descriptions(api_key, cse_id, keyword_content):
    # Construct the URL for the Custom Search API using the keyword_content
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={keyword_content}"

    # Send a GET request to the API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            search_results = data['items'][:10]

            descriptions = []
            for i, result in enumerate(search_results):
                description = result.get('snippet', 'Description not found')
                descriptions.append({"Website": i + 1, "Description": description})

            return descriptions
        else:
            return jsonify({"error": "No search results found."}), 404
    else:
        return jsonify({"error": f"Failed to retrieve Google search results. Status Code: {response.status_code}"}), 500
