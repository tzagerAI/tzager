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

    try:
        signal.alarm(60)
        
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()

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
    except TimeoutException:
        final_data = {}
        final_data['paper_title'] = title
        final_data['full_text'] = ''
        return final_data


