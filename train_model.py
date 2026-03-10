import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


def train_model(
    data_path: str = "parkinsons.csv",
    model_path: str = "model.pkl",
    scaler_path: str = "scaler.pkl",
    test_size: float = 0.2,
    random_state: int = 42,
    n_estimators: int = 200,
):
    """Load data, train random forest classifier, and save artifacts."""

    logging.info(f"Loading dataset from {data_path}")
    df = pd.read_csv(data_path)

    if "name" in df.columns:
        df = df.drop("name", axis=1)

    X = df.drop("status", axis=1)
    y = df["status"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=test_size, random_state=random_state
    )

    model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
    logging.info("Training RandomForestClassifier")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logging.info(f"Model accuracy on test set: {acc:.4f}")

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    logging.info(f"Saved model to {model_path} and scaler to {scaler_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Parkinson's detection model")
    parser.add_argument("--data", default="parkinsons.csv", help="Path to CSV dataset")
    parser.add_argument("--model", default="model.pkl", help="Output path for trained model")
    parser.add_argument("--scaler", default="scaler.pkl", help="Output path for scaler")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test set fraction")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed")
    parser.add_argument("--n-estimators", type=int, default=200, help="Number of trees")

    args = parser.parse_args()

    train_model(
        data_path=args.data,
        model_path=args.model,
        scaler_path=args.scaler,
        test_size=args.test_size,
        random_state=args.random_state,
        n_estimators=args.n_estimators,
    )

