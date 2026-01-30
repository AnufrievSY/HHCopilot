from src.config import ROOT
from src.common.readers import save_json, read_json


def save_cookies():
    i = input(f'input cookies str > ')
    c = i.split('; ')
    c = {c.split('=')[0]: c.split('=')[1] for c in c}
    fp = ROOT / 'src' / 'config' / 'cookies.json'
    save_json(c, fp)

def load_cookies():
    fp = ROOT / 'src' / 'config' / 'cookies.json'
    return read_json(fp)