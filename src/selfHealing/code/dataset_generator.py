from pathlib import Path

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
import pandas as pd
import os
import random

CURRENT_DIR = Path(__file__).resolve().parent
HEALING_FOLDER = CURRENT_DIR.parent

class CleanDatasetBuilder:

    def __init__(self):

        self.records = []

    def similarity(self, a, b):

        a = str(a or "")
        b = str(b or "")

        return round(
            fuzz.partial_ratio(
                a.lower(),
                b.lower()
            ) / 100,
            2
        )

    def generate_broken_id(self, element_id):

        if not element_id:
            return None

        return f"{element_id}1234"

    def generate_broken_text(self, text):

        if not text:
            return None

        return f"{text}123"

    def extract_elements(self, soup):

        interactable_tags = [
            "button",
            "input",
            "a"
        ]

        elements = []

        for tag in interactable_tags:

            for element in soup.find_all(tag):

                text = element.get_text(strip=True)

                if len(text) > 40:
                    continue

                element_data = {

                    "id": element.get("id", ""),
                    "text": text,
                    "tag": tag,
                    "class": " ".join(
                        element.get("class", [])
                    )
                }

                elements.append(element_data)

        return elements

    def build_samples(self, elements):

        for element in elements:

            element_id = element["id"]
            text = element["text"]
            tag = element["tag"]
            classes = element["class"]

            # -----------------------------
            # ID BASED TRAINING
            # -----------------------------

            if element_id:
                failed_locator = (
                    f"#{self.generate_broken_id(element_id)}"
                )

                positive_selector = f"#{element_id}"

                self.records.append({

                    "locator_type": "id",
                    "failed_locator": failed_locator,
                    "candidate_selector": positive_selector,
                    "candidate_id": element_id,
                    "candidate_text": text,
                    "candidate_tag": tag,

                    "id_similarity": self.similarity(
                        failed_locator,
                        element_id
                    ),

                    "text_similarity": self.similarity(
                        failed_locator,
                        text
                    ),

                    "class_similarity": self.similarity(
                        failed_locator,
                        classes
                    ),

                    "tag_match": 1,

                    "is_correct": 1
                })
                # Hard negatives
                negatives = random.sample(
                    elements,
                    min(5, len(elements))
                )

                for negative in negatives:

                    if negative["id"] == element_id:
                        continue

                    self.records.append({

                        "locator_type": "id",
                        "failed_locator": failed_locator,

                        "candidate_selector": (
                            f"#{negative['id']}"
                            if negative["id"]
                            else f'text="{negative["text"]}"'
                        ),

                        "candidate_id": negative["id"],
                        "candidate_text": negative["text"],
                        "candidate_tag": negative["tag"],

                        "id_similarity": self.similarity(
                            failed_locator,
                            negative["id"]
                        ),

                        "text_similarity": self.similarity(
                            failed_locator,
                            negative["text"]
                        ),

                        "class_similarity": self.similarity(
                            failed_locator,
                            negative["class"]
                        ),

                        "tag_match": 1 if tag == negative["tag"] else 0,

                        "is_correct": 0
                    })
            # -----------------------------
            # TEXT BASED TRAINING
            # -----------------------------

            if text:
                failed_text = self.generate_broken_text(text)

                failed_locator = f'text={failed_text}'

                positive_selector = f'text="{text}"'

                self.records.append({

                    "locator_type": "text",
                    "failed_locator": failed_locator,
                    "candidate_selector": positive_selector,
                    "candidate_id": element_id,
                    "candidate_text": text,
                    "candidate_tag": tag,

                    "id_similarity": self.similarity(
                        failed_locator,
                        element_id
                    ),

                    "text_similarity": self.similarity(
                        failed_locator,
                        text
                    ),

                    "class_similarity": self.similarity(
                        failed_locator,
                        classes
                    ),

                    "tag_match": 1,

                    "is_correct": 1
                })

    def build_dataset(self, path):

        with open(
                path,
                encoding="utf-8"
        ) as f:
            html = f.read()

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        elements = self.extract_elements(soup)

        self.build_samples(elements)

        df = pd.DataFrame(self.records)

        df = df.sample(frac=1).reset_index(drop=True)

        print(df.head())

        print("\nDataset Shape:")
        print(df.shape)

        print("\nClass Distribution:")
        print(df["is_correct"].value_counts())

        # # 1. Get the absolute path of the current script (dom_capture.py)
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        #
        # # 2. Go one levels up to reach the 'selfHealing' directory
        # self_healing_dir = os.path.abspath(os.path.join(script_dir, ".."))
        #
        # # 3. Target the 'pages_html' directory inside 'selfHealing'
        # output_dir = os.path.join(self_healing_dir, "datasets")
        #
        # # 4. Create the 'pages_html' folder if it doesn't exist yet
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)
        # pageName = "clean_dataset"
        # # 5. Combine directory and filename
        # file_path = os.path.join(output_dir, f"{pageName}.csv")
        dataSetPath = HEALING_FOLDER / "datasets" / "clean_dataset.csv"

        # Ensure the 'models' directory exists before saving
        dataSetPath.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(dataSetPath, index=False)

        print(df.head())

        print("\nClean dataset generated")


if __name__ == "__main__":
    builder = CleanDatasetBuilder()
    htmlFilePath = HEALING_FOLDER / "pages_html" / "InventoryPage.html"
    builder.build_dataset(htmlFilePath)
