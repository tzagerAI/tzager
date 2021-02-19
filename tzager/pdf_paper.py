import json
import requests


def analysis(password, path, title):

    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO

    print('Convering pdf to text ...')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password_pdf = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password_pdf, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    full_text = text.replace('-\n', '').replace('’', "'")
    fp.close()
    device.close()
    retstr.close()
    text = text.replace('-\n', '').replace('’', "'")
    lines = text.split('\n')
    lines_section_ids_dict = {}
    lines_section_ids = []
    for i, line in enumerate(lines[1:-2]):
        if len(lines[i-1]) == 0 and len(lines[i+1]) == 0 and len(lines[i]) > 3 and not str(lines[i]).isdigit():
            lines_section_ids_dict[i] = lines[i]
            lines_section_ids.append(i)

    ref_id = -1
    data = []
    for id in lines_section_ids_dict:
        data.append((lines_section_ids_dict[id], id))
    data = dict(data)

    final_data = {}
    final_data['paper_title'] = title
    final_data['full_text'] = full_text
    try:
        ref_id = data['References']
    except KeyError:
        ref_id = len(lines) - 1
    for i, id in enumerate(lines_section_ids):
        if i < len(lines_section_ids) - 1 and id < ref_id:
            start = lines_section_ids[i]
            end = lines_section_ids[i+1]
            interval_lines = lines[start+1:end]
            interval_lines_txt = ' '.join(interval_lines)
            if interval_lines and len(interval_lines_txt) > 100:
                final_data[lines_section_ids_dict[start]] = ' '.join(interval_lines)
                
    print('Uploading text ...')
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/paper_analysis/' + password, json=json.dumps(final_data))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def scientific_analysis(password, path, title, topn):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO

    print('Convering pdf to text ...')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password_pdf = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password_pdf, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()
    fp.close()
    device.close()
    retstr.close()
    text = text.replace('-\n', '').replace('’', "'").replace('inﬂ', 'infl')
    lines = text.split('\n')
    lines_section_ids_dict = {}
    lines_section_ids = []
    for i, line in enumerate(lines[1:-2]):
        if len(lines[i-1]) == 0 and len(lines[i+1]) == 0 and len(lines[i]) > 3 and not str(lines[i]).isdigit():
            lines_section_ids_dict[i] = lines[i]
            lines_section_ids.append(i)

    data = []
    for id in lines_section_ids_dict:
        data.append((lines_section_ids_dict[id], id))
    data = dict(data)

    final_data = {}
    new_txt = ''
    try:
        ref_id = data['References']
    except KeyError:
        ref_id = len(lines) - 1
    for i, id in enumerate(lines_section_ids):
        if i < len(lines_section_ids) - 1 and id < ref_id:
            start = lines_section_ids[i]
            end = lines_section_ids[i+1]
            interval_lines = lines[start+1:end]
            interval_lines_txt = ' '.join(interval_lines)
            if 'Abbreviations' not in  lines_section_ids_dict[start] and '18 of 36' not in  lines_section_ids_dict[start]:
                new_txt += interval_lines_txt
            if interval_lines and len(interval_lines_txt) > 100:
                final_data[lines_section_ids_dict[start]] = ' '.join(interval_lines)
    
    final_data['paper_title'] = title
    final_data['full_text'] = new_txt
    final_data['topn'] = topn
    print('Uploading text ...')
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/scientific_analysis/' + password, json=json.dumps(final_data))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def focus_on(password, pkey, entity):
    final_data = {'password': password, 'pkey': pkey, 'entity': entity}
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/focus_on', json=json.dumps(final_data))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def compare_papers(password, key1, key2, edges_1, edges_2, main_scope_1, main_scope_2):
    final_data = {'password': password, 'key1': key1, 'key2': key2, 'edges_1': edges_1, 'edges_2': edges_2, 'main_scope_1': main_scope_1, 'main_scope_2': main_scope_2}
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/compare_papers', json=json.dumps(final_data))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def directory_analysis(password, dir_path):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO
    import glob


    overall_data_to_return = []
    all_pdfs_in_path = glob.glob(dir_path+'/*')
    for ii, path in enumerate(all_pdfs_in_path):
        title = path.replace(dir_path + '/', '').replace('.pdf', '')
        print('Convering pdf to text ...', ii+1, '/', len(all_pdfs_in_path))
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password_pdf = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password_pdf, caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        text = text.replace('-\n', '').replace('’', "'").replace('inﬂ', 'infl')
        lines = text.split('\n')
        lines_section_ids_dict = {}
        lines_section_ids = []
        for i, line in enumerate(lines[1:-2]):
            if len(lines[i-1]) == 0 and len(lines[i+1]) == 0 and len(lines[i]) > 3 and not str(lines[i]).isdigit():
                lines_section_ids_dict[i] = lines[i]
                lines_section_ids.append(i)

        data = []
        for id in lines_section_ids_dict:
            data.append((lines_section_ids_dict[id], id))
        data = dict(data)

        final_data = {}
        new_txt = ''
        try:
            ref_id = data['References']
        except KeyError:
            ref_id = len(lines) - 1
        for i, id in enumerate(lines_section_ids):
            if i < len(lines_section_ids) - 1 and id < ref_id:
                start = lines_section_ids[i]
                end = lines_section_ids[i+1]
                interval_lines = lines[start+1:end]
                interval_lines_txt = ' '.join(interval_lines)
                if 'Abbreviations' not in  lines_section_ids_dict[start] and '18 of 36' not in  lines_section_ids_dict[start]:
                    new_txt += interval_lines_txt
                if interval_lines and len(interval_lines_txt) > 100:
                    final_data[lines_section_ids_dict[start]] = ' '.join(interval_lines)
        
        final_data['paper_title'] = title
        final_data['full_text'] = new_txt
        print('Uploading text ...', ii+1, '/', len(all_pdfs_in_path))
        print()
        response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/directory_analysis/' + password, json=json.dumps(final_data))
        if response.status_code == 200:
            r_data = dict(response.json())
        else:
            r_data = {'error': response.status_code}
            r_data = dict(r_data)

        if 'paper_id' in r_data:
            overall_data_to_return.append(r_data['paper_id'])
    
    return overall_data_to_return
    
def directory_scopes(password, papers_ids):
    final_data = {'papers_ids': papers_ids}
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/directory_scopes/' + password, json=json.dumps(final_data))
    if response.status_code == 200:
        r_data = dict(response.json())
    else:
        r_data = {'error': response.status_code}
        r_data = dict(r_data)
    return r_data

def complementary_papers(password, papers_ids):
    final_data = {'papers_ids': papers_ids}
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/complementary_papers/' + password, json=json.dumps(final_data))
    if response.status_code == 200:
        r_data = dict(response.json())
    else:
        r_data = {'error': response.status_code}
        r_data = dict(r_data)
    return r_data

def intuition_connection(password, papers_ids, focus_on=None):
    final_data = {'paper_ids': papers_ids, 'focus_on': focus_on}
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/intuition_connection/' + password, json=json.dumps(final_data))
    if response.status_code == 200:
        r_data = dict(response.json())
    else:
        r_data = {'error': response.status_code}
        r_data = dict(r_data)
    return r_data

def intuition_mechanisms(password, papers_ids, focus_on=None):
    final_data = {'paper_ids': papers_ids, 'focus_on': focus_on}
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/intuition_mechanisms/' + password, json=json.dumps(final_data))
    if response.status_code == 200:
        r_data = dict(response.json())
    else:
        r_data = {'error': response.status_code}
        r_data = dict(r_data)
    return r_data

