# EmoLLM 部署指南

## 本地部署

- Clone repo

```bash
git clone https://github.com/aJupyter/EmoLLM.git
```

- 安装依赖

```bash
pip install -r requirements.txt
```

- 下载模型
  - 模型权重：https://openxlab.org.cn/models/detail/jujimeizuo/EmoLLM_Model
  - 通过 openxlab.model.download 下载，详情请看 [cli_internlm2](./cli_internlm2.py)

    ```bash
    from openxlab.model import download

    download(model_repo='jujimeizuo/EmoLLM_Model', output='model')
    ```

  - 可以手动下载，放在 `./model` 目录下，然后把上面的代码删掉

- cli_demo

```bash
python ./demo/cli_internlm2.py
```

- web_demo

```bash
python ./app.py
```

如果在服务器上部署，需要配置本地端口映射

## OpenXLab 上部署

- 登陆 OpenXLab，创建 Gradio 应用

![Login OpenXLab](../assets/deploy_1.png)

- 选择配置，立即创建

![config](../assets/deploy_2.png)

- 等待构建、启动

![wait a minutes](../assets/deploy_3.png)

- 项目体验

![enjoy](../assets/deploy_4.png)