import pandas as pd

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from io import StringIO

def samples_xlsx(file_path):
    df = pd.read_excel(file_path)
    columns = df.columns
    entities = df['Entities']
    samples_dict = {}
    for c in columns:
        if 'Sample' in c:
            samples_dict[c] = {}
            samples = df[c]
            for i, s in enumerate(samples):
                if s > 0:
                    samples_dict[c][entities[i]] = s
    return samples_dict


def samples_csv(file_path):

    df = pd.read_csv(file_path)
    columns = df.columns
    entities = df['Entities']
    samples_dict = {}
    for c in columns:
        if 'Sample' in c:
            samples_dict[c] = {}
            samples = df[c]
            for i, s in enumerate(samples):
                if s > 0:
                    samples_dict[c][entities[i]] = s

    return samples_dict

def from_csv(file_path, head_column='None'):
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)

        if head_column != 'None':
            try:
                df_dict = df.set_index(head_column).T.to_dict()
            except KeyError:
                print(head_column, 'not in columns.', '\nColumns Found:', list(df.columns))
                df_dict = {}
        else:
            id_columns = [c for c in list(df.columns) if 'id ' in c.lower() + ' ']
            if len(id_columns) == 1:
                selected_column = id_columns[0]
                df_dict = df.set_index(selected_column).T.to_dict()
            else:
                print('Multiple ids columns found... Define one id column in "head_column" argument')
                df_dict = {}
    else:
        print("Input file is not csv ...")
        df_dict = {}

    return df_dict


def from_tsv(file_path, head_column='None'):
    
    if file_path.endswith('.tsv'):
        df = pd.read_csv(file_path, sep='\t')

        if head_column != 'None':
            try:
                df_dict = df.set_index(head_column).T.to_dict()
            except KeyError:
                print(head_column, 'not in columns.', '\nColumns Found:', list(df.columns))
                df_dict = {}
        else:
            id_columns = [c for c in list(df.columns) if 'id ' in c.lower() + ' ']
            if len(id_columns) == 1:
                selected_column = id_columns[0]
                df_dict = df.set_index(selected_column).T.to_dict()
            else:
                print('Multiple ids columns found... Define one id column in "head_column" argument')
                df_dict = {}
    else:
        print("Input file is not tsv ...")
        df_dict = {}

    return df_dict


def from_xlsx(file_path, head_column='None'):
    
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
        if head_column != 'None':
            try:
                df_dict = df.set_index(head_column).T.to_dict()
            except KeyError:
                print(head_column, 'not in columns.', '\nColumns Found:', list(df.columns))
                df_dict = {}
        else:
            id_columns = [c for c in list(df.columns) if 'id ' in c.lower() + ' ']
            if len(id_columns) == 1:
                selected_column = id_columns[0]
                df_dict = df.set_index(selected_column).T.to_dict()
            else:
                print('Multiple ids columns found... Define one id column in "head_column" argument')
                df_dict = {}
    else:
        print("Input file is not xlsx ...")
        df_dict = {}

    return df_dict


def from_pdf(file_path, starting_page='None', ending_page='None'):
    
    if file_path.endswith('.pdf'):
        print('Converting pdf to text ...')
        rsrcmgr = PDFResourceManager()
        sio = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        fp = open(file_path, 'rb')
        if starting_page != 'None' and ending_page != 'None':
            for page in list(PDFPage.get_pages(fp))[starting_page-1:ending_page]:
                interpreter.process_page(page)
        elif starting_page != 'None':
            for page in list(PDFPage.get_pages(fp))[starting_page-1:]:
                interpreter.process_page(page)
        elif ending_page != 'None':
            for page in list(PDFPage.get_pages(fp))[:ending_page]:
                interpreter.process_page(page)
        else:
            for page in list(PDFPage.get_pages(fp)):
                interpreter.process_page(page)
        fp.close()

        text = sio.getvalue()

        device.close()
        sio.close()
        data = {'text': text}
    else:
        print("Input file is not pdf ...")
        data = {}

    return data


def from_txt(file_path):
    
    if file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            text = file.read().replace('\n', '')
            data = {'text': text}
    else:
        print("Input file is not txt ...")
        data = {}
    
    return data
