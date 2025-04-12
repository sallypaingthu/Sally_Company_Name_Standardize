# -*- coding: utf-8 -*-
"""
Created on Sat Apr 12 21:29:35 2025

@author: sally
"""
import re
from thefuzz import fuzz
def canonicalize_company_name(name):
    """
    Standardizes a company name by removing common business suffixes, punctuation, and whitespace.

    The function:
    - Converts the name to lowercase
    - Removes common suffixes (e.g., "Pte Ltd", "Inc", "Corp")
    - Strips all non-alphanumeric characters
    - Removes all spaces
    - Returns the result in uppercase

    Args:
        name (str): The original company name to be canonicalized.

    Returns:
        str: The cleaned, uppercase version of the company name.
    """
    name = name.lower()
    suffixes = [
        "private limited", "pte ltd", "pte. ltd.", "sdn bhd", 
        "corporation", "limited", "corp", "co", "inc", 
        "llc", "ltd", "plc"
        ]
    for suffix in suffixes:
        pattern = r"\b" + re.escape(suffix) + r"\b"
        name = re.sub(pattern, '', name)
        
    name = re.sub(r"[^\w\s]", '', name)
    name = re.sub(r"\s+", "", name)
    return name.upper()


def find_best_match(target, collection, threshold=85):
    """
    Finds the best match for a target name in a collection of strings.

    First checks for an exact match. If not found, tries substring matching.
    Returns the first match found or None.

    Args:
        target (str): The name to search for.
        collection (list of str): The set of values to search within.

    Returns:
        str or None: The best matching string, or None if no match is found.
    """
    if target in collection:
        return target
    
    for item in collection:
        if target in item:
            return item
        
    best_score = 0
    best_match = None
    for item in collection:
        score = fuzz.token_sort_ratio(target, item)
        if score >= threshold and score > best_score:
            best_score = score
            best_match = item
        return best_match


def map_three_sources(system_a, system_b, excel):
    
    """
    Matches company names across three lists (system_a, system_b, and excel).
    
    First checks for exact matches. Then performs three-way substring matching:
    - A to B & E
    - B to A & E
    - E to A & B

    Returns:
        dict: A mapping dictionary where each key is a matched canonical name,
              and values are a_index, b_index, and e_index from the respective lists.
    """
    tmp_a = system_a.copy()
    tmp_b = system_b.copy()
    tmp_e = excel.copy()
    mapped_sources = {}

    for index,item in enumerate(system_a):  
        if item in system_b and item in excel:
            mapped_sources[item] = {
                "a_index": index,
                "b_index": system_b.index(item),
                "e_index": excel.index(item)
            }
            tmp_a.remove(item)
            tmp_b.remove(item)
            tmp_e.remove(item)
            tmp_a.sort(key=len, reverse=True)
            tmp_b.sort(key=len, reverse=True)
            tmp_e.sort(key=len, reverse=True)
    
    # 3 way merge
    to_remove_a = []
    to_remove_b = []
    to_remove_e = []
    # A to BE
    for index_a,item_a in enumerate(tmp_a):
        match_tmp_b = find_best_match(item_a,tmp_b)
        match_tmp_e = find_best_match(item_a, tmp_e)  
        if match_tmp_b != None and match_tmp_e != None:
            mapped_sources[item_a] = {}
            mapped_sources[item_a]["a_index"] = system_a.index(item_a)
            mapped_sources[item_a]["b_index"] = system_b.index(match_tmp_b)
            mapped_sources[item_a]["e_index"] = excel.index(match_tmp_e)
            to_remove_a.append(item_a)
            to_remove_b.append(match_tmp_b)
            to_remove_e.append(match_tmp_e)
    for item in to_remove_a:
        tmp_a.remove(item)
    for item in to_remove_b:
        tmp_b.remove(item)
    for item in to_remove_e:
        tmp_e.remove(item)

    # B to AE
    to_remove_a = []
    to_remove_b = []
    to_remove_e = []
    for index_b,item_b in enumerate(tmp_b):
        match_tmp_a = find_best_match(item_b,tmp_a)
        match_tmp_e = find_best_match(item_b, tmp_e)    
        if match_tmp_a != None and match_tmp_e != None:
            mapped_sources[item_b] = {}
            mapped_sources[item_b]["a_index"] = system_a.index(match_tmp_a)
            mapped_sources[item_b]["b_index"] = system_b.index(item_b)
            mapped_sources[item_b]["e_index"] = excel.index(match_tmp_e)
            mapped_sources[item] = {
                "a_index": system_a.index(match_tmp_a),
                "b_index": system_b.index(item_b),
                "e_index": excel.index(match_tmp_e)
            }
            
            to_remove_a.append(match_tmp_a)
            to_remove_b.append(item_b)
            to_remove_e.append(match_tmp_e)
    for item in to_remove_a:
        tmp_a.remove(item)
    for item in to_remove_b:
        tmp_b.remove(item)
    for item in to_remove_e:
        tmp_e.remove(item)
        
    # E to AB
    to_remove_a = []
    to_remove_b = []
    to_remove_e = []
    for index_e,item_e in enumerate(tmp_e):
        match_tmp_a = find_best_match(item_e,tmp_a)
        match_tmp_b = find_best_match(item_e, tmp_b)    
        if match_tmp_a != None and match_tmp_b != None:
            mapped_sources[item_e] = {}
            mapped_sources[item_e]["a_index"] = system_a.index(match_tmp_a)
            mapped_sources[item_e]["b_index"] = system_b.index(match_tmp_b)
            mapped_sources[item_e]["e_index"] = excel.index(item_e)
            to_remove_a.append(match_tmp_a)
            to_remove_b.append(match_tmp_b)
            to_remove_e.append(item_e)
    for item in to_remove_a:
        tmp_a.remove(item)
    for item in to_remove_b:
        tmp_b.remove(item)
    for item in to_remove_e:
        tmp_e.remove(item)
        
    return mapped_sources