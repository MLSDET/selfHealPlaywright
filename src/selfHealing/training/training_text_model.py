from pathlib import Path

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from xgboost import XGBClassifier

CURRENT_DIR = Path(__file__).resolve().parent
HEALING_FOLDER = CURRENT_DIR.parent

class TextHealingTrainer:
    CURRENT_DIR = Path(__file__).resolve().parent
    healingFolder = CURRENT_DIR.parent
    def __init__(self):

        self.features = [

            "id_similarity",
            "text_similarity",
            "class_similarity",
            "tag_match"

        ]


    def train(self, dataset_path):

        df = pd.read_csv(dataset_path)

        # ONLY text locator rows
        df = df[
            df["locator_type"] == "text"
        ]

        X = df[self.features]

        y = df["is_correct"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        model = XGBClassifier(

            n_estimators=200,
            max_depth=5,
            learning_rate=0.05,
            objective="binary:logistic",
            eval_metric="logloss",

            scale_pos_weight=3
        )

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        print(
            classification_report(
                y_test,
                predictions
            )
        )

        model_save_path = HEALING_FOLDER / "models" / "text_healing_model.pkl"

        # Ensure the 'models' directory exists before saving
        model_save_path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(model, str(model_save_path))
        print(f"\nID Healing model saved to: {model_save_path}")


if __name__ == "__main__":

    trainer = TextHealingTrainer()
    target_dataset = HEALING_FOLDER / "datasets" / "clean_dataset.csv"
    trainer.train(target_dataset)