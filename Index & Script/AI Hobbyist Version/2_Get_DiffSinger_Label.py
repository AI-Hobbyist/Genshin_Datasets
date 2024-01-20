import json, re, os, argparse
from tqdm import tqdm
from pathlib import Path
from glob import glob

parser = argparse.ArgumentParser()
parser.add_argument('-src','--source', type=str, help='未整理数据集目录', required=True)
parser.add_argument('-ver','--version', type=str, help='版本', required=True)
parser.add_argument('-dst','--destination', type=str, help='目标路径', required=True)
parser.add_argument('-lang','--language', type=str, help='语言（可选CHS/EN/JP/KR）', required=True)
args = parser.parse_args()

source = str(args.source)
dest = str(args.destination)
language = str(args.language).upper()
ver = str(args.version)
player = '旅行者|旅人|Traveler|여행자'

def is_in(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False

def is_file(full_path):
    if os.path.exists(full_path):
        return True
    else:
        return  False
    
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

def ren_player(player,lang):
    langcodes = get_support_lang(ver)
    player_boy_names = ['空', 'Aether', '空', '아이테르']
    player_girl_names = ['荧', 'Lumine', '蛍', '루미네']
    p_name = player
    if p_name == "PlayerBoy" or p_name == "PlayerGirl":
        if p_name == "PlayerBoy":
            i = langcodes.index(lang)
            p_name = player_boy_names[i]
        if p_name == "PlayerGirl":
            i = langcodes.index(lang)
            p_name = player_girl_names[i]
    else:
        p_name = player
    return p_name

indexfile = Path(f'./Indexs/{ver}/{langcode}.json').read_text(encoding="utf-8")
data = json.loads(indexfile)
for k in tqdm(data.keys()):
    try:
        text = data.get(k).get('voiceContent')
        char_name = data.get(k).get('talkName')
        avatar_name = data.get(k).get('avatarName')
        if char_name is not None:
            if is_in(char_name, player) == True:
                char_name = ren_player(avatar_name,langcode)
        path = data.get(k).get('sourceFileName')
        path = path.replace(".wem",".wav")
        wav_source = source + '/' + path
        wav_file = os.path.basename(path)
        if char_name is not None:
            vo_dest_dir = f"{dest}/{dest_lang}/数据集 - Datasets/{char_name}"
            lab_file = wav_file.replace(".wav",".lab")
            vo_lab_path = f"{vo_dest_dir}/{lab_file}"
            if is_file(wav_source) == True:
                if not os.path.exists(vo_dest_dir):
                    Path(f"{vo_dest_dir}").mkdir(parents=True)
                dest_path = vo_lab_path            
                Path(dest_path).write_text(text, encoding='utf-8')
    except:
        pass
