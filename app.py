from model import Model
import io, base64
from flask import Flask, render_template, request, jsonify
from PIL import Image

app = Flask(__name__)

print("Loading model...")
model = Model()
model.load()
print("Model loaded!")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def check_results():
    body = request.get_json()

    image_bytes = base64.b64decode(body['image_base64'].split(',')[1])
    image = Image.open(io.BytesIO(image_bytes))
    if image.mode != "RGB":
        image = image.convert("RGB")

    predictions = model.predict(image)
    print(predictions)

    message = predictions['Prediction']
    values = "Jim = {:.0f}%, Grinch = {:.0f}%".format(predictions['Confidences'][1] * 100, predictions['Confidences'][0] * 100)

    return jsonify({
        'message': message,
        'values': values
    })
