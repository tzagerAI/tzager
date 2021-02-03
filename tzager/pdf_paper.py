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


