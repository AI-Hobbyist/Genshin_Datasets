import json, re, os, argparse
from tqdm import tqdm
from pathlib import Path
from glob import glob
from shutil import copy, move
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str, help='待二次分类原神数据集', required=True)
parser.add_argument('--dest', type=str, help='目标路径', required=True)
args = parser.parse_args()

source = str(args.source)
dest = str(args.dest)
monster = 'monster'
battle = 'battle|life'
conv = 'fetter'

def is_in(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False
    
def has_vaild_content(text):
    pattern = r'[a-zA-Z0-9\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]+'
    if re.search(pattern, text):
        return True
    else:
        return False