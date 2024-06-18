from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

class WebsiteCategorizer:
    def __init__(self, model_path, tokenizer_path):
        self.tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_path)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_path)
        self.categories = [
            'Travel',
            'Social Networking and Messaging',
            'News',
            'Streaming Services',
            'Sports',
            'Photography',
            'Law and Government',
            'Health and Fitness',
            'Games',
            'E-Commerce',
            'Forums',
            'Food',
            'Education',
            'Computers and Technology',
            'Business/Corporate',
            'Adult'
        ]

    def categorize_website(self, website_content):
        # Tokenize input text
        inputs = self.tokenizer(website_content, return_tensors='pt', truncation=True, padding=True)

        # Perform inference
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Get predicted label
        predicted_label = torch.argmax(outputs.logits).item()

        # Map label to category name
        category = self.categories[predicted_label] if predicted_label < len(self.categories) else "Uncategorized"

        return category
