# Data Engineering - Data Quality Exercise

## Objective:
Learn to perform data profiling and quality checks on a dataset using a data platform. This exercise will guide you through the process of profiling a table and creating data quality checks.

### Prerequisites:
- Go to Dataplex (https://console.cloud.google.com/dataplex)
- Go to Search, select BigQuery in Systems
- Search and choose: `salesorderheader`
- The tabs for Data Profile and Data Quality are empty

### Exercise Steps:

#### Part 1: Data Profiling

**Action:** Profile the `salesorderheader` table.

1. Go to the "Profile" tab.
2. Click on "Create Data Profile Scan".
3. Name the scan (e.g., `dp-2023-transactions-profile`).
4. Select the `salesorderheader` table.
5. Click "Continue".
6. Choose the "adventureworks" dataset.
7.  For the output, enter `profile-salesorderheader` as the table name.
8.  Initiate the scan and wait for it to complete (this may take a few minutes).
9.  Review the data profile results.

#### Part 2: Data Quality Check

**Goal:** Establish data quality checks for the `salesorderheader` table.

1. Go to the "Data Quality" tab.
2. Click on "Create Data Quality Scan".
3. Name the scan (e.g., `dp-2023-salesorderheader-quality`).
4. Again, select the `salesorderheader` table.
5. Click "Continue".
6. Add rules by choosing "Built-in rule types".
   - For NULL checks, apply the rule to critical columns such as `billtoaddressid`, `customerid`, and `orderdate`.
   - For format checks, use a Regex check on the `totaldue` column to ensure it contains only numeric values (use the regex pattern `^\d+(\.\d+)?$`).
7. Continue to the next step and select the "adventureworks" dataset.
8. For the output, enter `salesorderheader` as the table name.
9. Start the scan and wait for it to complete.
10. Once finished, review the data quality results.

#### Part 3: Verification

1. Return to the search bar and type "transactions" to open the table again.
2. Examine the "Data Profile" and "Data Quality" tabs to see the updated information.
3. In the data platform, locate and review the `profile-salesorderheader` and `check-salesorderheader` tables to understand the profiling and quality check results.

### Conclusion:
By completing this exercise, you will gain practical experience in performing essential data quality and profiling tasks, which are critical for ensuring the reliability of data in any data-driven decision-making process.
