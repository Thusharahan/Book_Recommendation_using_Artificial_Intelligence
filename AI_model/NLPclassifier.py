from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from torch.nn.functional import softmax
import torch

# Load pre-trained DistilBERT model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')
model.eval()

# Define classes for classification
classes = ["Genre", "Title", "General"]

def classify_user_input_distilbert(input_text):
    # Tokenize input text
    inputs = tokenizer(input_text, return_tensors='pt', truncation=True, padding=True)

    try:
        # Get model predictions
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Apply softmax to get probabilities
        probabilities = softmax(outputs.logits, dim=1).squeeze().tolist()

        # Get the predicted class
        predicted_class = classes[probabilities.index(max(probabilities))]

        return predicted_class

    except Exception as e:
        # Handle any errors that may occur during inference
        print(f"Error during inference: {e}")
        return "Unknown"