from pathlib import Path
import json
from langchain_openai import ChatOpenAI
from langchain_deepseek import ChatDeepSeek
CONFIG_PATH = Path.home() / ".mycli" / "config.json"


def load_model(config_name: str = "default"):

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    
    llm = None

    model_config = config["models"][config_name]
    model_type = model_config["type"]
    api_key = model_config["api-key"]

    if model_type == "deepseek-chat":
            llm = ChatDeepSeek(
                model=model_type,
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=api_key,
            )

    return llm

if __name__ == "__main__":
    load_model()