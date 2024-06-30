import pandas
from docassemble.base.util import path_and_mimetype

__all__ = ['get_fruit_names']

def read_data(filename):
    the_xlsx_file, mimetype = path_and_mimetype(filename)
    df = pandas.read_excel(the_xlsx_file)

  
def get_fruit_names():
    fruit_names = df['Name']
    return fruit_names

read_data('data/static/fruit_data.xlsx')