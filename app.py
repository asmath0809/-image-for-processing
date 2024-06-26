from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Function to perform OCR on uploaded image
def perform_ocr(image):
    text = pytesseract.image_to_string(image)
    words = text.split()
    return words

# Route for uploading images
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            img = Image.open(file.stream)
            words = perform_ocr(img)
            word_counts = Counter(words)
            
            # Generate plot
            plt.figure(figsize=(10, 6))
            top_words = dict(word_counts.most_common(10))  # Top 10 words
            plt.bar(top_words.keys(), top_words.values())
            plt.xlabel('Words')
            plt.ylabel('Frequency')
            plt.title('Top 10 Word Frequencies')
            plt.xticks(rotation=45)
            
            # Convert plot to base64 for embedding in HTML
            img_stream = BytesIO()
            plt.savefig(img_stream, format='png')
            img_stream.seek(0)
            plot_url = base64.b64encode(img_stream.getvalue()).decode('utf8')
            
            return render_template('result.html', words=word_counts, plot_url=plot_url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
