__all__ = ['oxford_comma_join', 'generate_gist_string', 'generate_caption_parties_block', 'update_documents_drafted', 'get_document_titles', 'update_past_lm_proceedings', 'get_past_lm_proceedings']

import inflect
import re
from datetime import datetime
from docassemble.base.functions import fix_punctuation, showifdef

import re

def oxford_comma_join(elements):
    """
    Join a list of elements into a string with proper comma and 'and' placement.
    If a string is passed, it will be split into a list by commas or semicolons.

    Parameters:
        elements (list or str): List of elements or a string containing elements separated by comma or semicolon.

    Returns:
        str: String of elements joined with proper comma and 'and' placement.
    """

    # Convert string to list if necessary
    if isinstance(elements, str):
        elements = [item.strip() for item in re.split(',|;|\n', elements)]

    if len(elements) == 1:
        return elements[0]
    elif len(elements) == 2:
        return f"{elements[0]} and {elements[1]}"
    else:
        return f"{', '.join(elements[:-1])}, and {elements[-1]}"

def format_causes_list(causes_list, num_causes):
    """
    Format the list of causes of action based on the number of causes.

    Parameters:
        causes_list (list): List of causes of action.
        num_causes (int): Number of causes of action.

    Returns:
        str: Formatted string of causes of action.
    """
    if num_causes == 1:
        return causes_list[0]
    elif num_causes == 2:
        return ', and '.join(causes_list)
    elif num_causes == 3:
        return f'{causes_list[0]}, {causes_list[1]}, and {causes_list[2]}'
    else:
        return ', '.join(f'({i + 1}) {cause}' for i, cause in enumerate(causes_list))

def generate_gist_string(case):
    """
    Generate a gist string that summarizes a legal case.

    Parameters:
        case (object): An object with attributes detailing the case.

    Returns:
        str: A string summarizing the case.
    """
    # Check for missing or None attributes
    if not all(getattr(case, attr, None) for attr in ["type", "causes_of_action", "initiating_pleading_type", "filing_date", "relief_sought"]):
        return "Insufficient case data."
    
    p = inflect.engine()
    
    # Splitting causes_of_action into a list and calculating the number of causes
    causes_list = [item.strip() for item in re.split(',|;', case.causes_of_action)]
    num_causes = len(causes_list)
    num_causes_str = p.number_to_words(num_causes)
    
    # Ensuring correct grammar for pluralization
    cause_noun = p.plural("cause of action", num_causes)
    
    # Check and format the types of attributes as needed
    if isinstance(case.filing_date, datetime):
        formatted_date = case.filing_date.strftime('%B %Y')  # or any other desired format
    else:
        formatted_date = case.filing_date
    
    # Constructing the gist string based on the number of causes
    formatted_causes = format_causes_list(causes_list, num_causes)
    
    if num_causes == 1:
        gist_string = (
            f"This {case.type} action arises out of {fix_punctuation(case.arises_out_of)} "
            f"The {case.initiating_pleading_type} was filed in {formatted_date} and it asserts a single {cause_noun} for {formatted_causes} with a demand for {oxford_comma_join(case.relief_sought)}. "
        )
    elif num_causes in [2, 3]:
        gist_string = (
            f"This {case.type} action arises out of {fix_punctuation(case.arises_out_of)} "
            f"The {case.initiating_pleading_type} was filed in {formatted_date} and it asserts {num_causes_str} {cause_noun} for {formatted_causes} along with demands for {oxford_comma_join(case.relief_sought)}. "
        )
    else:
        gist_string = (
            f"This {case.type} action arises out of {fix_punctuation(case.arises_out_of)} "
            f"The {case.initiating_pleading_type}, filed in {formatted_date}, asserts {num_causes_str} ({num_causes}) {cause_noun}: {formatted_causes}. The {case.initiating_pleading_type} demands {oxford_comma_join(case.relief_sought)}. "
        )
    
    return gist_string
  
def generate_caption_parties_block(party, pluralize):
    name = party.whole_name if showifdef('party.modify_proposed_formal_name') else party.name.full()
    et_al = ' et al.' if pluralize else ''
    rest_of_block = (party.entity_or_capacity if not showifdef('party.modify_proposed_formal_name') and party.person_type != 'human' else '') + et_al
    role_block = party.party_role + ('s' if pluralize else '')
    return name, rest_of_block, role_block

def update_documents_drafted(title):
  
    if not hasattr(update_documents_drafted, 'document_titles'):
        update_documents_drafted.document_titles = []

    update_documents_drafted.document_titles.append(title)

def get_document_titles():
    if hasattr(update_documents_drafted, 'document_titles'):
        return update_documents_drafted.document_titles
    else:
        return []
  
def update_past_lm_proceedings(proceeding):
  # Initialize the list as a function attribute if it doesn't already exist
  if not hasattr(update_past_lm_proceedings, 'past_lm_proceedings'):
    update_past_lm_proceedings.past_lm_proceedings = []

  update_past_lm_proceedings.past_lm_proceedings.append(proceeding)
  
def get_past_lm_proceedings():
    if hasattr(update_past_lm_proceedings, 'past_lm_proceedings'):
        return update_past_lm_proceedings.past_lm_proceedings
    else:
        return []