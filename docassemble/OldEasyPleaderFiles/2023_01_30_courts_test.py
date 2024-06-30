import pandas
from docassemble.base.util import path_and_mimetype

__all__ = ['get_court_names', 'court_info']

court_info_by_name = {}
court_names = []

def read_data(filename):
    the_xlsx_file, mimetype = path_and_mimetype(filename)  # pylint: disable=unused-variable
    df = pandas.read_excel(the_xlsx_file)
    for indexno in df.index:
        if not df['Choice_Name'][indexno]:
            continue
        court_names.append(df['Choice_Name'][indexno])
        court_info_by_name[df['Choice_Name'][indexno]] = {"court.full_name": df['Full_Name'][indexno], "court.branch_name": df['Court_Branch_Name'][indexno], "court.street_address": df['Court_Street_Address'][indexno], "court.mail_address": df['Court_Mail_Address'][indexno], "court.city": df['Court_City'][indexno], "court.state": df['Court_State'][indexno], "court.zip": df['Court_Zip'][indexno], "court.clerk_phone": df['Court_Clerk_Phone'][indexno], "court.website": df['Court_Website'][indexno], "court.local_forms": df['Court_Local_Forms'][indexno]}

def get_court_names():
    return court_names

def court_info(court):
    if court not in court_info_by_name:
        raise Exception("Reference to invalid court " + court)
    return court_info_by_name[court]
  
def pleading_jurisdiction_block(court_info_by_name)
    if 'county' in court_info_by_name[df['Choice_Name']]:
        
  
  
read_data('data/sources/courts.xlsx')