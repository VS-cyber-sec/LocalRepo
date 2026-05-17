import numpy as np
import matplotlib.pyplot as plt

from keras.datasets import fashion_mnist
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.utils import to_categorical # one - hor encoding but not used

(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
print("Training Data Shape :", x_train.shape)
print("Testing Data Shape  :", x_test.shape)

x_train = x_train / 255.0  #normalize pixel values to [0,1]
x_test = x_test / 255.0

# Step 5: Class Labels
class_names = [
    'T-shirt/top',
    'Trouser',
    'Pullover',
    'Dress',
    'Coat',
    'Sandal',
    'Shirt',
    'Sneaker',
    'Bag',
    'Ankle boot'
]

# Step 6: Display Sample Images
plt.figure(figsize=(10,10))
#Creates a 3×3 grid showing first 9 training images:

for i in range(9):
    plt.subplot(3,3,i+1)
    plt.imshow(x_train[i], cmap='gray')
    plt.title(class_names[y_train[i]])
    plt.axis('off')

plt.show()

# Step 7: Build Deep Neural Network Model
model = Sequential([
    Flatten(input_shape=(28,28)),   #reshapes 28x28 images into 1D array of 784 pixels
    
    Dense(128, activation='relu'), #fully connected layer with 128 neurons and ReLU activation function
    Dense(64, activation='relu'), #relu activation function introduces non-linearity, allowing the model to learn complex patterns in the data.
    
    Dense(10, activation='softmax') # softmax activation function is used in the output layer for multi-class classification, providing probabilities for each of the 10 classes.
])

# Step 8: Compile Model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',  #Multi-class with integer labels
    metrics=['accuracy']
)

# Step 9: Train Model
history = model.fit(
    x_train,  # imgases
    y_train,   #labels
    epochs=10,
    validation_split=0.2
)

# Step 10: Evaluate Model
test_loss, test_accuracy = model.evaluate(x_test, y_test)

print("\nTest Accuracy :", test_accuracy)

# Step 11: Predict on Test Data
predictions = model.predict(x_test)

# Step 12: Show Prediction Example
index = 5

plt.imshow(x_test[index], cmap='gray')
plt.title("Predicted : " + class_names[np.argmax(predictions[index])])
plt.axis('off')
plt.show()
 #np.argmax() finds index of highest probability
#Shows image with predicted label as title


print("Actual Label    :", class_names[y_test[index]])
print("Predicted Label :", class_names[np.argmax(predictions[index])])

# Step 14: Plot Loss Graph
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')

plt.legend(['Training Loss', 'Validation Loss'])

plt.show()# Step 13: Plot Accuracy Graph
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title('Model Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')

plt.legend(['Training Accuracy', 'Validation Accuracy'])

plt.show()