import requests
from bs4 import BeautifulSoup
from transformers import pipeline

class SearchEngine:
    def query(self, query):
        search_query = f"https://www.google.com/search?q={query}"
        response = requests.get(search_query)
        if response.status_code == 200:
            return response.text
        else:
            return ""

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

        for result in search_results:
            link = result.find('a')['href']
            self.content_urls.append(link)

    def analyze_content(self, content):
        sentiment_analysis = self.sentiment_classifier(content)
        topic_classification = self.topic_classifier(content, candidate_labels=["technology", "sports", "politics"])
        summarized_content = self.summarizer(content, max_length=100, min_length=30, do_sample=False)

        return sentiment_analysis, topic_classification, summarized_content

    def generate_recommendations(self, sentiment, topic, summary):
        recommendations = []

        for profile in self.user_profiles.values():
            profile_interests = profile['interests']
            
            if sentiment in profile_interests and topic in profile_interests:
                recommendations.append(summary)
            
            elif topic == 'technology' and 'technology' in profile_interests:
                recommendations.append(summary)
            
            elif topic == 'sports' and 'sports' in profile_interests:
                recommendations.append(summary)
            
            elif topic == 'politics' and 'politics' in profile_interests:
                recommendations.append(summary)

        return recommendations

    def update_user_profiles(self, user_id, interests):
        if user_id in self.user_profiles:
            self.user_profiles[user_id]['interests'] = interests
        else:
            self.user_profiles[user_id] = {'interests': interests}

    def fetch_content(self):
        for url in self.content_urls:
            response = requests.get(url)
            if response.status_code == 200:
                content = response.text
                sentiment, topic, summary = self.analyze_content(content)
                recommendations = self.generate_recommendations(sentiment, topic, summary)
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