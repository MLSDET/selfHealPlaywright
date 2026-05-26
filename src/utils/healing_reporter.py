import allure


class HealingReporter:


    @staticmethod
    def healing_step_title(

            failed_locator,
            healed_locator
     ):

        return f"""

        🟠 SELF-HEALED

        Original:
        {failed_locator}

        Recovered:
        {healed_locator}

        """


    @staticmethod
    def attach_healing_metadata(

            failed_locator,
            healed_locator
            # confidence_score

    ):

        html = f"""

        <div style='
            background-color:#fff3cd;
            border-left:8px solid orange;
            padding:15px;
            border-radius:8px;
            font-size:14px;
        '>

        <h3 style='color:#ff9800;'>
            Self-Healing Details
        </h3>

        <p>
            <b>Original Locator:</b>
            {failed_locator}
        </p>

        <p>
            <b>Recovered Locator:</b>
            {healed_locator}
        </p>
        </div>
        """

        allure.attach(

            html,

            name="Healing Details",

            attachment_type=allure.attachment_type.HTML
        )