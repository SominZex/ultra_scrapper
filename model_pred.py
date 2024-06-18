from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import torch

def predict_category_from_input(model_path, tokenizer_path, label_mapping):
    # Load the model and tokenizer
    model = DistilBertForSequenceClassification.from_pretrained(model_path)
    tokenizer = DistilBertTokenizer.from_pretrained(tokenizer_path)

    # Get user input
    website_text = input("Enter the website text: ")

    # Tokenize the input text
    inputs = tokenizer(website_text, truncation=True, padding=True, return_tensors="pt")

    # Forward pass through the model
    outputs = model(**inputs)

    # Get the predicted label
    predicted_label = torch.argmax(outputs.logits, dim=1).item()

    # Map the label to the category
    predicted_category = label_mapping[predicted_label]

    return predicted_category


# Define paths to the saved model and tokenizer
model_path = "./models/model"
tokenizer_path = "./models/tokenizer"

# Define the label mapping dictionary
label_mapping = {
    0: 'Travel',
    1: 'Social Networking and Messaging',
    2: 'News',
    3: 'Streaming Services',
    4: 'Sports',
    5: 'Photography',
    6: 'Law and Government',
    7: 'Health and Fitness',
    8: 'Games',
    9: 'E-Commerce',
    10: 'Forums',
    11: 'Food',
    12: 'Education',
    13: 'Computers and Technology',
    14: 'Business/Corporate',
    15: 'Adult'
}

# predict anything
predicted_category = predict_category_from_input(model_path, tokenizer_path, label_mapping)
print("Predicted category:", predicted_category)
