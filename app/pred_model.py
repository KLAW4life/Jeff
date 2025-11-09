
# import torch
# from transformers import BertTokenizer, BertForSequenceClassification
# import os

# # 1️⃣ Load the same tokenizer and model architecture
# model_name = "bert-base-uncased"
# tokenizer = BertTokenizer.from_pretrained(model_name)

# # num_labels = 23 
# num_labels = 18 
# model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

# # 2️⃣ Load your trained weights
# # model_path = os.path.join(os.path.dirname(__file__), "JeffModel.pth")
# model_path = os.path.join(os.path.dirname(__file__), "model.pth")
# model.load_state_dict(torch.load(model_path, map_location="cpu"))
# model.eval()

# # 3️⃣ Helper function for prediction
# def predict_emotion(text):
#     # Tokenize the input text
#     inputs = tokenizer(
#         text,
#         return_tensors="pt",
#         truncation=True,
#         padding=True,
#         max_length=128
#     )

#     # Run the model
#     with torch.no_grad():
#         outputs = model(**inputs)
#         logits = outputs.logits
#         probs = torch.sigmoid(logits).squeeze()  # multi-label emotion output
#     return probs.numpy()

# # 4️⃣ Example use
# if __name__ == "__main__":
#     test_text = "You look so familiar, but I can’t remember your name."
#     predictions = predict_emotion(test_text)
#     print("\nPredicted emotion probabilities:")
#     print(predictions)

#     # Optional: if you have emotion column names, print them with labels
#     emotion_cols = ["afraid", "angry", "anxious", "ashamed", "awkward", "bored", "calm",
#     "confused", "disgusted", "excited", "frustrated", "happy", "jealous",
#     "nostalgic", "proud", "sad", "satisfied", "surprised"]  # 18 labels
#     # emotion_cols = ["afraid", "angry", "anxious", "ashamed", "awkward", "bored", "calm",
#     # "confused", "disgusted", "excited", "frustrated", "happy", "jealous",
#     # "nostalgic", "proud", "sad", "satisfied", "surprised", "fear", "love", "joy", "surprise", "anger"]  # 23 labels

#     print("\nLabeled predictions:")
#     for label, score in zip(emotion_cols, predictions):
#         print(f"{label:<10} → {score:.3f}")

import torch
from transformers import BertTokenizer, BertForSequenceClassification
import os
import numpy as np

# Load tokenizer and model architecture
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)

# num_labels = 23 
num_labels = 18 
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

# Load trained weights
model_path = os.path.join(os.path.dirname(__file__), "model.pth")
model.load_state_dict(torch.load(model_path, map_location="cpu"))
model.eval()

# Emotion labels
emotion_cols = [
    "afraid", "angry", "anxious", "ashamed", "awkward", "bored", "calm",
    "confused", "disgusted", "excited", "frustrated", "happy", "jealous",
    "nostalgic", "proud", "sad", "satisfied", "surprised"
]

# Helper function for prediction
def predict_emotion(text, top_k=3):
    # Tokenize the input text
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    # Run the model
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.sigmoid(logits).squeeze()  # multi-label probabilities

    probs = probs.numpy()

    # Get top-k indices
    top_indices = np.argsort(probs)[-top_k:][::-1]
    top_emotions = [(emotion_cols[i], probs[i]) for i in top_indices]

    return probs, top_emotions

# Test Example
if __name__ == "__main__":
    test_text = "You look so familiar, but I can’t remember your name."
    probs, top3 = predict_emotion(test_text, top_k=3)

    print("\n Top 3:")
    for emotion, score in top3:
        print(f"{emotion:<10} → {score:.3f}")

    print("\nAll Probabilities:")
    for label, score in zip(emotion_cols, probs):
        print(f"{label:<10} → {score:.3f}")