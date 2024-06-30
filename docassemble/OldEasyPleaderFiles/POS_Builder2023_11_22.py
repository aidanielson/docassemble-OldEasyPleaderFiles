from docassemble.base.util import defined, showifdef, log
import textwrap

__all__ = ['build_POS', 'build_service_address_block']

def format_contact_information(entity, role_desc=None):
    # Initialize contact_info as an empty string
    contact_info = ""
    
    # Validate entity has all required attributes
    required_attributes = ['name', 'address', 'phone_number', 'fax_number', 'email']
    for attr in required_attributes:
        if not getattr(entity, attr, False):
            log(f"The entity is missing a required attribute: {attr}")
            return contact_info
    
    # Assume other necessary attributes exist and are valid, such as entity.name.full(), etc.
    # Construct the contact block, adding each piece of information
    law_firm_with_newlines = f"{entity.law_firm.upper()}[BR]" if getattr(entity, 'law_firm', False) else ''
    entity.custom_address_block = f"{entity.name.full()}[BR]{law_firm_with_newlines}{entity.address.line_one()}[BR]{entity.address.line_two()}"
    contact_info = f"{entity.custom_address_block}[BR]Phone: {entity.phone_number}[BR]"
    contact_info += f"Fax: {entity.fax_number}[BR]Email: {entity.email}[BR]"

    if showifdef('entity.add_second_email'):
        contact_info += f"Alt. Email ({entity.second_email_recipient}): {entity.second_email}[BR]"
    if role_desc:
        contact_info += f"*{role_desc}*\n\n"
    return contact_info

def build_POS(all_servees, documents_served, server_address):
    # Initial logging to start the POS building process
    log("Starting to build Proof of Service document.")
    
    # Validate all_servees is not empty and contains the right attributes
    if not all_servees:
        log("The all_servees list is empty. Cannot proceed without servees.")
        return ""

    # Validate each servee has the necessary attributes before proceeding
    for servee in all_servees:
        if not hasattr(servee, 'service_methods') or not servee.service_methods:
            log(f"Servee {servee} is missing the service_methods attribute or it is empty.")
            continue
        if not hasattr(servee, 'service_date'):
            log(f"Servee {servee} is missing the service_date attribute.")
            continue
            
   # The rest of the function remains unchanged, but add logging at key points to help diagnose issues
    # For example:
    grouped_servees = {}  # Dictionary to group servees by methods and date
    for servee in all_servees:
        # Existing grouping code with added logging
        key = (tuple(servee.service_methods), servee.service_date)
        log(f"Grouping servee with key: {key}")
        if key not in grouped_servees:
            grouped_servees[key] = []
        grouped_servees[key].append(servee)

    POS_text = f"At the time of service, I was over 18 years of age and not a party to this action. My business address is {server_address}.\n\n"

    POS_text += f"I served the following documents:\n\n **{documents_served}**\n\n"

    service_method_dict = {
    'U.S. Mail (placed for mailing)': "Pursuant to CCP §§ 1013(a) and 1013a(3), I enclosed the document(s) in a sealed envelope or package addressed to the person(s) or entity(ies) at the address(es) listed below, and placed it for collection and mailing, following this business’s regular practice. I am readily familiar with this business’ practice for collection and processing of correspondence for mailing with the United States Postal Service. On the same day that correspondence is placed for collection and mailing, it is deposited in the ordinary course of business with the United States Postal Service, in a sealed envelope with postage fully prepaid.",
    'U.S. Mail (deposited with USPS)': "Pursuant to CCP §§ 1013(a), 1013(b), 1013a(1), and 1013a(2), I enclosed the document(s) in a sealed envelope or package, with USPS First-Class Mail postage thereon fully prepaid, addressed to the person(s) or entity(ies) at the address(es) listed below, and deposited it in a post office, mailbox, subpost office, substation, or mail chute, or other like facility regularly maintained by the United States Postal Service.",
    'Certified Mail': 'Pursuant to CCP §§ 1013(a), 1013(b), 1013a(1), 1013a(2), and 1020(a), I enclosed the document(s) in a sealed envelope or package, with USPS First-Class Mail, Certified postage thereon fully prepaid, addressed to the person(s) or entity(ies) at the address(es) listed below, and deposited it in a post office, mailbox, subpost office, substation, or mail chute, or other like facility regularly maintained by the United States Postal Service.',
    'Overnight Delivery': 'Pursuant to CCP § 1013(c), I enclosed the document(s) in a sealed envelope or package provided by an overnight delivery carrier, with delivery fees paid or provided for, addressed to the person(s) or entity(ies) at the address(es) listed below. I placed the envelope or package for collection and overnight delivery at an office or a regularly utilized drop box of the overnight delivery carrier.',
    'USPS Priority Mail Express': 'Pursuant to CCP §§ 1013(c) and 1013(d), I enclosed the document(s) in a sealed Priority Mail Express envelope or package provided by the United States Postal Service, with Priority Mail Express postage paid, addressed to the person(s) or entity(ies) at the address(es) listed below, and deposited it with a post office, mailbox, subpost office, substation, or mail chute, or other like facility regularly maintained by the United States Postal Service for receipt of Express Mail.',
    'Email': 'Pursuant to CCP § 1010.6; Cal. Rules of Court, rule 2.251 and under the express agreement of all parties hereto, or as otherwise authorized by law, I transmitted an email from my email address – Anthony@DanielsonKim.com – to the party(ies) or person(s) at the electronic service address(es) listed below. I attached complete, true, and correct PDF copies of the document(s) to the email. The subject line of the email commenced with the words “ELECTRONIC SERVICE” in ALL CAPS typeface, and followed by identifying the short case name and the case number of the above-captioned action. The verbatim titles of the documents served were conspicuously listed and individually numbered in the body of the e-mail. I did not receive, within a reasonable time after the transmission, any electronic message or other indication that the transmission was unsuccessful, and a true and correct copy of the transmitted email is attached hereto.',
    'Fax': 'Pursuant to CCP §§ 1013(e) and 1013(f), and based on an agreement of the parties to accept service by fax transmission, I faxed the documents to the person or persons at the fax numbers listed below. No error was reported by the fax machine that I used. A copy of the record of the fax transmission, which I printed out, is attached.',
    'Personal': "Pursuant to CCP § 1011, I personally delivered the documents to the person or persons at the addresses listed below. (1) For a party represented by an attorney, delivery was made (a) to the attorney personally; or (b) by leaving the documents at the attorney's office, in an envelope or package clearly labeled to identify the attorney being served, with a receptionist or an individual in charge of the office; or (c) if there was no person in the office with whom the notice or papers could be left, by leaving them in a conspicuous place in the office between the hours of nine in the morning and five in the evening. (2) For a party, delivery was made to the party or by leaving the documents at the party's residence with some person not younger than 18 years of age between the hours of eight in the morning and eight in the evening.",
    'Courtesy Email Copy': "As a courtesy and in order to minimize any potential service dispute, I transmitted an email from my email address – Anthony@DanielsonKim.com – to the party(ies) or person(s) at the electronic service address(es) listed below. I attached complete, true, and correct PDF copies of the document(s) to the email. The subject line of the email commenced with the words “COURTESY ELECTRONIC SERVICE” in ALL CAPS typeface, followed by the short case name and the case number of the above-captioned action. The verbatim titles of the documents served were conspicuously listed and individually numbered in the body of the e-mail. I did not receive, within a reasonable time after the transmission, any electronic message or other indication that the transmission was unsuccessful, and a true and correct copy of the transmitted email is attached hereto."
}

    for (methods, date), servees in grouped_servees.items():  # Iterate through grouped servees
        methods_text = "\n\n**AND** ".join(f"**By {method}:**[BR]{service_method_dict[method]}" for method in methods)
        POS_text += f"**on {date}**\n\n{methods_text}\n\n"

        parties_by_lawyer = {}
        for party in servees:  # Work with servees grouped by methods and date
            if party.lawyers:
                for lawyer in party.lawyers:
                    if lawyer not in parties_by_lawyer:
                        parties_by_lawyer[lawyer] = []
                    parties_by_lawyer[lawyer].append(party)

        for lawyer, represented_parties in parties_by_lawyer.items():
          roles_and_names = {}
          for rep_party in represented_parties:
            role = rep_party.role
            if role not in roles_and_names:
                roles_and_names[role] = []
            roles_and_names[role].append(rep_party.whole_name)

        attorneys_for_line = "Attorneys for " + ", ".join(f"{role + 's' if len(names) > 1 else role} {' and '.join(names)}" for role, names in roles_and_names.items())
        POS_text += format_contact_information(lawyer, attorneys_for_line)

        unrepresented_parties = [party for party in servees if not party.lawyers.there_are_any]
        for party in unrepresented_parties:
            POS_text += format_contact_information(party, f"{party.role}, in pro per")

    return POS_text

def format_contact_blocks(contact_blocks):
    """
    Formats the contact service blocks, wrapping each block at 30 characters.
    Returns a list of formatted blocks.
    """
    def wrap_text(text):
        """
        Wrap text at 30 characters, handling newlines.
        """
        wrapped_lines = []
        for line in text.split('\n'):
            wrapped_lines.extend(textwrap.wrap(line, width=30))
        return wrapped_lines

    formatted_blocks = []
    
    # Format each contact block individually
    for block in contact_blocks:
        wrapped_block = wrap_text(block)
        formatted_block = "\n".join(wrapped_block)
        formatted_blocks.append(formatted_block)

    return formatted_blocks

def build_service_address_block(servees):
    parties_by_lawyer = {}
    for party in servees:
        if party.lawyers:
            for lawyer in party.lawyers:
                if lawyer not in parties_by_lawyer:
                    parties_by_lawyer[lawyer] = []
                parties_by_lawyer[lawyer].append(party)

    contact_blocks = []
    for lawyer, represented_parties in parties_by_lawyer.items():
        roles_and_names = {}
        for rep_party in represented_parties:
            role = rep_party.role
            if role not in roles_and_names:
                roles_and_names[role] = []
            roles_and_names[role].append(rep_party.whole_name)

        attorneys_for_line =  "Attorneys for " + ", ".join(
            f"{role + 's' if len(names) > 1 else role} {' and '.join(names)}"
            for role, names in roles_and_names.items()
        )
        contact_info = format_contact_information(lawyer, attorneys_for_line)
        contact_blocks.append(contact_info)

    unrepresented_parties = [party for party in servees if not party.lawyers.there_are_any]
    for party in unrepresented_parties:
        contact_info = format_contact_information(party, f"{party.role}, in pro per")
        contact_blocks.append(contact_info)

    return format_contact_blocks(contact_blocks)