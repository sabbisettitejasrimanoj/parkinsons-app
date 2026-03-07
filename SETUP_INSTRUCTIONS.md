# Parkinson's Disease Detection System - Installation & Setup Guide

## 📋 Project Overview

This is an advanced AI-powered web application for detecting Parkinson's Disease using machine learning. The system features:

- ✅ **Image Upload with Drag-and-Drop** - Upload medical images for analysis
- ✅ **Manual Feature Input** - Input vocal features for prediction
- ✅ **Medical Report Card** - Professional hospital-style analysis report
- ✅ **Risk Assessment** - Low/Medium/High risk classification
- ✅ **Print-Friendly Reports** - Download/print medical reports
- ✅ **Responsive Design** - Works on desktop and mobile devices
- ✅ **Security** - File validation, size limits, and secure storage

---

## 🛠️ Prerequisites

Before installation, ensure you have:

- **Python 3.8 or higher** installed on your system
- **pip** (Python package manager)
- **Virtual Environment** (recommended)
- **Modern web browser** (Chrome, Firefox, Edge, Safari)

---

## 📦 Installation Steps

### 1. Clone or Extract Project Files

Extract the project to your desired location:
```bash
cd path/to/parkinson_project
```

### 2. Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Core dependencies:**
- Flask - Web framework
- joblib - Model and scaler serialization
- scikit-learn - Machine learning models
- Pillow (PIL) - Image processing
- OpenCV (cv2) - Computer vision operations
- NumPy - Numerical computing

### 4. Verify Model Files

Ensure these files exist in the project root:
- `model.pkl` - Trained Random Forest classifier
- `scaler.pkl` - StandardScaler for feature normalization
- `parkinsons.csv` - Training dataset (for reference)

If model files are missing, train a new model:
```bash
python train_model.py
```

### 5. Create Uploads Directory

The `uploads/` folder should exist in the project root (created automatically by the app):
```
parkinson_project/
├── uploads/          (auto-created)
│   └── [uploaded images]
├── app.py
├── model.pkl
├── scaler.pkl
└── ...
```

---

## 🚀 Running the Application

### Start Flask Development Server

```bash
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### Access the Web Application

Open your browser and navigate to:
```
http://localhost:5000
```

---

## 📖 Usage Guide

### Image Upload Tab 📸

1. **Upload Image:**
   - Click or drag-and-drop medical image (JPG, PNG, JPEG)
   - Maximum file size: 5MB
   - Image preview displays automatically

2. **Analyze:**
   - Click "🔬 Analyze Image" button
   - Features extracted automatically from image
   - ML model generates prediction

3. **View Report:**
   - Medical-style report card displays results
   - Shows probability percentage and risk level
   - Print or go back for new analysis

### Manual Input Tab 🔢

1. **Enter Features:**
   - Fill in 22 vocal features from medical test
   - All fields required
   - Use decimal values (e.g., 0.123)

2. **Predict:**
   - Click "🔬 Predict Status" button
   - Instant prediction results

3. **View Report:**
   - Formatted report displays results
   - Professional medical styling

---

## 🔬 Feature Extraction from Images

The system extracts the following statistical features from uploaded images:

- **Mean Intensity** - Average pixel value
- **Standard Deviation** - Variation in pixel values
- **Min/Max Intensity** - Intensity range
- **Histogram Features** - Distribution of pixel values
- **Edge Detection** - Canny edge features
- **Variance Factors** - Image variation metrics

These features are scaled and fed to the trained Random Forest classifier.

---

## 📊 ML Model Details

**Model:** Random Forest Classifier
- **Estimators:** 200 trees
- **Split Ratio:** 80% train, 20% test
- **Features:** 22 vocal features
- **Scaler:** StandardScaler (mean=0, std=1)

**To retrain the model:**
```bash
python train_model.py
```

---

## 🎨 File Structure

```
parkinson_project/
├── app.py                      # Flask backend
├── train_model.py              # Model training script
├── model.pkl                   # Trained model
├── scaler.pkl                  # Feature scaler
├── parkinsons.csv              # Training dataset
├── requirements.txt            # Python dependencies
├── uploads/                    # Uploaded images directory
├── templates/
│   ├── index.html             # Home page (tabs interface)
│   ├── result.html            # Medical report card
│   └── error.html             # Error page
├── static/
│   ├── style.css              # Complete styling
│   └── script.js              # Frontend logic
└── README.md                   # This file
```

---

## 🔒 Security Features

1. **File Type Validation** - Only jpg, jpeg, png allowed
2. **File Size Limit** - Maximum 5MB per upload
3. **Secure Filenames** - Using werkzeug.utils.secure_filename
4. **Timestamp Prefixes** - Prevents filename collisions
5. **Error Handling** - Graceful error messages without exposing system details
6. **Input Sanitization** - All user inputs validated

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError" when running app.py

**Solution:**
```bash
pip install flask joblib scikit-learn pillow opencv-python numpy
```

### Issue: "model.pkl not found"

**Solution:**
```bash
python train_model.py
```

### Issue: Port 5000 already in use

**Solution:** 
Modify `app.py` last line:
```python
app.run(debug=True, port=5001)  # Use different port
```

### Issue: Images not uploading

**Check:**
- File format is JPG, PNG, or JPEG
- File size is less than 5MB
- Uploads folder has write permissions
- Browser console for JavaScript errors (F12)

### Issue: Prediction fails on manual input

**Check:**
- All 22 fields are filled
- Values are valid numbers
- Try with smaller decimal values

---

## 🌐 Deployment

### For Production Use:

1. **Disable Debug Mode** - Replace `debug=True` with `debug=False`

2. **Use Production Server** - Replace Flask dev server:
```bash
pip install gunicorn
gunicorn app:app
```

3. **Set Environment Variables:**
```bash
export FLASK_ENV=production
```

4. **Configure Security:**
   - Set `SECRET_KEY` in Flask config
   - Use HTTPS/SSL certificates
   - Add CORS if needed

5. **Database Setup** (optional):
   - Store predictions in database
   - Track patient histories

---

## 📈 Performance Optimization

- Images are processed efficiently with OpenCV
- Features cached during analysis
- CSS uses minimal repaints
- JavaScript optimized for responsiveness

---

## 📝 Medical Disclaimer

⚠️ **IMPORTANT:**

This AI system is for educational and research purposes only. It is NOT a substitute for professional medical diagnosis. 

Always consult qualified healthcare professionals for:
- Definitive diagnosis
- Treatment decisions
- Medical advice

The predictions are based on machine learning patterns and may not be 100% accurate.

---

## 📊 Example Results

### Low Risk (< 30%)
- Status: **Low Risk**
- Color: 🟢 Green
- Recommendation: Continue regular health check-ups

### Medium Risk (30-60%)
- Status: **Medium Risk**
- Color: 🟡 Yellow/Orange
- Recommendation: Further medical evaluation recommended

### High Risk (> 60%)
- Status: **High Risk**
- Color: 🔴 Red
- Recommendation: Immediate medical attention recommended

---

## 🎓 Academic Details

**Project Type:** Final Year AI & Data Science Project

**Technology Stack:**
- Frontend: HTML5, CSS3, JavaScript (Vanilla)
- Backend: Python 3, Flask
- ML: Scikit-Learn, Random Forest
- Image Processing: OpenCV, Pillow
- Database: Optional (CSV for now)

**Features Implemented:**
- ✅ Drag-and-drop file upload
- ✅ Image feature extraction
- ✅ Medical report card generation
- ✅ Risk stratification
- ✅ Responsive UI/UX
- ✅ Error handling & validation
- ✅ Security best practices
- ✅ Print functionality

---

## 📞 Support & Documentation

- Check error messages in browser console (F12)
- Review Flask server logs in terminal
- Verify all dependencies installed: `pip list`
- Test with sample images first

---

## 📄 License

This project is for educational purposes.

---

## ✨ Credits

Built as a comprehensive upgrade to showcase:
- Full-stack web development
- Machine learning integration
- UX/UI best practices
- Medical AI applications
- Professional software engineering

---

## 🚀 Future Enhancements

Potential improvements for production:

1. **Database Integration** - Store predictions and patient records
2. **Real Image Analysis** - Use pre-trained medical image models
3. **Multi-Model Ensemble** - Combine multiple ML models
4. **User Authentication** - Doctor/patient login system
5. **PDF Report Generation** - Server-side PDF creation
6. **API Documentation** - REST API with Swagger docs
7. **Admin Dashboard** - Analytics and reporting
8. **Mobile App** - Native mobile application

---

**Last Updated:** February 2026  
**Version:** 2.0 (Upgraded with Image Support)

For questions or issues, refer to the inline code comments and documentation.

Happy analyzing! 🎉
