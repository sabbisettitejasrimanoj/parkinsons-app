#!/usr/bin/env python3
"""
PARKINSON'S DETECTION - AUTOMATIC SETUP SCRIPT
Automatically downloads and sets up Kaggle dataset
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
DATASETS_DIR = PROJECT_DIR / "datasets"
SPIRAL_DIR = DATASETS_DIR / "spiral_drawings"


def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 70)
    print("🏥 PARKINSON'S DISEASE DETECTION - AUTOMATIC SETUP")
    print("=" * 70)
    print()


def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    required = {
        'kagglehub': 'kagglehub',
        'pandas': 'pandas',
        'flask': 'flask',
        'scikit-learn': 'sklearn',
        'cv2': 'opencv-python',
        'joblib': 'joblib'
    }
    
    missing = []
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nInstalling missing packages...")
        
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install"] + missing,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            print("Try manually: pip install -r requirements.txt")
            return False
    
    return True


def setup_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    
    directories = [
        DATASETS_DIR,
        SPIRAL_DIR,
        PROJECT_DIR / "data",
        PROJECT_DIR / "uploads"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory.name}")


def download_dataset():
    """Download Kaggle dataset"""
    print("\n📥 Downloading Kaggle dataset...")
    print("   Dataset: team-ai/parkinson-disease-spiral-drawings")
    
    try:
        import kagglehub
        
        print("   Downloading... (this may take a minute)")
        path = kagglehub.dataset_download(
            "team-ai/parkinson-disease-spiral-drawings"
        )
        
        print(f"   ✅ Downloaded to: {path}")
        
        # Copy files
        import shutil
        
        if os.path.exists(path):
            for item in os.listdir(path):
                src = os.path.join(path, item)
                dst = os.path.join(SPIRAL_DIR, item)
                
                if os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            
            print(f"   ✅ Copied to: {SPIRAL_DIR}")
            return True
    
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
        print("\n   Setup Kaggle authentication:")
        print("   1. Visit: https://www.kaggle.com/account")
        print("   2. Click 'Create New Token'")
        print("   3. Save kaggle.json to ~/.kaggle/")
        print("   4. Run this script again")
        return False


def verify_datasets():
    """Verify all datasets"""
    print("\n✅ Verifying datasets...")
    
    # Check vocal dataset
    vocal_path = PROJECT_DIR / "data" / "parkinsons.csv"
    if vocal_path.exists():
        print(f"   ✅ Vocal dataset: {vocal_path.name}")
    else:
        print(f"   ⚠️  Vocal dataset not found: {vocal_path}")
    
    # Check spiral images
    spiral_count = 0
    if SPIRAL_DIR.exists():
        for root, dirs, files in os.walk(SPIRAL_DIR):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    spiral_count += 1
        
        if spiral_count > 0:
            print(f"   ✅ Spiral images: {spiral_count} found")
        else:
            print(f"   ⚠️  No spiral images found in {SPIRAL_DIR}")
    else:
        print(f"   ⚠️  Spiral directory not found")


def create_config():
    """Create configuration file"""
    print("\n⚙️  Creating configuration...")
    
    config_file = PROJECT_DIR / "config.txt"
    config_content = f"""
PROJECT CONFIGURATION
====================

Project Directory: {PROJECT_DIR}
Data Directory: {PROJECT_DIR / 'data'}
Datasets Directory: {DATASETS_DIR}
Spiral Drawings: {SPIRAL_DIR}
Uploads Directory: {PROJECT_DIR / 'uploads'}

Kaggle Dataset: team-ai/parkinson-disease-spiral-drawings
Location: {SPIRAL_DIR}

Models:
- model.pkl: Trained classifier
- scaler.pkl: Feature normalizer

Features: 22 vocal characteristics + spiral analysis

Training Options:
1. Vocal Only: python train_model.py
2. Combined: python train_model_advanced.py
"""
    
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    print(f"   ✅ Config file created: {config_file.name}")


def print_next_steps():
    """Print next steps"""
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETE!")
    print("=" * 70)
    
    print("\n📋 Next Steps:")
    print("\n1. Start the web application:")
    print("   $ python app.py")
    print("\n2. Open in browser:")
    print("   http://localhost:5000")
    print("\n3. Use the system:")
    print("   - Upload spiral drawings")
    print("   - Or enter 22 vocal features manually")
    print("   - Get instant Parkinson's risk assessment")
    
    print("\n🚀 Additional Commands:")
    print("\n   Train model with spiral data:")
    print("   $ python train_model_advanced.py")
    print("\n   Manage datasets:")
    print("   $ python dataset_manager.py")
    print("\n   List spiral images:")
    print("   $ python dataset_manager.py list")
    
    print("\n📚 Documentation:")
    print("   - KAGGLE_DATASET_GUIDE.md")
    print("   - SETUP_INSTRUCTIONS.md")
    print("   - COMPLETE_DOCUMENTATION.md")
    
    print("\n" + "=" * 70 + "\n")


def main():
    """Main execution"""
    try:
        print_banner()
        
        # Step 1: Check dependencies
        if not check_dependencies():
            print("\n❌ Setup failed. Please install dependencies manually.")
            sys.exit(1)
        
        # Step 2: Create directories
        setup_directories()
        
        # Step 3: Download dataset
        print("\n" + "-" * 70)
        download_ok = download_dataset()
        
        # Step 4: Verify
        verify_datasets()
        
        # Step 5: Create config
        create_config()
        
        # Step 6: Next steps
        print_next_steps()
        
        if download_ok:
            print("🎉 All set! Your Parkinson's detection system is ready!")
        else:
            print("⚠️  Dataset not downloaded. See instructions above.")
    
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
