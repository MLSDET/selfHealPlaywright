import allure
from bs4 import BeautifulSoup
import pandas as pd

from rapidfuzz import fuzz

from src.selfHealing.training.predict_locator import (
    LocatorPredictor
)

from src.utils.healing_reporter import (
    HealingReporter
)


class SelfHealingEngine:

    def __init__(self):

        self.predictor = LocatorPredictor()


    def similarity(self, a, b):

        return round(

            fuzz.partial_ratio(

                str(a).lower(),
                str(b).lower()

            ) / 100,

            2
        )


    def find_new_locator(

            self,
            page,
            failed_locator

    ):

        locator_type = "text"

        if failed_locator.startswith("#"):

            locator_type = "id"


        failed_locator_clean = (

            failed_locator

            .replace("#", "")
            .replace("text=", "")
            .replace('"', "")

            .strip()
        )

        dom = page.content()

        soup = BeautifulSoup(
            dom,
            "html.parser"
        )

        interactable_tags = [

            "button",
            "input",
            "a"
        ]

        elements = soup.find_all(
            interactable_tags
        )

        candidate_rows = []

        for element in elements:

            text = element.get_text(
                strip=True
            )

            if len(text) > 40:

                continue

            element_id = element.get(
                "id",
                ""
            )

            tag = element.name

            classes = " ".join(
                element.get(
                    "class",
                    []
                )
            )

            selector = None

            if element_id:

                selector = f"#{element_id}"

            elif text:

                selector = f'text="{text}"'

            else:

                continue


            row = {

                "selector": selector,

                "id_similarity":
                    self.similarity(
                        failed_locator_clean,
                        element_id
                    ),

                "text_similarity":
                    self.similarity(
                        failed_locator_clean,
                        text
                    ),

                "class_similarity":
                    self.similarity(
                        failed_locator_clean,
                        classes
                    ),

                "tag_match":
                    1 if tag == "button"
                    else 0
            }

            candidate_rows.append(row)

        candidate_df = pd.DataFrame(
            candidate_rows
        )

        best_match = (

            self.predictor
            .predict_best_candidate(

                locator_type,
                candidate_df
            )
        )

        return best_match["selector"]


    # ----------------------------------
    # Reusable self-healing wrapper
    # ----------------------------------

    def safe_click(

            self,
            page,
            locator

    ):

        try:

            with allure.step(

                    f"Click locator: {locator}"

            ):

                page.click(locator)

        except Exception:

            print(f"\nLocator failed: {locator}\n")

            healed_locator = self.find_new_locator(
                page,
                locator
            )

            with allure.step(

                    HealingReporter.healing_step_title(

                        locator,
                        healed_locator
                    )
            ):

                HealingReporter.attach_healing_metadata(

                    locator,
                    healed_locator
                )

                page.click(healed_locator)