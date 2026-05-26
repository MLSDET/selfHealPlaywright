# Python + Playwright + ML Self-Healing UI Testing Framework

## Overview

This project demonstrates an AI/ML-driven self-healing UI automation framework built using Python and Playwright. The framework is designed to automatically recover from UI locator failures caused by changes in attributes, DOM structure, labels, or layout updates.

The solution combines:

* **Playwright** for UI automation
* **Python** for automation framework development
* **Machine Learning** for intelligent locator recovery

The framework improves test stability and reduces maintenance effort in rapidly changing UI applications.

---

# Key Features

* Cross-browser UI automation using Playwright
* ML-based self-healing locator strategy
* Automatic fallback locator prediction
* Failed locator pattern analysis
* Dynamic locator similarity matching
---

# Architecture

```text
                 +---------------------+
                 |  Playwright Tests   |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | Locator Failure?    |
                 +----------+----------+
                            |
                  Yes       |
                            v
                 +---------------------+
                 | Self-Healing Engine |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | ML Prediction API   |
                 | SageMaker Endpoint  |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | Predicted Locator   |
                 +----------+----------+
                            |
                            v
                 +---------------------+
                 | Retry Automation    |
                 +---------------------+
```

---

# Tech Stack

| Component            | Technology                    |
| -------------------- | ----------------------------- |
| Programming Language | Python 3.11+                  |
| UI Automation        | Playwright                    |
| ML Framework         | Scikit-learn / XGBoost        |
| Cloud Platform       | AWS                           |
| ML Training          | SageMaker                     |
| Storage              | Amazon S3                     |
| Deployment           | SageMaker Serverless Endpoint |
| Reporting            | Allure Reports                |
| CI/CD                | Jenkins / GitHub Actions      |
| API Framework        | FastAPI / Flask               |


---

# Self-Healing Workflow

## Step 1: Execute UI Test

Playwright executes the UI automation flow using primary locators.

## Step 2: Detect Locator Failure

If a locator fails due to DOM changes:

* ID changes

The framework triggers the healing engine.

## Step 3: Extract DOM Features

The framework extracts:

* Tag name
* Class attributes
* Text values
* Neighbor elements
* XPath hierarchy
* Position information
* DOM similarity patterns

## Step 4: ML Prediction

The extracted features are sent to the deployed ML endpoint.

The model predicts:

* Best matching locator
* Similarity score
* Confidence score

## Step 5: Retry Execution

The framework retries the action using the healed locator.

## Step 6: Logging & Reporting

The healed locator and prediction confidence are stored for future retraining.

---

# Machine Learning Approach

## Problem Statement

UI locators frequently break when application UI changes occur. Manual maintenance becomes expensive in large-scale automation suites.

## ML Goal

Predict the most probable replacement locator using historical DOM and locator metadata.

---

# Input Features

Typical ML features include:

| Feature              | Description              |
| -------------------- | ------------------------ |
| Original Locator     | Failed XPath/CSS         |
| Tag Name             | HTML tag                 |
| Element Text         | Visible text             |
| Class Name           | CSS classes              |
| Attribute Similarity | Attribute matching score |
| DOM Position         | Relative hierarchy       |
| Neighbor Elements    | Contextual elements      |
| XPath Similarity     | Structural similarity    |

---

# ML Algorithms

Possible algorithms:

* Random Forest
* XGBoost
* Gradient Boosting
* Siamese Neural Networks
* NLP Embedding Similarity Models
* Transformer-based DOM similarity models

---

# Model Training Flow

## Dataset Preparation

Historical locator failures are collected and transformed into structured training datasets.

Example:

| Failed Locator         | New Locator               | Similarity Features |
| ---------------------- | ------------------------- | ------------------- |
| //button[@id='submit'] | //button[@id='submitBtn'] | vector              |

---

## Training Pipeline

1. Load dataset
2. Clean and preprocess features
3. Feature engineering
4. Train ML model
5. Evaluate accuracy

---
##To Run the Tests
To activate the local Python Environment

source .venv/bin/activate 

Run Tests:

pytest tests/ --alluredir=reports/allure-results

To Generate Report:

allure generate reports/allure-results -o reports/allure-report --clean

allure serve reports/allure-results  

Sample report with healing

https://github.com/MLSDET/selfHealPlaywright/blob/main/Report_ScreenShot_With_Healing.png

Sample locator candidate prediction

https://github.com/MLSDET/selfHealPlaywright/blob/main/predicted_locator_candidate_ranking.png


# Author
Ramya Shetty


