Certainly! Here's a refactored version of your script that follows best practices and aims for better performance and readability:

```python
from transformers import pipeline
from bs4 import BeautifulSoup
import requests


class SearchEngine:
    @staticmethod
    def query(query):
        search_query = f"https://www.google.com/search?q={query}"
        response = requests.get(search_query)
        return response.text if response.status_code == 200 else ""


class ContentCuration:
    def __init__(self):
        self.user_profiles = {}
        self.content_urls = []
        self.sentiment_classifier = pipeline("sentiment-analysis")
        self.topic_classifier = pipeline("zero-shot-classification")
        self.summarizer = pipeline("summarization")

    def extract_urls(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        search_results = soup.find_all('div', class_='r')
        self.content_urls = [result.find('a')['href']
                             for result in search_results]

    def analyze_content(self, content):
        sentiment_analysis = self.sentiment_classifier(content)[0]
        topic_classification = self.topic_classifier(
            content, candidate_labels=["technology", "sports", "politics"])[0]
        summarized_content = self.summarizer(
            content, max_length=100, min_length=30, do_sample=False)[0]['summary_text']

        return sentiment_analysis, topic_classification, summarized_content

    def generate_recommendations(self, sentiment, topic, summary):
        recommendations = []

        for profile in self.user_profiles.values():
            profile_interests = set(profile['interests'])

            if sentiment in profile_interests and topic in profile_interests:
                recommendations.append(summary)
            elif topic in profile_interests or (topic == 'technology' and 'technology' in profile_interests):
                recommendations.append(summary)

        return recommendations

    def update_user_profiles(self, user_id, interests):
        self.user_profiles[user_id] = {'interests': interests}

    def fetch_content(self):
        for url in self.content_urls:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                sentiment, topic, summary = self.analyze_content(content)
                recommendations = self.generate_recommendations(
                    sentiment, topic, summary)

                # Store recommendations in the user profiles or any other desired output


if __name__ == '__main__':
    content_curation = ContentCuration()
    search_engine = SearchEngine()
    queries = ["Python programming", "Machine learning", "Data analysis"]
    user_profiles = {
        "user1": {"interests": ["technology", "machine learning"]},
        "user2": {"interests": ["data analysis"]}
    }

    for query in queries:
        search_results = search_engine.query(query)
        content_curation.extract_urls(search_results)
        content_curation.fetch_content()

    for user_id, profile in user_profiles.items():
        content_curation.update_user_profiles(user_id, profile['interests'])
```

Here are the major improvements made to the original script:

1. The `sentiment_classification`, `topic_classification`, and `summarized_content` variables now only store the necessary values from the output of the respective pipelines, improving performance.
2. `profile_interests` is converted to a set before checking for membership, which allows for faster look-ups during recommendations generation.
3. The summary text is extracted correctly using `['summary_text']` in the summarizer output.
4. Minor improvements were made to variable names and code formatting to enhance readability.