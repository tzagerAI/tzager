import json
import requests
import signal

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

signal.signal(signal.SIGALRM, timeout_handler)


def pdf_text(path, title):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO

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

    final_data['paper_title'] = title
    final_data['full_text'] = new_txt
    return final_data

def paper_scopes(password, dir_path):
    import glob
    
    overall_data_to_return = []
    unconverted_files = []
    all_pdfs_in_path = glob.glob(dir_path+'/*')
    for ii, path in enumerate(all_pdfs_in_path):
        title = path.replace(dir_path + '/', '').replace('.pdf', '')
        print('Convering pdf to text ...', ii+1, '/', len(all_pdfs_in_path))
        signal.alarm(1000)
        try:
            final_data = pdf_text(path, title) # Whatever your function that might hang
        except TimeoutException:
            final_data = None
        
        signal.alarm(0)
        if final_data:
            overall_data_to_return.append(final_data)
        else:
            unconverted_files.append(path)

    print('Uploading text ...')
    if unconverted_files:
        print("Files that fail to convert:", unconverted_files)
    else:
        print("All files converted succesfully")

    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/papers_scopes/' + password, json=json.dumps({'papers': overall_data_to_return}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def complemetary_papers(password, data_for_complemetary_papers):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/complemetary_papers/' + password, json=json.dumps({'data_for_complemetary_papers': data_for_complemetary_papers}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def scientific_analysis(password, papers, data_for_scientific_analysis, complemetary_data):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/scientific_analysis_papers/' + password, json=json.dumps({'data_for_scientific_analysis': data_for_scientific_analysis, 'papers': papers, 'complemetary_data': complemetary_data}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def paper_augment_nodes(password, papers, data_for_scientific_analysis, complemetary_data, scopes):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/paper_augment_nodes/' + password, json=json.dumps({'data_for_scientific_analysis': data_for_scientific_analysis, 'papers': papers, 'complemetary_data': complemetary_data, 'scopes': scopes}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def paper_augment_scopes(password, papers, data_for_scientific_analysis, complemetary_data, scopes):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/paper_augment_scopes/' + password, json=json.dumps({'data_for_scientific_analysis': data_for_scientific_analysis, 'papers': papers, 'complemetary_data': complemetary_data, 'scopes': scopes}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def question_hbn(password, question):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/question_hbn/' + password, json=json.dumps({'question_text': question}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def question_papers(password, question, papers):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/question_papers/' + password, json=json.dumps({'question_text': question, 'papers': papers}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def intuition_connection(password, papers, focus_on=None):
    final_data = {'papers': papers, 'focus_on': focus_on}
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/intuition_connection_papers/' + password, json=json.dumps(final_data))
    if response.status_code == 200:
        r_data = dict(response.json())
    else:
        r_data = {'error': response.status_code}
        r_data = dict(r_data)
    return r_data

def intuition_mechanisms(password, papers, focus_on=None):
    final_data = {'papers': papers, 'focus_on': focus_on}
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/intuition_mechanisms_papers/' + password, json=json.dumps(final_data))
    if response.status_code == 200:
        r_data = dict(response.json())
    else:
        r_data = {'error': response.status_code}
        r_data = dict(r_data)
    return r_data