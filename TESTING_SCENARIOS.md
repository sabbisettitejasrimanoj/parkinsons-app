# Testing Scenarios & Step-by-Step Walkthrough

## 🧪 Complete Testing Checklist

### Pre-Testing Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify model files exist
ls model.pkl scaler.pkl

# 3. Start server
python app.py

# 4. Open browser
# http://localhost:5000
```

---

## 📸 SCENARIO 1: Image Upload Flow

### Test Case 1.1: Successful JPG Upload

**Steps:**
1. Click "📸 Image Upload" tab
2. Drag JPG file to upload box
3. See "Uploading image..." spinner
4. Preview displays uploaded image
5. Filename shown below preview
6. "Remove" button is active
7. "🔬 Analyze Image" button appears

**Expected Result:** ✅ Image preview displayed, analysis button enabled

---

### Test Case 1.2: Successful PNG Upload

**Steps:**
1. Stay on Image Upload tab
2. Click upload box (no drag)
3. Browse to PNG file
4. Select and open
5. Same flow as 1.1

**Expected Result:** ✅ PNG processed successfully

---

### Test Case 1.3: File Type Validation (Invalid Format)

**Steps:**
1. Try to upload GIF file
2. Observe response

**Expected Result:** ❌ Error: "Only JPG, JPEG, and PNG files allowed"

---

### Test Case 1.4: File Size Validation (Too Large)

**Steps:**
1. Create 10MB+ test image
2. Try to upload
3. Observe error

**Expected Result:** ❌ Error: "File size exceeds 5MB limit"

---

### Test Case 1.5: Image Preview Removal

**Steps:**
1. Upload valid image
2. Preview displays
3. Click "Remove" button
4. Preview disappears
5. Try uploading different image

**Expected Result:** ✅ Old preview cleared, ready for new upload

---

### Test Case 1.6: Analyze Button After Upload

**Steps:**
1. Upload image
2. Click "🔬 Analyze Image"
3. Wait for processing
4. Report card displays

**Expected Result:** ✅ Report card shows with probability and risk

---

## 🔢 SCENARIO 2: Manual Input Flow

### Test Case 2.1: Valid Input Submission

**Steps:**
```
1. Click "🔢 Manual Input" tab
2. Note: 22 fields required
3. Fill first field: 197.0
4. Fill remaining fields with test values
5. All fields must have numbers
6. Click "🔬 Predict Status"
```

**Test Values Template:**
```
MDVP:Fo(Hz) = 197.0
MDVP:Fhi(Hz) = 238.0
MDVP:Flo(Hz) = 157.0
MDVP:Jitter(%) = 0.007
MDVP:Jitter(Abs) = 0.00005
MDVP:RAP = 0.003
MDVP:PPQ = 0.003
Jitter:DDP = 0.009
MDVP:Shimmer = 0.027
MDVP:Shimmer(dB) = 0.25
Shimmer:APQ3 = 0.015
Shimmer:APQ5 = 0.019
MDVP:APQ = 0.018
Shimmer:DDA = 0.046
NHR = 0.015
HNR = 24.5
RPDE = 0.48
DFA = 0.7
spread1 = 0.6
spread2 = 0.4
D2 = 2.5
PPE = 0.19
```

**Expected Result:** ✅ Prediction made, report displays

---

### Test Case 2.2: Missing Required Field

**Steps:**
1. Fill only 21 fields (leave one blank)
2. Click "🔬 Predict Status"

**Expected Result:** ❌ Form validation prevents submission

---

### Test Case 2.3: Invalid Data (Non-numeric)

**Steps:**
1. Fill all fields with numbers
2. Change one field to "abc"
3. Click "🔬 Predict Status"

**Expected Result:** ❌ Error message about invalid input

---

### Test Case 2.4: Large Values Testing

**Steps:**
1. Fill all fields with very large values (e.g., 999999)
2. Submit
3. Model handles scaling

**Expected Result:** ✅ Model processes (scaler normalizes)

---

## 📊 SCENARIO 3: Prediction Results

### Test Case 3.1: Low Risk Result (<30%)

**Setup:** Use healthy patient values (from actual dataset)

**Values for Low Risk:**
```
MDVP:Fo(Hz) = 120.0
(Use typical healthy vocal values)
```

**Expected Result:**
- 🟢 Green risk badge "Low"
- Probability shows <30%
- Green progress bar
- Recommendation: "Continue with regular health check-ups"

---

### Test Case 3.2: Medium Risk Result (30-60%)

**Expected Result:**
- 🟡 Orange/Yellow risk badge "Medium"
- Probability shows 30-60%
- Orange progress bar
- Recommendation: "Further medical evaluation recommended"

---

### Test Case 3.3: High Risk Result (>60%)

**Expected Result:**
- 🔴 Red risk badge "High"
- Probability shows >60%
- Red progress bar
- Recommendation: "Immediate medical attention recommended"

---

### Test Case 3.4: Report Card Display

**Report Elements to Verify:**
- [ ] Date and time stamp displays
- [ ] Analysis ID shows
- [ ] Patient image visible (if uploaded)
- [ ] Probability percentage shows
- [ ] Progress bar accurate
- [ ] Risk level color correct
- [ ] Recommendation text appropriate
- [ ] Disclaimer visible
- [ ] Print and New Analysis buttons present

---

## 🎨 SCENARIO 4: UI/UX Testing

### Test Case 4.1: Tab Switching

**Steps:**
1. Load page
2. Image Upload tab active by default
3. Click Manual Input tab
4. Manual form displays
5. Click Image Upload tab
6. Image upload section displays

**Expected Result:** ✅ Smooth tab transitions, content switches correctly

---

### Test Case 4.2: Responsive Mobile View

**Using Chrome DevTools:**

**Test Case 4.2a: Mobile 320px width**
- Lines stack properly
- Buttons full width
- Text readable
- Images scale

**Test Case 4.2b: Tablet 768px width**
- 2-column layout appears
- Proper spacing

**Test Case 4.2c: Desktop 1024px+**
- Full layout
- Optimal spacing

---

### Test Case 4.3: Error Message Display

**Steps:**
1. Trigger various errors:
   - Upload wrong file type
   - File too large
   - Missing form fields
   - Invalid values

**Expected Result:** ✅ Clear, helpful error messages

---

### Test Case 4.4: Loading Indicators

**Steps:**
1. Upload image
2. Watch spinner during upload
3. Status text updates

**Expected Result:** ✅ Visual feedback during processing

---

## 🖨️ SCENARIO 5: Report Card Features

### Test Case 5.1: Print Functionality

**Steps:**
1. Generate prediction report
2. Press Ctrl+P (or print button)
3. Preview print dialog
4. Check layout

**Expected Result:** ✅ Clean print preview, no navbar/buttons

---

### Test Case 5.2: New Analysis Button

**Steps:**
1. View report card
2. Click "🏠 New Analysis"
3. Return to home page

**Expected Result:** ✅ After clicking, form resets, ready for new input

---

### Test Case 5.3: Image Display in Report

**Steps:**
1. Upload image
2. Get prediction
3. Report shows uploaded image

**Expected Result:** ✅ Patient image visible in report

---

## 🔒 SCENARIO 6: Security Testing

### Test Case 6.1: File Extension Bypass

**Steps:**
1. Rename executable to .jpg
2. Try to upload
3. Monitor for errors

**Expected Result:** ✅ File saved but can't be opened (not a real image)

---

### Test Case 6.2: Path Traversal Attempt

**Steps:**
1. Try filename like "../../../malicious.jpg"
2. Upload

**Expected Result:** ✅ Filename sanitized, stored safely

---

### Test Case 6.3: Large File DoS

**Steps:**
1. Try uploading 100MB file
2. Expect error before server processes

**Expected Result:** ✅ Size limit enforced (413 error)

---

## 📈 SCENARIO 7: Performance Testing

### Test Case 7.1: Image Processing Speed

**Measurement:**
- Time from upload to preview: Should be <2 seconds
- Time from analysis click to report: Should be <3 seconds

---

### Test Case 7.2: Manual Input Speed

**Measurement:**
- Time from submit to report: Should be <1 second

---

### Test Case 7.3: Multiple Successive Predictions

**Steps:**
1. Make 5 predictions in a row
2. No errors
3. No slowdown

**Expected Result:** ✅ Consistent performance

---

## 🔄 SCENARIO 8: Browser Compatibility

Test on:
- [ ] Chrome/Edge (Chromium-based)
- [ ] Firefox
- [ ] Safari (if macOS available)
- [ ] Mobile browsers (iOS Safari, Chrome Android)

**Expected Result:** ✅ Works on all modern browsers

---

## 📋 Issue Logging Template

When issues occur:

```
BUG REPORT
----------
Title: [Short description]
Severity: Critical / High / Medium / Low
Steps to Reproduce:
  1. [step 1]
  2. [step 2]
  3. [step 3]
Expected Result: [what should happen]
Actual Result: [what happened]
Screenshots: [if applicable]
Browser: [Chrome/Firefox/Safari/etc]
OS: [Windows/Mac/Linux]
```

---

## ✅ Final Verification Checklist

Before declaring project complete:

- [ ] All 22 test cases pass
- [ ] No console errors (F12)
- [ ] No server errors
- [ ] Mobile responsive works
- [ ] Print outputs correctly
- [ ] Security checks pass
- [ ] Performance acceptable
- [ ] Documentation complete
- [ ] Code well-commented
- [ ] Project ready for submission

---

## 📝 Test Results Summary

**Date:** __________  
**Tester:** __________  
**Browser:** __________  
**OS:** __________  

### Results:
- Total Test Cases: 26+
- Passed: ___
- Failed: ___
- Blocked: ___
- Not Tested: ___

**Overall Status:** ✅ Ready / ⚠️ Needs Fixes / ❌ Not Ready

---

**Use this checklist to systematically verify all functionality before submission!**
