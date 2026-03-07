"""
PARKINSON'S DISEASE DATASET MANAGER
=====================================
Downloads and manages datasets from Kaggle and local sources
Supports both vocal features and spiral drawing images
"""

import os
import sys
import shutil
import pandas as pd
import numpy as np
from pathlib import Path

# Try to import kagglehub for Kaggle dataset download
try:
    import kagglehub
    KAGGLE_AVAILABLE = True
except ImportError:
    KAGGLE_AVAILABLE = False
    print("⚠️ kagglehub not installed. Install with: pip install kagglehub")

# Project directories
PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
DATASETS_DIR = PROJECT_DIR / "datasets"
SPIRAL_DRAWINGS_DIR = DATASETS_DIR / "spiral_drawings"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
DATASETS_DIR.mkdir(exist_ok=True)
SPIRAL_DRAWINGS_DIR.mkdir(exist_ok=True)


class DatasetManager:
    """Manage and download Parkinson's datasets"""

    def __init__(self):
        self.data_dir = DATA_DIR
        self.datasets_dir = DATASETS_DIR
        self.spiral_dir = SPIRAL_DRAWINGS_DIR

    def download_spirals_from_kaggle(self):
        """
        Download Parkinson's spiral drawings dataset from Kaggle
        Dataset: team-ai/parkinson-disease-spiral-drawings
        """
        if not KAGGLE_AVAILABLE:
            print("❌ ERROR: kagglehub not installed")
            print("Install with: pip install kagglehub")
            return False

        try:
            print("📥 Downloading Parkinson's Spiral Drawings dataset from Kaggle...")
            print("   Dataset: team-ai/parkinson-disease-spiral-drawings")

            # Download dataset
            path = kagglehub.dataset_download(
                "team-ai/parkinson-disease-spiral-drawings"
            )
            
            print(f"✅ Dataset downloaded to: {path}")
            
            # Copy to project datasets folder
            if os.path.exists(path):
                # Get the full path with all subdirectories
                for item in os.listdir(path):
                    src = os.path.join(path, item)
                    dst = os.path.join(self.spiral_dir, item)
                    
                    if os.path.isdir(src):
                        if os.path.exists(dst):
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)
                        print(f"   Copied folder: {item}")
                    else:
                        shutil.copy2(src, dst)
                        print(f"   Copied file: {item}")
                
                print(f"\n✅ Dataset copied to: {self.spiral_dir}")
                return True
            else:
                print(f"❌ Download path not found: {path}")
                return False

        except Exception as e:
            print(f"❌ Error downloading dataset: {e}")
            return False

    def list_spiral_drawings(self):
        """List all spiral drawing images in the dataset"""
        print(f"\n📁 Spiral Drawings in {self.spiral_dir}:")
        
        if not self.spiral_dir.exists():
            print("   Directory not found. Download dataset first.")
            return []

        images = []
        for root, dirs, files in os.walk(self.spiral_dir):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                    path = os.path.join(root, file)
                    images.append(path)
                    print(f"   - {os.path.relpath(path, self.spiral_dir)}")

        print(f"\n   Total images found: {len(images)}")
        return images

    def analyze_spiral_dataset_structure(self):
        """Analyze and display dataset structure"""
        print("\n📊 Dataset Structure:")
        print("=" * 50)

        if not self.spiral_dir.exists():
            print("Directory not found. Download dataset first.")
            return

        for root, dirs, files in os.walk(self.spiral_dir):
            level = root.replace(str(self.spiral_dir), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f'{indent}{os.path.basename(root)}/')
            
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files
                print(f'{subindent}{file}')
            
            if len(files) > 5:
                print(f'{subindent}... and {len(files) - 5} more files')

    def verify_vocal_dataset(self):
        """Verify the vocal features CSV dataset"""
        csv_path = self.data_dir / "parkinsons.csv"
        
        if csv_path.exists():
            print(f"\n✅ Vocal Dataset Found: {csv_path}")
            df = pd.read_csv(csv_path)
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {list(df.columns[:5])}... ({len(df.columns)} total)")
            print(f"   Classes: {df['status'].value_counts().to_dict()}")
            return True
        else:
            print(f"\n⚠️ Vocal Dataset not found: {csv_path}")
            return False

    def create_dataset_info(self):
        """Create a dataset information file"""
        info_file = self.datasets_dir / "DATASET_INFO.txt"
        
        info_text = """
PARKINSON'S DISEASE DATASETS
============================

1. VOCAL FEATURES DATASET
   Location: data/parkinsons.csv
   Type: CSV (Tabular)
   Features: 22 vocal characteristics
   Samples: 195 patients
   Classes: 2 (Healthy=0, Parkinson's=1)
   Source: Original Parkinson's dataset

2. SPIRAL DRAWINGS DATASET
   Location: datasets/spiral_drawings/
   Type: Images (JPG/PNG)
   Description: Hand-drawn spiral images
   Use Case: Image-based classification
   Source: Kaggle (team-ai/parkinson-disease-spiral-drawings)
   
   Dataset Structure:
   - Healthy: Spiral drawings from healthy individuals
   - Parkinson: Spiral drawings from Parkinson's patients
   
   Image Analysis:
   - Can extract texture features
   - Can analyze drawing quality
   - Can detect tremor patterns

FEATURES EXTRACTED FROM SPIRAL IMAGES:
- Mean intensity
- Standard deviation
- Min/Max values
- Histogram distributions
- Edge detection (Canny)
- Variance metrics
- Tremor indicators

USAGE IN APPLICATION:
1. Upload your spiral drawing image
2. System automatically extracts 22 compatible features
3. ML model makes prediction
4. Medical report generated with risk assessment
"""
        
        with open(info_file, 'w') as f:
            f.write(info_text)
        
        print(f"\n📝 Dataset info saved: {info_file}")

    def setup_datasets(self):
        """Complete setup of all datasets"""
        print("\n" + "=" * 60)
        print("PARKINSON'S DATASET SETUP")
        print("=" * 60)
        
        # Verify vocal dataset
        print("\n1️⃣ Checking Vocal Features Dataset...")
        vocal_ok = self.verify_vocal_dataset()
        
        # Download spiral drawings
        print("\n2️⃣ Downloading Spiral Drawings Dataset...")
        if KAGGLE_AVAILABLE:
            spiral_ok = self.download_spirals_from_kaggle()
        else:
            print("   ⚠️ Kaggle credentials not configured")
            print("   Setup instructions:")
            print("   1. Install: pip install kagglehub")
            print("   2. Login: kagglehub.login()")
            print("   3. Re-run this script")
            spiral_ok = False
        
        # List spiral images
        if spiral_ok or self.spiral_dir.exists():
            print("\n3️⃣ Analyzing Spiral Dataset Structure...")
            self.analyze_spiral_dataset_structure()
            self.list_spiral_drawings()
        
        # Create info file
        print("\n4️⃣ Creating Dataset Information...")
        self.create_dataset_info()
        
        print("\n" + "=" * 60)
        print("SETUP COMPLETE")
        print("=" * 60)
        print("\n✅ Datasets ready for use!")
        print("   Vocal features: Use for manual input")
        print("   Spiral drawings: Use for image upload")
        
        return vocal_ok


def display_menu():
    """Display interactive menu"""
    print("\n" + "=" * 60)
    print("PARKINSON'S DATASET MANAGER")
    print("=" * 60)
    print("\n1. Setup all datasets")
    print("2. Download Spiral Drawings from Kaggle")
    print("3. List Spiral Drawing images")
    print("4. Verify Vocal Dataset")
    print("5. View Spiral Dataset Structure")
    print("6. Exit")
    print("\n" + "=" * 60)


def main():
    """Main execution"""
    manager = DatasetManager()
    
    while True:
        display_menu()
        choice = input("Select option (1-6): ").strip()
        
        if choice == "1":
            manager.setup_datasets()
        
        elif choice == "2":
            if KAGGLE_AVAILABLE:
                manager.download_spirals_from_kaggle()
            else:
                print("\n❌ kagglehub not installed")
                print("Install with: pip install kagglehub")
        
        elif choice == "3":
            manager.list_spiral_drawings()
        
        elif choice == "4":
            manager.verify_vocal_dataset()
        
        elif choice == "5":
            manager.analyze_spiral_dataset_structure()
        
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid option. Try again.")


if __name__ == "__main__":
    # If run with argument, execute specific function
    if len(sys.argv) > 1:
        manager = DatasetManager()
        command = sys.argv[1]
        
        if command == "download":
            manager.download_spirals_from_kaggle()
        elif command == "list":
            manager.list_spiral_drawings()
        elif command == "verify":
            manager.verify_vocal_dataset()
        elif command == "info":
            manager.create_dataset_info()
        elif command == "setup":
            manager.setup_datasets()
        else:
            print(f"Unknown command: {command}")
            print("Available: download, list, verify, info, setup")
    else:
        # Run interactive menu
        main()
