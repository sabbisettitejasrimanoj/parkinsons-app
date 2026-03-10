"""
ADVANCED PARKINSON'S MODEL TRAINER
===================================
Supports training on vocal features + spiral drawing images
Integrates Kaggle dataset for enhanced accuracy
"""

import os
import pandas as pd
import numpy as np
import cv2
import librosa
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Project directories
PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
DATASETS_DIR = PROJECT_DIR / "datasets"
SPIRAL_DIR = DATASETS_DIR / "spiral_drawings"


class AdvancedModelTrainer:
    """Train Parkinson's detection model with multiple datasets"""

    def __init__(self):
        self.data_dir = DATA_DIR
        self.spiral_dir = SPIRAL_DIR
        self.model = None
        self.scaler = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_vocal_dataset(self):
        """Load vocal features dataset"""
        csv_path = self.data_dir / "parkinsons.csv"
        
        if not csv_path.exists():
            print(f"❌ Dataset not found: {csv_path}")
            return None
        
        print(f"📥 Loading vocal features dataset: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Drop name column if present
        if 'name' in df.columns:
            df = df.drop("name", axis=1)
        
        print(f"   ✅ Loaded {len(df)} samples")
        print(f"   Features: {len(df.columns) - 1}")
        print(f"   Classes: {df['status'].value_counts().to_dict()}")
        
        return df

    def extract_spiral_image_features(self, image_path):
        """Extract 22 features from a spiral drawing image"""
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                return None
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            features = []
            
            # Basic statistics
            features.append(np.mean(gray))
            features.append(np.std(gray))
            features.append(np.min(gray))
            features.append(np.max(gray))
            
            # Histogram features
            hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
            hist = hist.flatten() / hist.sum()
            features.extend(hist[:4].tolist())
            
            # Edge detection
            edges = cv2.Canny(gray, 100, 200)
            features.append(np.mean(edges))
            features.append(np.std(edges))
            
            # Contour features (for spiral analysis)
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            features.append(len(contours))
            
            # Moments (shape analysis)
            M = cv2.moments(gray)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                features.append(cx)
                features.append(cy)
            else:
                features.extend([0, 0])
            
            # Variance in different regions
            h, w = gray.shape
            regions = [
                gray[:h//2, :w//2],  # Top-left
                gray[:h//2, w//2:],  # Top-right
                gray[h//2:, :w//2],  # Bottom-left
                gray[h//2:, w//2:]   # Bottom-right
            ]
            for region in regions:
                features.append(np.var(region))
            
            # Laplacian (texture analysis)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            features.append(np.mean(laplacian))
            
            # Ensure we have exactly 22 features
            features = features[:22]
            while len(features) < 22:
                features.append(0)
            
            return np.array(features)
        
        except Exception as e:
            print(f"      ❌ Error processing {image_path}: {e}")
            return None

    def load_spiral_dataset(self):
        """Load spiral drawing dataset from Kaggle"""
        if not self.spiral_dir.exists():
            print(f"\n⚠️ Spiral dataset directory not found: {self.spiral_dir}")
            print("   Run: python dataset_manager.py download")
            return None, None
        
        print(f"\n📥 Loading spiral drawing images from: {self.spiral_dir}")
        
        X_spiral = []
        y_spiral = []
        
        # Look for subdirectories named "healthy" and "parkinson" (or similar)
        for label_dir in self.spiral_dir.iterdir():
            if not label_dir.is_dir():
                continue
            
            dir_name = label_dir.name.lower()
            
            # Determine label
            if "healthy" in dir_name or "normal" in dir_name or "control" in dir_name:
                label = 0
                label_text = "Healthy"
            elif "parkinson" in dir_name or "pd" in dir_name or "patient" in dir_name:
                label = 1
                label_text = "Parkinson's"
            else:
                continue
            
            print(f"   📁 Processing {label_text} samples from: {label_dir.name}")
            count = 0
            
            for image_file in label_dir.glob("*"):
                if image_file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
                    features = self.extract_spiral_image_features(image_file)
                    if features is not None:
                        X_spiral.append(features)
                        y_spiral.append(label)
                        count += 1
            
            print(f"      ✅ Loaded {count} {label_text} samples")
        
        if len(X_spiral) == 0:
            print("   ⚠️ No spiral images found in expected directories")
            return None, None
        
        X_spiral = np.array(X_spiral)
        y_spiral = np.array(y_spiral)
        
        print(f"   ✅ Total spiral samples: {len(X_spiral)}")
        return X_spiral, y_spiral

    def train_vocal_only(self):
        """Train model using only vocal features"""
        print("\n" + "=" * 60)
        print("TRAINING: VOCAL FEATURES MODEL")
        print("=" * 60)
        
        # Load data
        df = self.load_vocal_dataset()
        if df is None:
            return False
        
        # Prepare features
        X = df.drop("status", axis=1).values
        y = df["status"].values
        
        # Scale features
        print("\n🔧 Scaling features...")
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        print("📊 Splitting data (80/20)...")
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )
        
        # Train model
        print("🤖 Training Random Forest (200 trees)...")
        self.model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
        self.model.fit(self.X_train, self.y_train)
        
        # Evaluate
        self._evaluate_model()
        
        # Save
        self._save_models()
        
        return True

    def load_audio_folder(self, audio_root: Path):
        """Walk a directory tree of audio files organized by label folders.

        Expected structure:
            audio_root/healthy/*.wav
            audio_root/parkinson/*.wav
        Returns (X_audio, y_audio) or (None, None) if not found.
        """
        if not audio_root.exists():
            print(f"⚠️ Audio directory not found: {audio_root}")
            return None, None

        X_audio = []
        y_audio = []
        print(f"\n📥 Loading audio files from {audio_root}")
        for label_dir in audio_root.iterdir():
            if not label_dir.is_dir():
                continue
            name = label_dir.name.lower()
            if 'healthy' in name or 'normal' in name or 'control' in name:
                label = 0
            elif 'parkinson' in name or 'pd' in name or 'patient' in name:
                label = 1
            else:
                continue
            count = 0
            for audio_file in label_dir.glob('*'):
                if audio_file.suffix.lower() in ['.wav', '.mp3', '.flac', '.ogg', '.m4a']:
                    # extract_audio_features uses librosa logic copied from app.py
                    try:
                        y, sr = librosa.load(str(audio_file), sr=None)
                        f0 = librosa.yin(y, fmin=50, fmax=500)
                        wav_feats = [np.mean(f0)]
                        wav_feats.append(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
                        wav_feats.append(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))
                        wav_feats.append(np.mean(librosa.feature.zero_crossing_rate(y)))
                        wav_feats.append(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)))
                        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                        for i in range(13):
                            wav_feats.append(np.mean(mfcc[i]))
                        wav_feats.append(np.mean(librosa.feature.chroma_stft(y=y, sr=sr)))
                        while len(wav_feats) < 22:
                            wav_feats.append(0)
                        wav_feats = np.array(wav_feats)
                    except Exception as e:
                        print(f"   ❌ error processing audio {audio_file}: {e}")
                        continue
                    X_audio.append(wav_feats)
                    y_audio.append(label)
                    count += 1
            print(f"   ✅ Loaded {count} files from {label_dir.name}")
        if len(X_audio) == 0:
            return None, None
        return np.vstack(X_audio), np.array(y_audio)

    def train_combined(self):
        """Train model using vocal features, spiral drawings, and optionally audio files"""
        print("\n" + "=" * 60)
        print("TRAINING: COMBINED VOCAL + SPIRAL + AUDIO MODEL")
        print("=" * 60)

        # Load vocal data
        df = self.load_vocal_dataset()
        if df is None:
            print("\n⚠️ Falling back to vocal-only training...")
            return self.train_vocal_only()

        X_vocal = df.drop("status", axis=1).values
        y_vocal = df["status"].values

        # Try to load spiral data
        X_spiral, y_spiral = self.load_spiral_dataset()
        # Try to load audio recordings from folder 'audio_data'
        X_audio, y_audio = self.load_audio_folder(PROJECT_DIR / "audio_data")

        # Combine datasets
        pieces = [X_vocal]
        labels = [y_vocal]
        if X_spiral is not None:
            pieces.append(X_spiral)
            labels.append(y_spiral)
        if X_audio is not None:
            pieces.append(X_audio)
            labels.append(y_audio)

        X_combined = np.vstack(pieces)
        y_combined = np.hstack(labels)
        print(f"   ✅ Combined dataset size: {len(X_combined)} samples")
        
        # Scale features
        print("\n🔧 Scaling features...")
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_combined)
        
        # Split data
        print("📊 Splitting data (80/20)...")
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X_scaled, y_combined, test_size=0.2, random_state=42
        )
        
        # Train model
        print("🤖 Training Random Forest (200 trees)...")
        self.model = RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1)
        self.model.fit(self.X_train, self.y_train)
        
        # Evaluate
        self._evaluate_model()
        
        # Save
        self._save_models()
        
        return True

    def _evaluate_model(self):
        """Evaluate model performance"""
        print("\n📈 Evaluating model...")
        
        # Predictions
        y_pred_train = self.model.predict(self.X_train)
        y_pred_test = self.model.predict(self.X_test)
        
        # Metrics
        train_acc = accuracy_score(self.y_train, y_pred_train)
        test_acc = accuracy_score(self.y_test, y_pred_test)
        
        print(f"\n   Train Accuracy: {train_acc:.4f}")
        print(f"   Test Accuracy:  {test_acc:.4f}")
        
        # Additional metrics on test set
        precision = precision_score(self.y_test, y_pred_test, zero_division=0)
        recall = recall_score(self.y_test, y_pred_test, zero_division=0)
        f1 = f1_score(self.y_test, y_pred_test, zero_division=0)
        
        print(f"\n   Precision: {precision:.4f}")
        print(f"   Recall:    {recall:.4f}")
        print(f"   F1-Score:  {f1:.4f}")
        
        # Feature importance
        print(f"\n   Top 5 Important Features:")
        importances = self.model.feature_importances_
        top_indices = np.argsort(importances)[-5:][::-1]
        for i, idx in enumerate(top_indices, 1):
            print(f"      {i}. Feature {idx}: {importances[idx]:.4f}")

    def _save_models(self):
        """Save trained models"""
        print("\n💾 Saving models...")
        
        model_file = self.data_dir / "model.pkl"
        scaler_file = self.data_dir / "scaler.pkl"
        
        joblib.dump(self.model, model_file)
        joblib.dump(self.scaler, scaler_file)
        
        print(f"   ✅ Model saved: {model_file}")
        print(f"   ✅ Scaler saved: {scaler_file}")


def main():
    """Main execution"""
    trainer = AdvancedModelTrainer()
    
    print("\n" + "=" * 60)
    print("PARKINSON'S DETECTION - MODEL TRAINER")
    print("=" * 60)
    print("\nSelect training mode:")
    print("1. Vocal Features Only")
    print("2. Combined (Vocal + Spiral Drawings)")
    print("=" * 60)
    
    choice = input("\nEnter choice (1-2): ").strip()
    
    if choice == "1":
        trainer.train_vocal_only()
    elif choice == "2":
        trainer.train_combined()
    else:
        print("❌ Invalid choice")
        return
    
    print("\n✅ Training complete!")


if __name__ == "__main__":
    main()
