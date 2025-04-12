# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 15:46:22 2025

@author: sally
"""
import requests
import os, re
import pandas as pd
from utils import *



def fetch_company_data_from_apis():
    """
    Fetches and returns company data from System A and System B APIs.
    
    Returns:
        df_system_a (DataFrame): Company data from System A
        ori_system_a (list): System A data as list of lists
        df_system_b (DataFrame): Company data from System B
        ori_system_b (list): System B data as list of lists
    """
    # Make GET requests to both API endpoints
    system_a_response = requests.get("http://localhost:5000/system-a/companies")
    system_b_response = requests.get("http://localhost:5000/system-b/companies")
    
    # Check if both responses are successful
    if all(resp.status_code == 200 for resp in [system_a_response, system_b_response]):
        
        # Convert System A and B responses to DataFrames and lists
        df_system_a = pd.DataFrame(system_a_response.json())
        ori_system_a = df_system_a.values.tolist()
        
        df_system_b = pd.DataFrame(system_b_response.json())
        ori_system_b = df_system_b.values.tolist()
        return df_system_a, ori_system_a, df_system_b, ori_system_b
    
    else:
        # Print failure messages if any API fails
        if system_a_response.status_code != 200:
            print("System A FAIL:", system_a_response.status_code)
        if system_b_response.status_code != 200:
            print("System B FAIL:", system_b_response.status_code)        
        return None, None, None, None
    
    
def load_excel_reference(filename="excel.xlsx", folder="Sources"):
    """
    Loads and cleans the Excel reference file.

    Args:
        filename (str): Name of the Excel file.
        folder (str): Folder where the Excel file is stored.

    Returns:
        df_excel (DataFrame): Cleaned DataFrame with standardized column names.
        ori_excel (list): Original data as list of lists.
    """
    source_dir = os.path.join(os.getcwd(), folder)
    excel_file_path = os.path.join(source_dir, filename)
    df_excel = pd.read_excel(excel_file_path, engine='openpyxl')
    ori_excel = df_excel.values.tolist()
    return df_excel, ori_excel


def perform_canonical_matching(df_system_a, ori_system_a, df_system_b, ori_system_b, df_excel, ori_excel):
    """
    Standardizes company names from three sources and maps them by similarity.

    Args:
        df_system_a (DataFrame): DataFrame from System A
        ori_system_a (list): Original list of System A values
        df_system_b (DataFrame): DataFrame from System B
        ori_system_b (list): Original list of System B values
        df_excel (DataFrame): DataFrame from Excel
        ori_excel (list): Original list of Excel values

    Returns:
        df_mapped (DataFrame): Mapped results with canonical names and matched records from each source
    """

    # Create output lists to store canonical names for each source
    system_a, system_b, excel = [], [], []

    # Map each label to the corresponding list
    output_lists = {
        "System A": system_a,
        "System B": system_b,
        "Excel": excel
    }

    # Canonicalize names and populate output lists
    for label, df in [("System A", df_system_a), ("System B", df_system_b), ("Excel", df_excel)]:
        for name in df['company_name']:
            canonical_name = canonicalize_company_name(name)
            output_lists[label].append(canonical_name)

    # Perform 3-way matching using canonical names
    myresult = map_three_sources(output_lists["System A"], output_lists["System B"], output_lists["Excel"])
    
    # Format the matched result into structured records
    records = []
    for key, indices in myresult.items():
        row = {
            "canonical_name": key,
            "system_a": ori_system_a[indices['a_index']][0],
            "system_b": ori_system_b[indices['b_index']][0],
            "excel": ori_excel[indices['e_index']][0]
        }
        records.append(row)

    # Convert result into DataFrame and export to Excel
    df_mapped = pd.DataFrame(records)
    return df_mapped


if __name__ == "__main__":    
    df_system_a, ori_system_a, df_system_b, ori_system_b = fetch_company_data_from_apis()
    df_excel, ori_excel = load_excel_reference()
    df_mapped = perform_canonical_matching(df_system_a, ori_system_a, df_system_b, ori_system_b, df_excel, ori_excel)
    df_mapped.to_excel("output.xlsx", index=False)
