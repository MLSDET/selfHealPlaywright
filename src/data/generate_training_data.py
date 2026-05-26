from playwright.sync_api import sync_playwright
from difflib import SequenceMatcher
import pandas as pd
import random


def similarity(a, b):
    return SequenceMatcher(
        None,
        str(a).lower(),
        str(b).lower()
    ).ratio()


def safe_string(value):
    return value.strip() if value else ""


def extract_element_data(element):

    try:

        text = safe_string(
            element.inner_text()
        )

        element_id = safe_string(
            element.get_attribute("id")
        )

        class_name = safe_string(
            element.get_attribute("class")
        )

        tag = element.evaluate(
            "el => el.tagName.toLowerCase()"
        )

        return {
            "text": text,
            "id": element_id,
            "class": class_name,
            "tag": tag
        }

    except Exception:
        return None


def generate_features(
        failed_locator,
        candidate,
        label
):

    return {

        "failed_locator":
            failed_locator,

        "candidate_text":
            candidate["text"],

        "candidate_id":
            candidate["id"],

        "candidate_class":
            candidate["class"],

        "candidate_tag":
            candidate["tag"],

        "text_similarity":
            similarity(
                failed_locator,
                candidate["text"]
            ),

        "id_similarity":
            similarity(
                failed_locator,
                candidate["id"]
            ),

        "class_similarity":
            similarity(
                failed_locator,
                candidate["class"]
            ),

        "tag_match":
            int(
                candidate["tag"]
                in failed_locator.lower()
            ),

        "label":
            label
    }


def build_dataset():

    rows = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        page.goto(
            "https://www.saucedemo.com"
        )

        # Simulated failed locator
        failed_locator = "Add to cart"

        elements = page.query_selector_all("*")

        extracted = []

        for el in elements:

            data = extract_element_data(el)

            if data:
                extracted.append(data)

        # Positive example
        for item in extracted:

            if (
                item["text"]
                == "Add to cart"
            ):

                rows.append(
                    generate_features(
                        failed_locator,
                        item,
                        label=1
                    )
                )

        # Negative examples
        negatives = random.sample(
            extracted,
            min(
                30,
                len(extracted)
            )
        )

        for item in negatives:

            if (
                item["text"]
                != "Add to cart"
            ):

                rows.append(
                    generate_features(
                        failed_locator,
                        item,
                        label=0
                    )
                )

        browser.close()

    df = pd.DataFrame(rows)

    df.to_csv(
        "./src/data/training_data.csv",
        index=False
    )

    print(
        f"Generated {len(df)} rows"
    )


if __name__ == "__main__":
    build_dataset()