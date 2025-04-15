import click
import json
from pathlib import Path
from typing import Dict, Any
from load_model import load_model
from history_manager import History_Manager
from ask_model import Ask_Model
from database_history import DataBaseHistory
from format_output import format_and_print_history

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
def ask():
    """ask with history"""

    # before ask, show history
    history_manager = History_Manager()
    history_manager.show_session()

    session_id = click.prompt("Please choose or create a new Session ID", prompt_suffix=": ")
    ask_with_history = Ask_Model()

    click.echo("Type 'exit' or 'quit' to end the conversation.")

    while True:
        prompt = click.prompt("\nYou", prompt_suffix=": ")
        if prompt.lower() in ["exit", "quit"]:
            click.echo(f"Conversation ended. Your session ID is: {session_id}")
            break
        
        response = ask_with_history.ask_with_history(session_id=session_id, prompt=prompt)
        click.echo(f"\nAI: {response}")

@cli.command()
@click.option("-d", "--session_id", type=str, help="Please enter the session_id which you want to delete", required=False)
@click.option("-s", "--is_showed", type=str, help="show histories", required=False, is_flag=True)
def history(session_id: str, is_showed: str):
    """operate history in database"""
    history_manager = History_Manager()

    if session_id is not None:
        # delete history in dbase with session_id
        try:
            history_manager.delete(session_id=session_id)

        except:
            click.echo("failed")
        # finally:
            # click.echo("delete completed!")

    if is_showed is not None:
        
        history_manager.show_session()
        

@cli.command()
@click.option("--model-type", prompt="Please choose the model-type", type=click.Choice(["openai", "deepseek"]), default="deepseek")
@click.option("--model-name", prompt="Please enter the model-name (deepseek-chat)", default="deepseek-chat")
@click.option("--api-key", prompt="Please enter your key")
@click.option("--env-file", prompt="环境变量文件路径（存储API密钥）", default=".env")
def init(model_type: str, model_name: str, api_key: str, env_file: str):
    """init the model setting"""
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

    # store the config
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    click.echo(f"setting has stored in {CONFIG_PATH}")

if __name__ == "__main__":

    cli()

