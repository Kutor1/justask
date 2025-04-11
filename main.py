import click
import json
from pathlib import Path
from typing import Dict, Any
from load_model import load_model
from history_manager import History_Manager
from ask_model import Ask_Model
from langchain_core.runnables import (
    RunnableLambda,
    ConfigurableFieldSpec,
    RunnablePassthrough,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
CONFIG_PATH = Path.home() / ".mycli" / "config.json"

@click.group()
def cli():
    """LangChain CLI"""
    pass

@cli.command()
@click.argument('prompt')
def oask(prompt: str):
    """once ask, simple ask"""
    once_ask = Ask_Model()
    response = once_ask.once_ask(prompt=prompt)

    click.echo(response)

@cli.command()
@click.option("--session_id", prompt="Please choose/create a history id")
@click.argument('prompt')
def ask(session_id: str ,prompt: str):
    """ask with history"""
    
    # ask_with_history = Ask_Model()
    # response = ask_with_history.ask_with_history(session_id=session_id, prompt=prompt)
    
    # click.echo(response)
    ask_with_history = Ask_Model()
    click.echo(f"Session ID: {session_id}")
    click.echo("Type 'exit' or 'quit' to end the conversation.")

    while True:
        prompt = click.prompt("\nYou", prompt_suffix=": ")
        if prompt.lower() in ["exit", "quit"]:
            click.echo(f"Conversation ended. Your session ID is: {session_id}")
            break
        
        response = ask_with_history.ask_with_history(session_id=session_id, prompt=prompt)
        click.echo(f"\nAI: {response}")

@cli.command()
@click.option("--model-type", prompt="Please choose the model-type", type=click.Choice(["openai", "deepseek"]), default="deepseek")
@click.option("--model-name", prompt="Please enter the model-name (deepseek-chat)", default="deepseek-chat")
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

    # 保存配置文件
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    click.echo(f"配置已保存至 {CONFIG_PATH}")

if __name__ == "__main__":

    cli()

