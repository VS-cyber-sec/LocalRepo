import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.regularizers import l2
from keras.callbacks import EarlyStopping

# ==========================================
# 1. LOAD DATASET
# ==========================================
df = pd.read_csv(
    "IMDB_Dataset.csv",
    encoding_errors='ignore',
    on_bad_lines='skip',
    engine='python'
)
print("Dataset Loaded ✅")
print(f"Total rows: {len(df)}")

# ==========================================
# 2. CLEAN DATASET
# ==========================================
df = df.dropna()
df.columns = ['review', 'sentiment']

def clean_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)       # remove HTML tags
    text = re.sub(r'[^a-zA-Z ]', '', text)  # remove symbols/numbers
    return text

df['review'] = df['review'].apply(clean_text)
df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})

print("\nSentiment Count:")
print(df['sentiment'].value_counts())

# ==========================================
# 3. TF-IDF VECTORIZATION
# ==========================================
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['review']).toarray()
y = df['sentiment']

# ==========================================
# 4. SPLIT DATA
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTraining samples : {X_train.shape[0]}")
print(f"Testing samples  : {X_test.shape[0]}")

# ==========================================
# 5. BUILD FIXED MODEL
# ==========================================
model = Sequential()

# FIX 1 - Smaller model (64→32 instead of 128→64)
model.add(Dense(64, activation='relu',
                input_shape=(X_train.shape[1],),
                kernel_regularizer=l2(0.001)))  # FIX 4 - L2 regularization

# FIX 2 - Dropout after first layer
model.add(Dropout(0.5))  # turns off 50% neurons randomly

model.add(Dense(32, activation='relu',
                kernel_regularizer=l2(0.001)))  # FIX 4 - L2 regularization

# FIX 2 - Dropout after second layer
model.add(Dropout(0.3))  # turns off 30% neurons randomly

model.add(Dense(1, activation='sigmoid'))

# ==========================================
# 6. COMPILE
# ==========================================
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)
model.summary()

# ==========================================
# 7. EARLY STOPPING (FIX 3)
# ==========================================
early_stop = EarlyStopping(
    monitor='val_accuracy',    # watch validation accuracy
    patience=3,                # stop if no improvement for 3 epochs
    restore_best_weights=True, # use best weights when stopped
    verbose=1
)

# ==========================================
# 8. TRAIN FIXED MODEL
# ==========================================
print("\nStarting Training...")
history = model.fit(
    X_train, y_train,
    epochs=20,                          # max 20 but early stop will trigger
    batch_size=32,
    validation_data=(X_test, y_test),
    callbacks=[early_stop]              # FIX 3 - early stopping
)

# ==========================================
# 9. EVALUATE
# ==========================================
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\n✅ Test Accuracy : {accuracy * 100:.2f}%")
print(f"✅ Test Loss     : {loss:.4f}")

# ==========================================
# 10. PLOT FIXED GRAPH
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy plot
axes[0].plot(history.history['accuracy'],
             label='Training Accuracy', color='blue', linewidth=2)
axes[0].plot(history.history['val_accuracy'],
             label='Validation Accuracy', color='orange', linewidth=2)
axes[0].set_title('Fixed Accuracy Graph', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Epochs')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim([0.8, 1.0])

# Loss plot
axes[1].plot(history.history['loss'],
             label='Training Loss', color='blue', linewidth=2)
axes[1].plot(history.history['val_loss'],
             label='Validation Loss', color='orange', linewidth=2)
axes[1].set_title('Fixed Loss Graph', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Epochs')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ==========================================
# 11. PREDICT YOUR OWN REVIEW
# ==========================================
def predict_review(review_text):
    cleaned = clean_text(review_text)
    vectorized = vectorizer.transform([cleaned]).toarray()
    prediction = model.predict(vectorized, verbose=0)[0][0]
    sentiment = "POSITIVE 😊" if prediction >= 0.5 else "NEGATIVE 😞"
    confidence = prediction if prediction >= 0.5 else 1 - prediction
    print(f"\nReview    : {review_text}")
    print(f"Sentiment : {sentiment}")
    print(f"Confidence: {confidence * 100:.1f}%")

# Test with sample reviews
predict_review("This movie was absolutely amazing and fantastic!")
predict_review("Terrible movie, complete waste of time.")
predict_review("The acting was okay but story was boring.")