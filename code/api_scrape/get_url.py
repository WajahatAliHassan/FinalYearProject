from flask import jsonify
import requests

def get_urls(api_key, cse_id, keyword_content):
    # Construct the URL for the Custom Search API using the keyword_content
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={keyword_content}"

    # Send a GET request to the API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data:
            search_results = data['items'][:10]

            urls = []
            for i, result in enumerate(search_results):
                link = result.get('link', 'Link not found')
                urls.append({"Website": i + 1, "URL": link})

            return urls
        else:
            return jsonify({"error": "No search results found."}), 404
    else:
        return jsonify({"error": f"Failed to retrieve Google search results. Status Code: {response.status_code}"}), 500
