# Quick Start Guide - Parkinson's Detection System

## ⚡ Get Running in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

**If that fails, install individually:**
```bash
pip install flask joblib scikit-learn pillow opencv-python
```

### Step 2: Verify Model Files

Check if these files exist in project root:
- ✅ `model.pkl` (trained model)
- ✅ `scaler.pkl` (feature scaler)

If missing, train:
```bash
python train_model.py
```

### Step 3: Start Application (1 minute)

```bash
python app.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
```

### Step 4: Open Browser

Go to:
```
http://localhost:5000
```

---

## 🚀 Using the Application

### Option A: Upload Image

1. **Click "📸 Image Upload" tab**
2. **Drag & drop medical image** (JPG/PNG, <5MB)
3. **Click "🔬 Analyze Image"**
4. **View report card** with risk assessment

### Option B: Manual Input

1. Click **"🔢 Manual Input"** tab
2. Fill in **22 vocal features**
3. Click **"🔬 Predict Status"**
4. View **analysis report**

---

## 📊 Example Test Values

For manual input, try these typical values:

```
MDVP:Fo(Hz): 197.0
MDVP:Fhi(Hz): 238.0
MDVP:Flo(Hz): 157.0
MDVP:Jitter(%): 0.007
MDVP:Jitter(Abs): 0.00005
MDVP:RAP: 0.003
MDVP:PPQ: 0.003
Jitter:DDP: 0.009
MDVP:Shimmer: 0.027
MDVP:Shimmer(dB): 0.25
Shimmer:APQ3: 0.015
Shimmer:APQ5: 0.019
MDVP:APQ: 0.018
Shimmer:DDA: 0.046
NHR: 0.015
HNR: 24.5
RPDE: 0.48
DFA: 0.7
spread1: 0.6
spread2: 0.4
D2: 2.5
PPE: 0.19
```

---

## 🎨 Features Overview

| Feature | Details |
|---------|---------|
| 🖼️ Image Upload | Drag-drop, automatic preview |
| 📝 Manual Form | 22 medical features |
| 🤖 ML Model | Random Forest, 200 trees |
| 📊 Report Card | Medical-style format |
| 🎨 Color-Coded Risk | Green/Orange/Red |
| 🖨️ Print Report | Browser print function |
| 📱 Responsive | Works on phone/tablet/desktop |

---

## 🐛 Quick Troubleshooting

### Issue: "Port already in use"
Edit `app.py`, last line:
```python
app.run(debug=True, port=5001)
```

### Issue: "model.pkl not found"
```bash
python train_model.py
```

### Issue: "ModuleNotFoundError"
```bash
pip install --upgrade flask joblib scikit-learn
```

### Issue: Images not uploading
- Check file is JPG/PNG
- Verify size <5MB
- Try a different image

---

## 📚 Full Documentation

For detailed information, see:
- `SETUP_INSTRUCTIONS.md` - Complete setup guide
- `COMPLETE_DOCUMENTATION.md` - Technical details
- Code comments in `app.py` and `script.js`

---

## ✨ What's New in v2.0

✅ Image upload with drag-and-drop  
✅ Automatic image-to-features extraction  
✅ Medical-style report card  
✅ Professional UI/UX  
✅ Mobile responsive  
✅ Security best practices  
✅ Error handling  
✅ Print support  

---

## 🎓 Project Info

**Type:** Final Year AI & Data Science Project  
**Tech Stack:** Python, Flask, HTML5, CSS3, JavaScript  
**ML Model:** Random Forest (scikit-learn)  
**Status:** Production Ready ✅  

---

**Need Help?** Check SETUP_INSTRUCTIONS.md or review code comments.

**Happy Analyzing!** 🎉
