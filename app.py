from flask import Flask, render_template, request, redirect, url_for, jsonify
import tensorflow as tf
import numpy as np
import os

app = Flask(__name__)

# Load the trained models
model_potato = tf.keras.models.load_model('models/potato.h5')
model_tomato = tf.keras.models.load_model('models/tomato.hdf5')

# Define class names
potato_class_names = ['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']
tomato_class_names = ['Tomato_Early_blight', 'Tomato_Leaf_Mold', 'Tomato__Tomato_mosaic_virus', 'Tomato_healthy']

# Define prediction functions for potato and tomato
def predict_potato(img_path, model, class_names):
    try:
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * np.max(predictions[0]), 2)
        return predicted_class, confidence
    except Exception as e:
        return 'Error occurred during prediction.', 0

def predict_tomato(img_path, model, class_names):
    try:
        img = tf.keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, 0)
        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = round(100 * np.max(predictions[0]), 2)
        return predicted_class, confidence
    except Exception as e:
        return 'Error occurred during prediction.', 0
    
# Route to render the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to render the selection page
@app.route('/selection', methods=['GET', 'POST'])
def selection():
    if request.method == 'POST':
        choice = request.form['choice']
        if choice == 'potato':
            return redirect(url_for('potato'))
        elif choice == 'tomato':
            return redirect(url_for('tomato'))
    return render_template('selection.html')

# Route to render the potato page
@app.route('/potato')
def potato():
    return render_template('potato.html')

# Route to render the tomato page
@app.route('/tomato')
def tomato():
    return render_template('tomato.html')

# Route to handle image upload and disease prediction
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        file = request.files['file']
        img_path = 'temp_image.jpg'
        file.save(img_path)
        if request.path == '/upload_tomato':  # Check if tomato page
            prediction, confidence = predict_tomato(img_path, model_tomato, tomato_class_names)
        else:  # Assume potato page
            prediction, confidence = predict_potato(img_path, model_potato, potato_class_names)
        os.remove(img_path)
        return jsonify({'prediction': prediction, 'confidence': confidence})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/upload_tomato', methods=['POST'])
def upload_tomato_image():
    try:
        file = request.files['file']
        img_path = 'temp_image.jpg'
        file.save(img_path)
        prediction, confidence = predict_tomato(img_path, model_tomato, tomato_class_names)
        os.remove(img_path)
        return jsonify({'prediction': prediction, 'confidence': confidence})
    except Exception as e:
        return jsonify({'error': str(e)})
# Define routes for other pages (potato disease types, about us, contact us, etc.)
@app.route('/potato_earlyblight')
def potato_earlyblight():
    print("Rendering Potato___Early_blight.html")  # Log when rendering the template
    try:
        return render_template('Potato___Early_blight.html')
    except Exception as e:
        print(f"Error rendering Potato___Early_blight.html: {e}")  # Log any rendering errors
        return "Error rendering template"

@app.route('/potato_lateblight')
def potato_lateblight():
    print("Rendering Potato___Late_blight.html")  # Log when rendering the template
    try:
        return render_template('Potato___Late_blight.html')
    except Exception as e:
        print(f"Error rendering Potato___Late_blight.html: {e}")  # Log any rendering errors
        return "Error rendering template"

@app.route('/potato_healthy')
def potato_healthy():
    print("Rendering Potato___healthy.html")  # Log when rendering the template
    try:
        return render_template('Potato___healthy.html')
    except Exception as e:
        print(f"Error rendering Potato___healthy.html: {e}")  # Log any rendering errors
        return "Error rendering template"

@app.route('/back_to_index')
def back_to_potato():
    return redirect(url_for('index'))
# Similarly, define routes for tomato pages and prediction

@app.route('/how_it_works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

# Route to render the Tomato Early Blight page
@app.route('/Tomato_Early_blight')
def tomato_early_blight():
    return render_template('Tomato_Early_blight.html')

# Route to render the Tomato Leaf Mold page
@app.route('/Tomato_Leaf_Mold')
def tomato_leaf_mold():
    return render_template('Tomato_Leaf_Mold.html')

# Route to render the Tomato Mosaic Virus page
@app.route('/Tomato__Tomato_mosaic_virus')
def tomato_mosaic_virus():
    return render_template('Tomato__Tomato_mosaic_virus.html')

# Route to render the Tomato Healthy page
@app.route('/Tomato_healthy')
def tomato_healthy():
    return render_template('Tomato_healthy.html')


if __name__ == '__main__':
    app.run(debug=True)
