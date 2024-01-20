import json, os, argparse
from pathlib import Path
from glob import glob
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('-src','--source', type=str, help='源目录', required=True)
parser.add_argument('-tm','--textmap', type=str, help='TextMap路径', required=True)
parser.add_argument('-lang','--language', type=str, help='语言（可选EN/JP/KR）', required=True)
args = parser.parse_args()

textmap = args.textmap
lang = args.language
src = args.source
files = glob(f"{src}\*")
txtmap = json.loads(Path(f"{textmap}/TextMap{lang}.json").read_text(encoding="utf-8"))
txtmap_cn = json.loads(Path(F"{textmap}/TextMapCHS.json").read_text(encoding="utf-8"))

for names in tqdm(files):
    charname = os.path.basename(names)
    try:
        for key, value in txtmap.items():
            if value == charname:
                if os.path.exists(f"{src}/{charname}"):
                    cn_name = txtmap_cn[key]
                    os.rename(f"{src}/{charname}",f"{src}/{cn_name}")
    except:
        continue