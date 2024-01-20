import json, re, os, argparse
from tqdm import tqdm
from pathlib import Path
from glob import glob
from shutil import move

parser = argparse.ArgumentParser()
parser.add_argument('-src','--source', type=str, help='待二次分类原神数据集', required=True)
parser.add_argument('-dst','--destination', type=str, help='目标路径', required=True)
args = parser.parse_args()

source = str(args.source)
dest = str(args.destination)
monster = 'monster'
battle = 'battle|life'
conv = 'fetter'
vaild_content = r'[a-zA-Z0-9\u4e00-\u9fa5\u3040-\u309f\u30a0-\u30ff\u1100-\u11ff\u3130-\u318f\uac00-\ud7af]+'
placeholder = r'[<>{}]'

labfiles = glob(f"{source}/**/*.lab")

def is_in(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False
    
def check(full_path, regx):
    if re.findall(regx, full_path):
        return True
    else:
        return False
    
def check_content(text, regx):
    if re.search(regx, text):
        return True
    else:
        return False

for file in tqdm(labfiles):
    lab_content = Path(file).read_text(encoding='utf-8')
    spk = os.path.basename(os.path.dirname(file))
    lab_file_name = os.path.basename(file)
    wav_file_name = lab_file_name.replace(".lab",".wav")
    src = f"{source}/{spk}"
    if not check_content(lab_content,vaild_content):
        out_path = f"{dest}/其它语音 - Others/{spk}"
    elif is_in(file,conv):
        out_path = f"{dest}/多人对话 - Conversation/{spk}" 
    elif check_content(lab_content,placeholder):
        out_path = f"{dest}/带变量语音 - Placeholder/{spk}"
    elif is_in(file,monster):
        out_path = f"{dest}/怪物语音 - Monster/{spk}"
    elif is_in(file,battle):
        out_path = f"{dest}/战斗语音 - Battle/{spk}"
    else:
        continue
    if not os.path.exists(out_path):
        Path(f"{out_path}").mkdir(parents=True)
    move(f"{src}/{lab_file_name}",f"{out_path}/{lab_file_name}")
    move(f"{src}/{wav_file_name}",f"{out_path}/{wav_file_name}")
    tqdm.write(f"音频文件：{src}/{wav_file_name}\n标注文件：{src}/{lab_file_name}\n已移动至：{out_path}\n-----------")

    
