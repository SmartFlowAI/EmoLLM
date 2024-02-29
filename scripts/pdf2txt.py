import os
import sys
import glob
try:
    import  cv2
except :
    os.system('pip install opencv-python')
    import  cv2
try :
    from  paddleocr  import  PaddleOCR ,  draw_ocr ,  download_with_progressbar 
except:
    os.system('pip install paddleocr')
    from  paddleocr  import  PaddleOCR ,  draw_ocr ,  download_with_progressbar 
output_folder_path = 'res/'
if not os.path.exists(output_folder_path):  
    os.makedirs(output_folder_path) 

def get_pdf_files_in_directory(directory_path):  
    # 确保路径存在
    if os.path.exists(directory_path) and os.path.isdir(directory_path):  
        return glob.glob(os.path.join(directory_path, '**', '*.pdf'), recursive=True)
    else:  
        return []  
def ocr_pdf_folder(folder_path):
    ocr  =  PaddleOCR ( use_angle_cls = True ,  lang = "ch" , page_num = 0 )   # 只需运行一次即可将模型下载并加载到内存中
    print("ppocrv4 加载完毕！！！")
    pdf_paths = get_pdf_files_in_directory(folder_path)
    print(f"共检测到 {len(pdf_paths)} 个PDF文件")
    # 打印所有PDF文件的路径
    for pdf_path in pdf_paths:  
        print(f'正在处理文件：{pdf_path}')

        result = ocr.ocr (pdf_path , cls = True )
        for idx in range(len(result)): 
            res = result[idx] 
            for line in res : 
                print(line)
        print(f'{pdf_path} 处理完毕')
        ocr_result = ""
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
        #         print(line[1][0])
                ocr_result = f"{ocr_result} {str(line[1][0])}"

        filename = os.path.splitext(os.path.basename(pdf_path))[0]  

        # 构建TXT文件的完整路径
        txt_path = os.path.join('res/', f'{filename}.txt')  

        # 将提取的文本写入TXT文件  
        with open(txt_path, 'w', encoding='utf-8') as txt_file:  
            txt_file.write(ocr_result)  

        print(f'生成的txt文档保存在{txt_path}')
        #         break
        # print(ocr_result)
        # with open('my_file.txt', 'a') as f:  
        #     # 写入字符串  
        #     f.write(ocr_result)


if __name__ == "__main__":  
    if len(sys.argv) > 1:  
        # sys.argv[0] 是脚本名，sys.argv[1:] 是传递给脚本的参数列表  
        pdf_path = sys.argv[1]  
        print(f'需要处理的文件夹是：{pdf_path}')
        ocr_pdf_folder(pdf_path)
    