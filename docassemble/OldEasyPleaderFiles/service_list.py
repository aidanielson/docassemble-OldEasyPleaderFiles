from docassemble.base.util import defined, showifdef

__all__ = ['build_service_list']

def format_contact_information(entity, role_desc=None):
    law_firm_with_newlines = f"{entity.law_firm}\n\n" if getattr(entity, 'law_firm', False) else ''
    entity.custom_address_block = f"**{entity.name.full()}**\n\n{law_firm_with_newlines}{entity.address.line_one()}\n\n{entity.address.line_two()}"
    contact_info = f"{entity.custom_address_block}\n\nPhone: {entity.phone_number}\n\n"
#    if getattr(entity, 'add_second_phone', False):
#        contact_info += f"Second Phone ({entity.second_phone_description}): {entity.second_phone_number}\n\n"
    contact_info += f"Fax: {entity.fax_number}\n\nEmail: {entity.email}\n\n"
    if showifdef('entity.add_second_email'):
        contact_info += f"Second Email ({entity.second_email_recipient}): {entity.second_email}\n\n"
    if role_desc:
        contact_info += f"**{role_desc}**\n\n"
    return contact_info

def build_service_list(all_served_parties):
    parties_by_lawyer = {}

    for party in all_served_parties:
        if party.lawyers:
            for lawyer in party.lawyers:
                if lawyer not in parties_by_lawyer:
                    parties_by_lawyer[lawyer] = []
                parties_by_lawyer[lawyer].append(party)

    service_list = "[BOLDCENTER]Service List\n\n"

    for lawyer, represented_parties in parties_by_lawyer.items():
        roles_and_names = {}
        for rep_party in represented_parties:
            party_role = rep_party.party_role
            if party_role not in roles_and_names:
                roles_and_names[party_role] = []
            roles_and_names[party_role].append(rep_party.whole_name)

        attorneys_for_line = "Attorneys for " + ", ".join(f"{party_role + 's' if len(names) > 1 else party_role} {' and '.join(names)}" for party_role, names in roles_and_names.items())
        service_list += format_contact_information(lawyer, attorneys_for_line)

    unrepresented_parties = [party for party in all_served_parties if not party.lawyers]
    for party in unrepresented_parties:
        service_list += format_contact_information(party, f"{party.party_role}, in pro per")

    return service_list