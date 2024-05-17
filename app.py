from flask import Flask, render_template, request, jsonify
from api_scrape.get_titles import get_titles
from api_scrape.get_description import get_descriptions
from api_scrape.get_url import get_urls
from api_scrape.get_keywords import get_keywords_blueprint, get_keywords
from api_scrape.get_inlinks import get_inlinks
from api_scrape.get_headings import get_heading
from api_scrape.get_contenttype import get_content_types
from api_scrape.get_footer import get_footer
from api_scrape.get_header import get_header
from api_scrape.get_alt import get_alt_tags
from api_scrape.get_viewport import get_viewport
from llama_index.core import Document, VectorStoreIndex
from llama_index.llms import openai as llama_openai
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import json
import os
import string
import re

app = Flask(__name__)

os.environ['OPENAI_API_KEY'] = "openai api key"
openai_api_key = os.environ.get("OPENAI_API_KEY")

with open("config.json") as config_file:
    config = json.load(config_file)

api_key = config.get("CUSTOM_SEARCH_API_KEY")
cse_id = config.get("CUSTOM_SEARCH_CSE_ID")
keyword_content = None

app.register_blueprint(get_keywords_blueprint, url_prefix='/api')

def preprocess_text(text):
    if isinstance(text, str):

        stop_words = set(stopwords.words('english'))
        porter = PorterStemmer()


        tokens = word_tokenize(text)
        # Lowercasing
        tokens = [word.lower() for word in tokens]

        tokens = [word for word in tokens if word not in string.punctuation]
        # Remove special characters and numbers
        tokens = [re.sub(r'[^a-zA-Z]', '', word) for word in tokens]
        # Removing stopwords
        tokens = [word for word in tokens if word not in stop_words]

        tokens = [porter.stem(word) for word in tokens]
        return ' '.join(tokens)
    elif isinstance(text, list):
        return [preprocess_text(item) for item in text]
    else:
        return text

@app.route('/inputKeyword', methods=['POST', 'GET'])
def input_keyword():
    global keyword_content

    if request.method == 'POST':
        keyword_content = request.form['keyword']
        titles = get_titles(api_key, cse_id, keyword_content)
        descriptions = get_descriptions(api_key, cse_id, keyword_content)
        urls = get_urls(api_key, cse_id, keyword_content)
        keywords_response = get_keywords(api_key, cse_id, keyword_content)
        inLinks = get_inlinks(api_key, cse_id, keyword_content)
        headings = get_heading(api_key, cse_id, keyword_content)
        footers = get_footer(api_key, cse_id, keyword_content)
        headers = get_header(api_key, cse_id, keyword_content)
        contentTypes = get_content_types(api_key, cse_id, keyword_content)
        alttags = get_alt_tags(api_key, cse_id, keyword_content)
        viewports = get_viewport(api_key, cse_id, keyword_content)

        # Preprocess all data at once
        titles = preprocess_text(titles)
        descriptions = preprocess_text(descriptions)
        urls = preprocess_text(urls)
        keywords_response = preprocess_text(keywords_response)
        inLinks = preprocess_text(inLinks)
        headings = preprocess_text(headings)
        footers = preprocess_text(footers)
        headers = preprocess_text(headers)
        contentTypes = preprocess_text(contentTypes)
        alttags = preprocess_text(alttags)
        viewports = preprocess_text(viewports)

        # Combine all meta tags into a list of documents
        documents = []
        for i in range(len(titles)):
            document = {
                "title": titles[i],
                "description": descriptions[i],
                "url": urls[i],
                "keywords": keywords_response[i],
                "inlinks": inLinks[i],
                "heading": headings[i],
                "footer": footers[i],
                "header": headers[i],
                "content_type": contentTypes[i],
                "alt_tags": alttags[i],
                "viewport": viewports[i]
            }
            documents.append(Document(text=json.dumps(document)))

        # OpenAI GPT-3.5 Turbo
        llama_openai.api_key = openai_api_key
        llm = llama_openai.OpenAI(model="gpt-3.5-turbo", temperature=0)

        vector_index = VectorStoreIndex.from_documents(documents, llm=llm)
        query_engine = vector_index.as_query_engine(response_mode="compact")
        query_part1 = "As a business owner aiming to improve the visibility of my website on Google Search Engine, I need optimized and SEO-friendly meta tags for the keyword "
        query_part2 = f"'{keyword_content}'. The meta tags should include:\n\n"
        query_part3 = "- Title: [Generate an engaging title that includes the keyword "
        query_part4 = f"'{keyword_content}']\n"
        query_part5 = "- Description: [Create a concise and informative description highlighting the relevance of the keyword "
        query_part6 = f"'{keyword_content}' to my website/business]\n"
        query_part7 = "- Keywords: [Suggest relevant keywords related to "
        query_part8 = f"'{keyword_content}' that can enhance search engine optimization]\n"
        query_part9 = "- Header: [Design an attention-grabbing header incorporating the keyword "
        query_part10 = f"'{keyword_content}']\n"
        query_part11 = "- Footer: [Craft a footer that reinforces the keyword "
        query_part12 = f"'{keyword_content}' and the purpose of my website/business]\n"
        query_part13 = "- Alt Tag: [Provide an alternative text for images related to "
        query_part14 = f"'{keyword_content}' on my website]\n"
        query_part15 = "- Inlinks: [Identify authoritative websites or internal pages with information relevant to "
        query_part16 = f"'{keyword_content}']\n"
        query_part17 = "- URL: [Ensure the URL reflects the keyword "
        query_part18 = f"'{keyword_content}' and the content of my website]\n"
        query_part19 = "- Viewport: [Recommend an appropriate viewport setting for optimal display across devices]\n"
        query_part20 = "- Content Type: [Specify the type of content on my website related to "
        query_part21 = f"'{keyword_content}']\n\n"
        query_part22 = "- H1 (Optimized Heading): [Generate an optimized H1 heading that includes the keyword "
        query_part23 = f"'{keyword_content}']\n\n"
        query_part24 = "Using the provided data and analyzing each meta tag, generate optimized meta tags in bulleted points in English language to improve the ranking of my website on Google Search Engine."

        fullQuery = query_part1 + query_part2 + query_part3 + query_part4 + query_part5 + query_part6 + query_part7 + query_part8 + query_part9 + query_part10 + query_part11 + query_part12 + query_part13 + query_part14 + query_part15 + query_part16 + query_part17 + query_part18 + query_part19 + query_part20 + query_part21 + query_part22 + query_part23 + query_part24

        response = query_engine.query(fullQuery)


        return jsonify({"message": str(response)}), 200

    else:
        return render_template('inputKeyword.html')

# Route for the index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
