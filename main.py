# main.py
import click
from langchain_deepseek import ChatDeepSeek
import json
from pathlib import Path
from typing import Dict, Any

@click.group()
def cli():
    """LangChain CLI"""
    pass

@cli.command()
@click.argument('prompt')
def generate(prompt: str):
    """根据提示生成文本"""

    llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="sk-9ff864592fc641f39fecdab38b1c3474",
    )

    response = llm.invoke(prompt)
    
    click.echo(response.content)

CONFIG_PATH = Path.home() / ".mycli" / "config.json"

@cli.command()
@click.option("--model-type", prompt="Please choose the model-type", type=click.Choice(["openai", "deepseek-chat"]), default="deepseek-chat")
@click.option("--model-name", prompt="模型名称（如 gpt-4）", default="gpt-3.5-turbo")
@click.option("--api-key", prompt="Please enter your key")
@click.option("--env-file", prompt="环境变量文件路径（存储API密钥）", default=".env")
def init(model_type: str, model_name: str, api_key: str, env_file: str):
    """初始化模型配置"""
    config: Dict[str, Any] = {
        "default_model": "default",
        "models": {
            "default": {
                "type": model_type,
                "model_name": model_name,
                "api-key": api_key,
                "env_file": env_file
            }
        }
    }

    # 如果是本地模型（如 Llama），需额外参数
    if model_type == "llama":
        config["models"]["default"]["model_path"] = click.prompt("本地模型路径")

    # 保存配置文件
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    click.echo(f"配置已保存至 {CONFIG_PATH}")

if __name__ == "__main__":
    cli()

