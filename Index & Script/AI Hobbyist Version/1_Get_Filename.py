import json, re, os, argparse
from tqdm import tqdm
from pathlib import Path
from glob import glob
from shutil import move

parser = argparse.ArgumentParser()
parser.add_argument('-src','--source', type=str, help='未整理数据集目录', required=True)
parser.add_argument('-dst','--destination', type=str, help='目标路径', required=True)
parser.add_argument('-ver','--version', type=str, help='版本', required=True)
parser.add_argument('-lang','--language', type=str, help='语言（可选CHS/EN/JP/KR）', required=True)
args = parser.parse_args()

source = str(args.source)
dest = str(args.destination)
ver = str(args.version)
language = str(args.language)


def is_in(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False

def get_support_ver():
    indexs = glob('./Indexs/*')
    support_vers = []
    for vers in indexs:
        version = os.path.basename(vers)
        support_vers.append(version)
    versions = '|'.join(support_vers)
    return versions

def get_support_lang(version):
    if is_in(version, get_support_ver()):
        support_langs = []
        indexs = glob(f'./Indexs/{version}/*')
        for langs in indexs:
            lang_code = os.path.basename(langs).replace("_output.json","").replace(".json","")
            support_langs.append(lang_code)
        return support_langs
    else:
        print("不支持的版本")
        exit()
    
def get_path_by_lang(lang):
    langcodes = get_support_lang(ver)
    path = ['中文 - Chinese', '英语 - English',  '日语 - Japanese', '韩语 - Korean']
    try:
        i = langcodes.index(lang)
        dest_path = path[i]
        lang_code = lang
    except:
        print("不支持的语言")
        exit()
    return lang_code, dest_path

langcode, dest_lang = get_path_by_lang(language)

files = glob(os.path.join(source, "*.wav"))
indexfile = Path(f'./Indexs/{ver}/{langcode}.json').read_text(encoding="utf-8")
data = json.load(indexfile)
for wav in tqdm(files):
    file = str(wav).replace(".wav", "")
    file_hash = os.path.basename(file)
    try:
        path = data.get(file_hash).get('sourceFileName')
        wav_path = f"{source}/{os.path.dirname(path)}"
        dest_file = f"{dest}/{dest_lang}/{path}"
        dest_file = dest_file.replace(".wem",".wav")
        dis_dir = os.path.dirname(dest_file)
        if not os.path.exists(dis_dir):
            os.makedirs(dis_dir)
        move(wav, dest_file)
    except:
        pass