import re


def rem_dbl_newlines(str):
    return str.replace('\r\n\r\n', '\r\n').replace('\n\n', '\n')


def strip_dbl_spaces(str):
    return re.sub(' +', ' ', str).strip()


def strip_urls_newlines(str):
    s = re.sub(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|'
        r'(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’'
        r']))',
        '',
        str,
    )
    s = rem_dbl_newlines(s)
    s = s.strip(' \t\n\r')
    return s


def _shorten_txt(txt: str, n: int = 30) -> str:
    if len(txt) <= n:
        return txt
    return txt[:n] + "..."
