# Sally_Company_Name_Standardize

Company Name Standardization Case Study

Overview:
This project solves the problem of inconsistent company naming across:
- System A (CRM, via API)
- System B (Finance, via API)
- Excel (manual input from sales/admin team)

The goal is to clean, match, and standardize names into a single output file for accurate analytics and reporting.

Project Files:
- standardize_names.py: Main script to clean and match names
- system_a_b_API_Host.py: Flask app that simulates API responses
- utils.py: Contains logic for canonicalization and fuzzy matching
- Sources/
    - system_a.json: Company names from System A
    - system_b.json: Company names from System B
    - excel.xlsx: Excel file used internally
- output.xlsx: Final result after standardization

How to Run:
1. Install the dependencies:
   pip install pandas flask openpyxl thefuzz

2. Start the API server:
   python system_a_b_API_Host.py

3. Run the matching script:
   python standardize_names.py

4. View the results in output.xlsx

Logic Summary:
- Canonicalization: removes suffixes like "Ltd", strips punctuation and spaces, makes everything uppercase.
- Matching:
    - Exact match
    - Substring match
    - Fuzzy match (if no exact/substring match found)

Scalability:
- Easy to add to Airflow or other ETL tools
- Canonical names can be reused as unique keys
- New names are automatically matched or flagged

Output Example:
----------------|----------------------|--------------------|----------------
0           ACME|          ACME Pte Ltd|        ACME Limited|   Acme Inc.
1        GLOBALX|  Global-X Corporation|      Global X Corp.|    Global X
2      ALPHATECH|   Alpha Tech Holdings|  Alpha Technologies|  ALPHA TECH

Author: Sally Soo (2025)