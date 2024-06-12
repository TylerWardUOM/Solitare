import pyautogui
import cv2
import numpy as np
from PIL import Image
import pytesseract

#im currently screenshoting a solitare app i got open onleft half of screen
screenshot = pyautogui.screenshot(region=(0,150, 1200, 1250))

# Convert the screenshot to a format OpenCV can use
screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

# Save the screenshot for verification (optional)
cv2.imwrite('screenshot.png', screenshot)

# Convert the screenshot to HSV color space for better color filtering
hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)

# Define the range for white color in HSV space
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 55, 255])

# Threshold the HSV image to get only white colors
mask = cv2.inRange(hsv, lower_white, upper_white)

# Bitwise-AND mask and original image
filtered = cv2.bitwise_and(screenshot, screenshot, mask=mask)

# Convert the filtered image to grayscale
gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

# Use Canny edge detection to detect edges
edges = cv2.Canny(gray, 50, 150)

# Apply morphological operations to close gaps in the edges
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

# Find contours in the edge-detected image
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours for visualization
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    # Filter out small or large contours that are unlikely to be cards
    if 500 < w * h < 50000:  # Adjust these values based on your card size
        cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Display the contours
cv2.imshow('Contours', screenshot)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Improve OCR preprocessing
def preprocess_card(image):
    # Resize for better OCR accuracy
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # Apply Gaussian blur to reduce noise
    image = cv2.GaussianBlur(image, (5, 5), 0)
    # Enhance contrast
    image = cv2.convertScaleAbs(image, alpha=2.0, beta=0)
    # Apply adaptive thresholding
    image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                  cv2.THRESH_BINARY, 11, 2)
    return image

# Use OCR to read card values (if needed)
cards = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if 500 < w * h < 50000:  # Adjust these values based on your card size
        card_image = gray[y:y + h, x:x + w]
        preprocessed_card = preprocess_card(card_image)
        card_text = pytesseract.image_to_string(preprocessed_card, config='--psm 6 --oem 3')
        cards.append(card_text.strip())

# Print the detected cards
print(cards)
