from docassemble.base.util import defined, showifdef

__all__ = ['build_POS']

def format_contact_information(entity, role_desc=None):
    law_firm_with_newlines = f"{entity.law_firm.upper()}[BR]" if getattr(entity, 'law_firm', False) else ''
    entity.custom_address_block = f"{entity.name.full()}[BR]{law_firm_with_newlines}{entity.address.line_one()}[BR]{entity.address.line_two()}"
    contact_info = f"{entity.custom_address_block}[BR]Phone: {entity.phone_number}[BR]"
#    if getattr(entity, 'add_second_phone', False):
#        contact_info += f"Second Phone ({entity.second_phone_description}): {entity.second_phone_number}\n\n"
    contact_info += f"Fax: {entity.fax_number}[BR]Email: {entity.email}[BR]"
    if showifdef('entity.add_second_email'):
        contact_info += f"Alt. Email ({entity.second_email_recipient}): {entity.second_email}[BR]"
    if role_desc:
        contact_info += f"*{role_desc}*\n\n"
    return contact_info

def build_POS(all_servees, documents_served, server_address):
    grouped_servees = {}  # Dictionary to group servees by methods and date
    for servee in all_servees:
        key = (tuple(servee.service_methods), servee.service_date)
        if key not in grouped_servees:
            grouped_servees[key] = []
        grouped_servees[key].append(servee)

    POS_text = f"At the time of service, I was over 18 years of age and not a party to this action. My business address is {server_address}.\n\n"

    POS_text += f"I served the following documents:\n\n **{documents_served}**\n\n"

    service_method_dict = {
    'U.S. Mail': "I enclosed the documents in a sealed envelope or package addressed to the person or persons below and placed the envelope for collection and mailing, following our ordinary business practices. I am readily familiar with this business's practice for collecting and processing correspondence for mailing. On the same day that correspondence is placed for collection and mailing, it is deposited in the ordinary course of business with the United States Postal Service, in a sealed envelope with postage fully prepaid.",
    'Certified Mail': 'xxxxx',
    'Overnight Delivery': 'I enclosed the documents in an envelope or package provided by an overnight delivery carrier and addressed to the addressed to the person or persons below. I placed the envelope or package for collection and overnight delivery at an office or a regularly utilized drop box of the overnight delivery carrier.',
    'Email': 'Based on a court order or an agreement of the parties to accept service by electronic transmission, I electronically served the documents to the person or persons at the electronic service addresses below. I did not receive, within a reasonable time after the transmission, any electronic message or other indication that the transmission was unsuccessful.',
    'Fax': 'Based on an agreement of the parties to accept service by fax transmission, I faxed the documents to the person or persons at the fax numbers listed below. No error was reported by the fax machine that I used. A copy of the record of the fax transmission, which I printed out, is attached.',
    'Personal': "personally delivered the documents to the person or persons at the addresses listed below. (1) For a party represented by an attorney, delivery was made (a) to the attorney personally; or (b) by leaving the documents at the attorney's office, in an envelope or package clearly labeled to identify the attorney being served, with a receptionist or an individual in charge of the office; or (c) if there was no person in the office with whom the notice or papers could be left, by leaving them in a conspicuous place in the office between the hours of nine in the morning and five in the evening. (2) For a party, delivery was made to the party or by leaving the documents at the party's residence with some person not younger than 18 years of age between the hours of eight in the morning and eight in the evening."
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