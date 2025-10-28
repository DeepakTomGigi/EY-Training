from transformers import pipeline

# Load the sentiment-analysis pipeline from Hugging Face
classifier = pipeline("sentiment-analysis")

# Example text
text = "I think the new design of this website is very plain It's user-friendly but also vague."

# Perform sentiment analysis
result = classifier(text)

# Print the result
print(result)
