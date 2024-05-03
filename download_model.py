import requests
import os
import sys
import shutil
import zipfile
from openxlab.model import download

"""
Automatic download of model files from openxlab.
Currently only support openxlab automatic download, other platform model files need to be downloaded manually.
"""

if len(sys.argv) == 2:
    model_repo = sys.argv[1]
else:
    print("Usage: python download_model.py <model_repo>")
    print("Example: python download_model.py jujimeizuo/EmoLLM_Model")
    exit()

dir_name = "model"

if os.path.isdir(dir_name):
    print("model file exist")
    exit(0)

download_url = "https://code.openxlab.org.cn/api/v1/repos/{}/archive/main.zip".format(model_repo)
output_filename = "model_main.zip"  

# download model file
response = requests.get(download_url, stream=True)
if response.status_code == 200:
    with open(output_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    print(f"Successfully downloaded model file")
else:
    print(f"Failed to download the model file. HTTP status code: {response.status_code}")
    exit()

if not os.path.isfile(output_filename):
    raise FileNotFoundError(f"ZIP file '{output_filename}' not found in the current directory.")

temp_dir = f".{os.sep}temp_{os.path.splitext(os.path.basename(output_filename))[0]}"
os.makedirs(temp_dir, exist_ok=True)

with zipfile.ZipFile(output_filename, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

top_level_dir = next(os.walk(temp_dir))[1][0]


source_dir = os.path.join(temp_dir, top_level_dir)
destination_dir = os.path.join(os.getcwd(), dir_name)
shutil.move(source_dir, destination_dir)

os.rmdir(temp_dir)

os.remove(output_filename)

download(model_repo=model_repo, output='model')

print("Model bin file download complete")