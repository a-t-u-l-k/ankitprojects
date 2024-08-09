import os
import requests
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, pipeline
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

# Set up API keys and endpoints
NEWS_API_KEY = 'd771c54e4d464c5a92203c23fd14c160'
CURRENTS_API_KEY = 'Lzd2R_VYgdDSLJbch2Dkpuc2PkCr43Xqe1lIhw_Pp5jOqwo6'
NEWS_API_URL = 'https://newsapi.org/v2/everything'
CURRENTS_API_URL = 'https://api.currentsapi.services/v1/latest-news'

# Initialize tokenizer and model for Pegasus
pegasus_tokenizer = PegasusTokenizer.from_pretrained('google/pegasus-xsum')
pegasus_model = PegasusForConditionalGeneration.from_pretrained('google/pegasus-xsum')
pegasus_summarizer = pipeline("summarization", model=pegasus_model, tokenizer=pegasus_tokenizer)

# Define constants
PEGASUS_MAX_LENGTH = 1024  # Max length for Pegasus
BIGBIRD_MAX_LENGTH = 8000  # Max length for BigBird
DEFAULT_OUTPUT_DIR = r"D:\Summarisation project"

# Function to split text into chunks of max_length
def split_text_into_chunks(text, max_length):
    tokens = text.split()  # Simple tokenization by splitting on spaces
    chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
    return [' '.join(chunk) for chunk in chunks]

# Function to summarize text using Pegasus
def summarize_pegasus(text):
    chunks = split_text_into_chunks(text, PEGASUS_MAX_LENGTH)
    summaries = []
    for chunk in chunks:
        if len(chunk) > PEGASUS_MAX_LENGTH:
            chunk = chunk[:PEGASUS_MAX_LENGTH]
        summary = pegasus_summarizer(chunk, max_length=PEGASUS_MAX_LENGTH, min_length=50, do_sample=False)
        summaries.append(summary[0]['summary_text'])
    return ' '.join(summaries)

# Function to download and summarize articles
def process_articles(category, num_articles):
    output_dir = os.path.join(DEFAULT_OUTPUT_DIR, category)
    os.makedirs(output_dir, exist_ok=True)

    articles = fetch_articles(category, num_articles)
    
    if not articles:
        print(f"No articles found for category '{category}'.")
        return
    
    for i, article in enumerate(tqdm(articles, desc=f"Summarizing {category} articles")):
        try:
            article_text = download_article(article['url'])
            summary = summarize_pegasus(article_text)
            
            output_path = os.path.join(output_dir, f"{category}{i + 1}.json")
            with open(output_path, 'w') as file:
                json.dump({
                    'original_text': article_text,
                    'summary': summary
                }, file, indent=4)
            
            print(f"Processed and saved article {i + 1} for category '{category}'.")
        
        except Exception as e:
            print(f"Error summarizing article {i + 1} for category '{category}': {e}")
            continue

# Function to fetch articles from APIs
def fetch_articles(category, num_articles):
    articles = []
    for api_url, api_key in [(NEWS_API_URL, NEWS_API_KEY), (CURRENTS_API_URL, CURRENTS_API_KEY)]:
        response = requests.get(api_url, params={'apiKey': api_key, 'q': category, 'pageSize': num_articles})
        if response.status_code == 200:
            data = response.json()
            articles.extend(data.get('articles', []))
        else:
            print(f"Failed to fetch articles from {api_url}. Status code: {response.status_code}")
    return articles[:num_articles]

# Function to download article content
def download_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return ' '.join(p.get_text() for p in paragraphs)
    else:
        raise Exception(f"Failed to download article from {url}. Status code: {response.status_code}")

# Main function to drive the script
def main():
    while True:
        category_input = input("Enter categories (space-separated, e.g., business technology): ")
        categories = [cat.strip() for cat in category_input.split()]
        
        for category in categories:
            num_articles = int(input(f"How many articles per category for '{category}'? "))
            process_articles(category, num_articles)
        
        more_categories = input("Do you want to process more categories (y/n)? ").lower() == 'y'
        if not more_categories:
            break

if __name__ == "__main__":
    main()
