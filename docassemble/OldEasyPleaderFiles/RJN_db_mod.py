import pandas
from docassemble.base.util import path_and_mimetype

__all__ = ['get_RJN_matter_types', 'fruit_info']

fruit_info_by_name = {}
RJN_matter_types = []

def read_data(filename):
    the_xlsx_file, mimetype = path_and_mimetype(filename)  # pylint: disable=unused-variable
    df = pandas.read_excel(the_xlsx_file)
    for indexno in df.index:
        if not df['Type'][indexno]:
            continue
        RJN_matter_types.append(df['Type'][indexno])
        fruit_info_by_name[df['Type'][indexno]] = {"stat_auth": df['Stat_Auth'][indexno], "seeds": df['Seeds'][indexno], "case_auth": df['Case_Auth'][indexno]}
 

def get_RJN_matter_types():
    return RJN_matter_types


def fruit_info(fruit):
    if fruit not in fruit_info_by_name:
        raise Exception("Reference to invalid fruit " + fruit)
    return fruit_info_by_name[fruit]

read_data('data/sources/RJN_Data.xlsx')