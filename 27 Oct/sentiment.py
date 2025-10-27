from transformers import pipeline

# Load the sentiment-analysis pipeline from Hugging Face
classifier = pipeline("sentiment-analysis")

# Example text
text = "I love the new design of this website! It's so user-friendly and fast."

# Perform sentiment analysis
result = classifier(text)

# Print the result
print(result)
