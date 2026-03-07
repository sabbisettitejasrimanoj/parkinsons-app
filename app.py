from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from PIL import Image
import cv2
import base64
from io import BytesIO
import librosa  # for audio feature extraction

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_AUDIO = {'wav', 'mp3', 'm4a', 'flac', 'ogg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model and scaler
try:
    model = joblib.load("model.pkl")
except Exception as e:
    # handle missing or corrupted model file
    model = None
    print(f"⚠️ Could not load model.pkl: {e}")

try:
    scaler = joblib.load("scaler.pkl")
except Exception as e:
    scaler = None
    print(f"⚠️ Could not load scaler.pkl: {e}")

# ensure application doesn't crash later if artifacts are missing

# Utility Functions
def allowed_file(filename, audio=False):
    """Check if file has allowed extension. Set audio=True to validate audio files."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in (ALLOWED_AUDIO if audio else ALLOWED_EXTENSIONS)

def extract_image_features(image_path):
    """
    Extract features from image.
    For medical images (X-rays, etc.), this extracts statistical features.
    For now, generates realistic simulated features based on image characteristics.
    """
    try:
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Extract statistical features (22 features to match model input)
        features = []
        
        # Basic statistical features
        features.append(np.mean(gray))  # Mean intensity
        features.append(np.std(gray))   # Std deviation
        features.append(np.min(gray))   # Min intensity
        features.append(np.max(gray))   # Max intensity
        
        # Histogram features
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        features.extend(hist.flatten()[:4].tolist())  # First 4 histogram bins
        
        # Fill remaining features with simulated medical indicators
        # These are placeholder values that scale with image characteristics
        edge_factor = np.mean(cv2.Canny(gray, 100, 200)) / 255.0
        variance_factor = np.var(gray) / 255.0
        
        for i in range(22 - len(features)):
            # Generate features based on image content and medical likelihood
            if i % 3 == 0:
                features.append(np.mean(gray) / 255.0 * (1 + i * 0.1))
            elif i % 3 == 1:
                features.append(variance_factor * (1 + i * 0.05))
            else:
                features.append(edge_factor * (1 + i * 0.08))
        
        return np.array(features[:22]).reshape(1, -1)
    
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None


def extract_audio_features(audio_path):
    """Extract a vector of 22 audio features from a voice file."""
    try:
        y, sr = librosa.load(audio_path, sr=None)
        features = []

        # fundamental frequency via YIN
        try:
            f0 = librosa.yin(y, fmin=50, fmax=500)
            features.append(np.mean(f0))
        except Exception:
            features.append(0)

        # spectral centroid
        cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        features.append(np.mean(cent))

        # spectral bandwidth
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        features.append(np.mean(spec_bw))

        # zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)
        features.append(np.mean(zcr))

        # rolloff
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        features.append(np.mean(rolloff))

        # MFCCs (13 coefficients)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        for i in range(13):
            features.append(np.mean(mfcc[i]))

        # chroma
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features.append(np.mean(chroma))

        # pad/trim to 22
        while len(features) < 22:
            features.append(0)
        return np.array(features[:22]).reshape(1, -1)
    except Exception as e:
        print(f"Error extracting audio features: {e}")
        return None

def get_image_as_base64(image_path):
    """Convert image to base64 for display in HTML"""
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except:
        return None

@app.route("/")
def analysis():
    """Main analysis page with form and drag-drop upload"""
    return render_template("index.html")


@app.route("/info")
def info():
    """Informational home page describing Parkinson's disease"""
    return render_template("home.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Handle image upload and return image preview
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({"error": "Only JPG, JPEG, and PNG files allowed"}), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({"error": "File size exceeds 5MB limit"}), 400
        
        # Save file securely
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Convert to base64 for preview
        img_base64 = get_image_as_base64(filepath)
        
        return jsonify({
            "success": True,
            "filename": filename,
            "image_data": f"data:image/png;base64,{img_base64}",
            "message": "Image uploaded successfully"
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/upload_audio", methods=["POST"])
def upload_audio():
    """
    Handle audio upload; return filename for later prediction.
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        if not allowed_file(file.filename, audio=True):
            return jsonify({"error": "Unsupported audio format"}), 400
        # file size check
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        if size > MAX_FILE_SIZE:
            return jsonify({"error": "File size exceeds 5MB limit"}), 400
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return jsonify({"success": True, "filename": filename, "message": "Audio uploaded"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict", methods=["POST"])
def predict():
    """
    Make prediction based on uploaded image or manual features
    """
    try:
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%d-%b-%Y %H:%M:%S")
        
        # Determine input source (image, audio, or manual)
        image_source = None
        if 'image_file' in request.form and request.form['image_file']:
            filename = request.form['image_file']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(filepath):
                return render_template("error.html", 
                                     error="Uploaded image not found. Please upload again."), 400
            features = extract_image_features(filepath)
            if features is None:
                return render_template("error.html", 
                                     error="Could not process image. Please upload a valid image."), 400
            img_base64 = get_image_as_base64(filepath)
            image_source = f"data:image/png;base64,{img_base64}"

        elif 'audio_file' in request.form and request.form['audio_file']:
            filename = request.form['audio_file']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if not os.path.exists(filepath):
                return render_template("error.html",
                                     error="Uploaded audio not found. Please upload again."), 400
            features = extract_audio_features(filepath)
            if features is None:
                return render_template("error.html",
                                     error="Could not process audio file."), 400
            image_source = None  # no image

        else:
            # Manual feature input mode - only convert form values that aren't special fields
            try:
                features = [float(x) for x in request.form.values()]
                features = np.array(features).reshape(1, -1)
            except ValueError as e:
                return render_template("error.html", 
                                     error=f"Invalid input: All fields must be numbers. Error: {str(e)}"), 400
            image_source = None
        
        # ensure model and scaler are available
        if model is None or scaler is None:
            return render_template("error.html",
                                   error="Model or scaler not available. Please retrain the model by running train_model.py."), 500

        # Scale features
        scaled_features = scaler.transform(features)
        
        # Make prediction
        prediction = model.predict(scaled_features)[0]
        probability = model.predict_proba(scaled_features)[0][1] * 100
        
        # Determine risk level
        if probability < 30:
            risk = "Low"
            risk_color = "#28a745"  # Green
            recommendation = "No immediate concerns detected. Continue with regular health check-ups."
        elif probability < 60:
            risk = "Medium"
            risk_color = "#ffc107"  # Yellow/Orange
            recommendation = "Further medical evaluation is recommended. Consult with a neurologist."
        else:
            risk = "High"
            risk_color = "#dc3545"  # Red
            recommendation = "Immediate medical attention recommended. Seek professional diagnosis."
        
        return render_template("result.html",
                               prob=round(probability, 2),
                               risk=risk,
                               risk_color=risk_color,
                               timestamp=timestamp_str,
                               recommendation=recommendation,
                               image_source=image_source,
                               prediction_id=filename if ('image_file' in request.form and request.form['image_file']) else "manual_input")
    
    except ValueError as e:
        return render_template("error.html", error=f"Invalid input: {str(e)}"), 400
    except Exception as e:
        return render_template("error.html", error=f"Prediction error: {str(e)}"), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return render_template("error.html", error="File size exceeds 5MB limit"), 413

if __name__ == "__main__":
    app.run(debug=True)
