# Deploying Guide for EmoLLM

## Local Deployment

- Clone repo

```bash
git clone https://github.com/aJupyter/EmoLLM.git
```

- Install dependencies

```bash
pip install -r requirements.txt
```

- Download the model
  - Model weights：https://openxlab.org.cn/models/detail/jujimeizuo/EmoLLM_Model
  - Download via openxlab.model.download, see [cli_internlm2](./cli_internlm2.py) for details

    ```bash
    from openxlab.model import download

    download(model_repo='jujimeizuo/EmoLLM_Model', output='model')
    ```

  - You can also download manually and place it in the `./model` directory, then delete the above code.

- cli_demo

```bash
python ./demo/cli_internlm2.py
```

- web_demo

```bash
python ./app.py
```

If deploying on a server, you need to configure local port mapping.

## Deploy on OpenXLab

- Log in to OpenXLab and create a Gradio application

![Login OpenXLab](../assets/deploy_1.png)

- Select configurations and create the project

![config](../assets/deploy_2.png)

- Wait for the build and startup

![wait a minutes](../assets/deploy_3.png)

- Try your own project

![enjoy](../assets/deploy_4.png)