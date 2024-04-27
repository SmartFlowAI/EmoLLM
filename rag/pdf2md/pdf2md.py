import requests as rq
import json
import os
import zipfile


class PDF2MD:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://api.doc2x.noedgeai.com/api/v1/pdf"
        self.export_url = "https://api.doc2x.noedgeai.com/api/export"

    def convert(self, filepath, to="md"):
        filename = os.path.splitext(os.path.basename(filepath))[0]

        res = rq.post(self.url, files={"file": open(filepath, "rb")},
                      headers={"Authorization": "Bearer " + self.api_key}, stream=True)

        if res.status_code == 200:
            txt_path = filename + ".txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                for line in res.iter_lines():
                    if len(line) > 0:
                        decoded_line = line.decode("utf-8")
                        f.write(decoded_line + "\n")
                        print(decoded_line)

            uuid = json.loads(decoded_line.replace("data: ", ''))['uuid']
            print(uuid)

            if to == "md" or to == 'latex':
                path = filename + '.zip'
            elif to == 'docx':
                path = filename + '.docx'

            export_url = self.export_url + "?request_id=" + uuid + "&to=" + to
            res = rq.get(export_url, headers={"Authorization": "Bearer " + self.api_key})

            if res.status_code == 200:
                with open(path, "wb") as f:
                    f.write(res.content)
                print("下载成功,存入:", path)

                if to == "md" or to == 'latex':
                    zip_file = zipfile.ZipFile(path)

                    # 创建以原始文件名命名的文件夹
                    if not os.path.exists(filename):
                        os.mkdir(filename)

                    # 解压到该文件夹内
                    for names in zip_file.namelist():
                        zip_file.extract(names, filename)
                    zip_file.close()

                    # 找到解压后的md文件
                    for file in os.listdir(filename):
                        if file.endswith(".md"):
                            extracted_md = os.path.join(filename, file)
                            break

                    # 重命名md文件
                    new_md_name = os.path.join(filename, filename + '.md')
                    os.rename(extracted_md, new_md_name)
                    print("解压并重命名md文件为:", new_md_name)

            else:
                print(format("[ERROR] status code: %d, body: %s" % (res.status_code, res.text)))
        else:
            print(format("[ERROR] status code: %d, body: %s" % (res.status_code, res.text)))


def main():
    api_key = "sk-xxx"
    filepath = r"test.pdf"
    converter = PDF2MD(api_key)
    converter.convert(filepath, to="md")


if __name__ == "__main__":
    main()