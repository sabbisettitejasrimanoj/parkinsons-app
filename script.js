/**
 * PARKINSON'S DISEASE DETECTION SYSTEM - FRONTEND SCRIPT
 * 
 * Handles:
 * - Tab switching between Image Upload and Manual Input
 * - Drag-and-drop file upload functionality
 * - Image preview and validation
 * - Form submission and error handling
 * - UI interactions and visual feedback
 */

/**
 * Initialize when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function () {
    setupDragAndDrop();
    setupTabNavigation();
    setupFileInput();
    console.log("✅ Parkinson's Detection System initialized successfully!");
});

/**
 * Switch between tabs (Image Upload / Manual Input)
 * @param {Event} evt - Click event
 * @param {string} tabName - Name of tab to show
 */
function switchTab(evt, tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    const selectedTab = document.getElementById(tabName);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Mark button as active
    evt.currentTarget.classList.add('active');

    console.log(`📑 Switched to tab: ${tabName}`);
}

/**
 * Setup drag and drop event handlers
 */
function setupDragAndDrop() {
    const uploadBox = document.getElementById('uploadBox');
    const fileInput = document.getElementById('fileInput');

    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadBox.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    // Highlight drop area when item is dragged over it
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadBox.addEventListener(eventName, () => {
            uploadBox.classList.add('dragover');
        }, false);
    });

    // Remove highlight when dragged item leaves
    ['dragleave', 'drop'].forEach(eventName => {
        uploadBox.addEventListener(eventName, () => {
            uploadBox.classList.remove('dragover');
        }, false);
    });

    // Handle dropped files
    uploadBox.addEventListener('drop', handleDrop, false);

    // Click to upload
    uploadBox.addEventListener('click', () => fileInput.click());
}

/**
 * Prevent default drag and drop behaviors
 * @param {Event} e - Event object
 */
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

/**
 * Handle dropped files
 * @param {DragEvent} e - Drop event
 */
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

/**
 * Setup file input change handler
 */
function setupFileInput() {
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', function (e) {
        handleFiles(e.target.files);
    });
}

/**
 * Handle file selection/upload
 * @param {FileList} files - List of selected files
 */
function handleFiles(files) {
    if (files.length === 0) {
        showError("No file selected");
        return;
    }

    const file = files[0];

    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg'];
    if (!validTypes.includes(file.type)) {
        showError("❌ Invalid file type. Please upload JPG, JPEG, or PNG only.");
        return;
    }

    // Validate file size (5MB max)
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
        showError("❌ File size exceeds 5MB limit. Please choose a smaller image.");
        return;
    }

    // Show loading indicator
    showUploadStatus("Uploading image...");
    clearError();

    // Upload file via AJAX
    uploadFile(file);
}

/**
 * Upload file to server
 * @param {File} file - File to upload
 */
function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Upload failed');
                });
            }
            return response.json();
        })
        .then(data => {
            hideUploadStatus();

            if (data.success) {
                console.log("✅ File uploaded successfully:", data.filename);

                // Display preview
                showPreview(data.image_data, file.name);

                // Store filename for submission
                document.getElementById('hiddenFileName').value = data.filename;

                // Show predict button
                document.getElementById('imageForm').style.display = 'block';

                // Show success message
                showError(`✅ ${data.message}`, 'success');
            } else {
                throw new Error(data.error || 'Upload failed');
            }
        })
        .catch(error => {
            hideUploadStatus();
            console.error('❌ Upload error:', error);
            showError(`❌ Upload failed: ${error.message}`);
        });
}

/**
 * Display image preview
 * @param {string} imageSrc - Base64 encoded image
 * @param {string} filename - Original filename
 */
function showPreview(imageSrc, filename) {
    document.getElementById('previewImage').src = imageSrc;
    document.getElementById('fileName').textContent = filename;
    document.getElementById('previewContainer').style.display = 'block';
}

/**
 * Remove preview and reset upload
 */
function removePreview() {
    document.getElementById('previewContainer').style.display = 'none';
    document.getElementById('previewImage').src = '';
    document.getElementById('fileName').textContent = '';
    document.getElementById('fileInput').value = '';
    document.getElementById('hiddenFileName').value = '';
    document.getElementById('imageForm').style.display = 'none';
    clearError();
    console.log("🗑️ Preview removed");
}

/**
 * Show upload status indicator
 * @param {string} text - Status message
 */
function showUploadStatus(text) {
    const statusDiv = document.getElementById('uploadStatus');
    document.getElementById('statusText').textContent = text;
    statusDiv.style.display = 'block';
}

/**
 * Hide upload status indicator
 */
function hideUploadStatus() {
    document.getElementById('uploadStatus').style.display = 'none';
}

/**
 * Show error message
 * @param {string} message - Error message
 * @param {string} type - Message type ('error' or 'success')
 */
function showError(message, type = 'error') {
    const errorDiv = document.getElementById('errorMessage');

    if (type === 'success') {
        errorDiv.style.background = '#d4edda';
        errorDiv.style.color = '#155724';
        errorDiv.style.borderLeft = '4px solid #28a745';
    } else {
        errorDiv.style.background = '#f8d7da';
        errorDiv.style.color = '#721c24';
        errorDiv.style.borderLeft = '4px solid #dc3545';
    }

    errorDiv.textContent = message;
    errorDiv.style.display = 'block';

    // Auto-hide success messages after 5 seconds
    if (type === 'success') {
        setTimeout(clearError, 5000);
    }
}

/**
 * Clear error messages
 */
function clearError() {
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('errorMessage').textContent = '';
}

/**
 * Submit image for prediction
 */
function submitImagePrediction() {
    const filename = document.getElementById('hiddenFileName').value;

    if (!filename) {
        showError("❌ Please upload an image first");
        return;
    }

    console.log("🔬 Submitting image for prediction:", filename);

    // Show loading status
    showUploadStatus("Analyzing image...");

    // Create form and submit
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/predict';

    const fileInput = document.createElement('input');
    fileInput.type = 'hidden';
    fileInput.name = 'image_file';
    fileInput.value = filename;

    form.appendChild(fileInput);
    document.body.appendChild(form);

    // Submit form
    form.submit();
    document.body.removeChild(form);
}


/* =====================
   AUDIO FUNCTIONS
   ===================== */

// Handle audio input selection
const audioInput = document.getElementById('audioInput');
audioInput && audioInput.addEventListener('change', function(e) {
    handleAudioFiles(e.target.files);
});

function handleAudioFiles(files) {
    if (files.length === 0) {
        showAudioError("No audio selected");
        return;
    }
    const file = files[0];
    const validTypes = ['audio/wav','audio/x-wav','audio/mpeg','audio/mp3','audio/ogg','audio/flac','audio/x-m4a'];
    if (!validTypes.includes(file.type)) {
        showAudioError("❌ Unsupported audio format. Use WAV/MP3/etc.");
        return;
    }
    const maxSize = 5 * 1024 * 1024;
    if (file.size > maxSize) {
        showAudioError("❌ Audio file exceeds 5MB limit.");
        return;
    }
    clearAudioError();
    uploadAudioFile(file);
}

function uploadAudioFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    showUploadStatus("Uploading audio...");
    fetch('/upload_audio', {method:'POST', body: formData})
        .then(resp => {
            if (!resp.ok) {
                return resp.json().then(d=>{throw new Error(d.error||'Upload failed');});
            }
            return resp.json();
        })
        .then(data => {
            hideUploadStatus();
            if (data.success) {
                console.log('✅ Audio uploaded', data.filename);
                const preview = document.getElementById('previewAudio');
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
                document.getElementById('audioFileName').textContent = file.name;
                document.getElementById('audioPreview').style.display = 'block';
                document.getElementById('hiddenAudioName').value = data.filename;
                document.getElementById('audioForm').style.display = 'block';
            } else {
                throw new Error(data.error||'Upload failed');
            }
        })
        .catch(err => {
            hideUploadStatus();
            console.error('Audio upload error', err);
            showAudioError(`❌ ${err.message}`);
        });
}

function removeAudioPreview() {
    document.getElementById('previewAudio').src = '';
    document.getElementById('audioFileName').textContent = '';
    document.getElementById('audioInput').value = '';
    document.getElementById('hiddenAudioName').value = '';
    document.getElementById('audioForm').style.display = 'none';
    document.getElementById('audioPreview').style.display = 'none';
    clearAudioError();
}

function submitAudioPrediction() {
    const filename = document.getElementById('hiddenAudioName').value;
    if (!filename) {
        showAudioError('❌ Please upload audio first');
        return;
    }
    console.log('🔬 Submitting audio for prediction', filename);
    showUploadStatus('Analyzing audio...');
    const form = document.createElement('form');
    form.method='POST'; form.action='/predict';
    const field = document.createElement('input');
    field.type='hidden'; field.name='audio_file'; field.value=filename;
    form.appendChild(field);
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

function showAudioError(msg) {
    const div = document.getElementById('audioError');
    div.textContent = msg;
    div.style.display = 'block';
}

function clearAudioError() {
    const div = document.getElementById('audioError');
    div.style.display = 'none';
    div.textContent = '';
}

/**
 * Setup tab navigation keyboard support (optional)
 */
function setupTabNavigation() {
    const tabButtons = document.querySelectorAll('.tab-button');

    tabButtons.forEach((button, index) => {
        button.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') {
                e.preventDefault();
                const nextButton = tabButtons[(index + 1) % tabButtons.length];
                nextButton.click();
                nextButton.focus();
            } else if (e.key === 'ArrowLeft') {
                e.preventDefault();
                const prevButton = tabButtons[(index - 1 + tabButtons.length) % tabButtons.length];
                prevButton.click();
                prevButton.focus();
            }
        });
    });
}

console.log("📱 JavaScript module loaded and ready!");
