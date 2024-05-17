from flask import Blueprint, jsonify
import requests

titles_bp = Blueprint('titles_bp', __name__)

@titles_bp.route('/api_scrape/get_titles', methods=['POST'])
def get_titles(api_key, cse_id, keyword_content):
    # Construct the URL for the Custom Search API using the keyword_content
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={keyword_content}"

    # Send a GET request to the API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            search_results = data['items'][:10]

            titles = []
            for i, result in enumerate(search_results):
                title = result.get('title', 'Title not found')
                titles.append({"Website": i + 1, "Title": title})

            return titles, 200
        else:
            return jsonify({"error": "No search results found."}), 404
    else:
        return jsonify({"error": f"Failed to retrieve Google search results. Status Code: {response.status_code}"}), 500
