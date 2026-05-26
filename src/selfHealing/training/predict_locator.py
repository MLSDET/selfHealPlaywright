from pathlib import Path

import pandas as pd
import joblib

CURRENT_DIR = Path(__file__).resolve().parent
HEALING_FOLDER = CURRENT_DIR.parent

class LocatorPredictor:

    def __init__(self):
        model_path = HEALING_FOLDER / "models" / "id_healing_model.pkl"
        self.id_model = joblib.load(model_path)

        # self.text_model = joblib.load(
        #     "models/text_healing_model.pkl"
        # )

        self.features = [

            "id_similarity",
            "text_similarity",
            "class_similarity",
            "tag_match"
        ]


    def predict_best_candidate(

            self,
            locator_type,
            candidate_df

    ):

        X = candidate_df[self.features]

        if locator_type == "id":

            probabilities = self.id_model.predict_proba(X)

        # else:
        #
        #     probabilities = self.text_model.predict_proba(X)

        candidate_df["prediction_score"] = probabilities[:,1]

        candidate_df = candidate_df.sort_values(

            by="prediction_score",
            ascending=False
        )

        print("\nTop Candidates:\n")

        print(
            candidate_df[
                [
                    "selector",
                    "prediction_score",
                    "id_similarity",
                    "text_similarity"
                ]
            ].head(10)
        )

        return candidate_df.iloc[0]