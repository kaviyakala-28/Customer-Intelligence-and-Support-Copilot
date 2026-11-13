# Capstone Project

# Customer Intelligence and Support Copilot

## Overview

This project is based on Instamart's customer, order and support ticket data. The main aim is to understand customer behaviour, identify customers who may stop ordering, and make support ticket handling easier.

I worked on this project in four parts:

- **Part A – Data Foundation:** Understanding the raw data, cleaning it, storing it in SQLite and answering business questions using SQL and pandas.
- **Part B – Customer Segments and Lapse Prediction:** Creating customer segments using RFM and K-means, and building models to identify customers who may lapse.
- **Part C – Support Ticket Triage:** Preparing support tickets for classification, protecting personal information, handling model responses and routing tickets.
- **Part D – Policy RAG Assistant and Refund Agent:** Building a policy-based assistant and an agent that checks refund requests using the available order and policy information.

The project uses synthetic data supplied with the capstone. The supplied `generate_data.py` and `mock_llm.py` files are used without modification.

## Reproduce

Follow these steps from the project root folder.

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

2. Activate the environment on Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Install the required libraries:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Generate the raw data:

   ```bash
   python generate_data.py
   ```

5. Run the data validation script:

   ```bash
   python validate_data.py
   ```

6. Open the Part A+B notebook in VS Code and run the cells in order.

7. Open the Part C+D notebook and run the cells in order.

The notebooks should be run in sequence because later parts use files created by earlier parts.

## Part A – Data Foundation

In this part, I worked with the raw customer, product and order data. I first checked the data for missing values, duplicate records, incorrect values and inconsistent entries.

I then cleaned the customer and order data using the rules given in the capstone. The cleaned tables were stored as CSV files and loaded into a SQLite database.

I also wrote SQL queries to answer business questions and checked selected results again using pandas.

**Main work completed:**

- Audited the raw customer, product and order tables.
- Standardised customer city and gender values.
- Handled missing and invalid customer ages.
- Cleaned order dates, duplicate records, amounts and delivery information.
- Stored the cleaned data in SQLite.
- Created SQL queries using joins, subqueries, CTEs and window functions.
- Compared selected SQL results with pandas results.

**Key results:**

- Raw order rows: [Add actual result]
- Duplicate order rows: [Add actual result]
- Clean customer rows: [Add actual result]
- Clean order rows: [Add actual result]
- SQLite database: `data/instamart.db`
- SQL query file: `sql/queries.sql`

## Part B – Customer Segments and Lapse Prediction

In this part, I used the cleaned customer and order data to understand customer purchasing behaviour.

I created an RFM table using recency, frequency and monetary value. I compared different K values using inertia and silhouette scores and selected K = 4 for customer segmentation.

The segments were given business names based on their purchasing behaviour. The segment with the highest average monetary value was marked as Premium.

I also created a lapse prediction dataset using the September 2025 cutoff. Logistic Regression and Random Forest were trained and compared. I performed a class-balance experiment on the training data and checked the results on the original test set.

**Key results:**

- Customers in the RFM table: 1,175
- Selected number of clusters: 4
- Lapse prediction cohort: 1,156 customers
- Lapsed customers: 443
- Training rows: 924
- Test rows: 232
- Baseline accuracy: 61.6%
- Selected model: [Add selected model]
- Selected model test F1-score: [Add actual result]
- Customers who actually lapsed in the retention list: 1

**Files created:**

- `outputs/customer_segments.csv`
- `outputs/lapse_model.joblib`
- `outputs/retention_list.csv`

The preprocessing steps were fitted using training data only. No encoder, scaler or resampler was fitted on test rows. The lapse prediction features used only information available before 1 September 2025, and the segment labels from Task 3 were not used as model features.

## Part C – Support Ticket Triage

[Complete this section after Part C tasks are finished.]

This part uses the support ticket data and the supplied `mock_llm.py` file. The pipeline includes input checks, personal information redaction, zero-shot and few-shot prompts, retry handling, output validation and token-budget-based routing.

**Key results:**

- Total support tickets: 164
- Empty tickets skipped: 4
- Long tickets flagged: 4
- Eligible tickets: 156
- Email substitutions: [Add result]
- Phone substitutions: [Add result]
- Order ID substitutions: [Add result]
- Zero-shot accuracy: [Add result]
- Few-shot accuracy: [Add result]
- Tickets requiring human review: [Add result]
- Token budget used for the demonstration: [Add result]

**Files created:**

- `outputs/triage_results.csv`
- `outputs/triage_budget_demo.csv`

## Part D – Policy RAG Assistant and Refund Agent

[Complete this section after Part D tasks are finished.]

In this part, I worked with the policy documents provided in the project. The policy assistant retrieves relevant information from these documents before preparing an answer.

The refund agent uses order information and policy details to decide whether a request can be processed, should be denied or needs human review.

**Key results:**

- Number of policy documents: 5
- Seven scenario results: [Add the scenario results table]
- Token-limit demonstration status: [Add result]
- Timeout demonstration status: [Add result]
- Crash-and-resume result: [Add result]
- Tools executed during the resumed run: [Add actual order]

**Files created:**

- `outputs/agent_runs.jsonl`
- `outputs/refund_ledger.jsonl`
- `state/` – checkpoint files used for resuming an interrupted run.

Limitations and Next Steps

This project uses synthetic data, so the results may not fully reflect how customers behave in a real business environment.

The lapse model uses the available historical data and selected customer features to identify customers who may be likely to lapse. Its predictions are only an indication and should not be treated as a guarantee.

The Premium flag is created using the whole-period RFM data, including September, which is also used to define the lapse label. Because of this, the retention list is illustrative and should not be considered a leakage-free evaluation.

The support ticket classification and policy assistant use the supplied mock LLM instead of a live language model. Therefore, their results depend on the behaviour of the provided mock LLM.