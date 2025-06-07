"""Configuration for the evaluation utilities."""

import os
from pathlib import Path
from dotenv import load_dotenv


def load_env_file() -> None:
    """Load environment variables from `.env.evaluation` if present."""
    env_file = os.getenv("EVAL_ENV_FILE", ".env.evaluation")
    if os.path.isfile(env_file):
        load_dotenv(env_file)


load_env_file()


class EvalSettings:
    """Settings used by the evaluation scripts."""

    def __init__(self) -> None:
        """Initialize evaluation settings from environment variables."""
        self.EVALUATION_LLM = os.getenv("EVALUATION_LLM", "gpt-4o-mini")
        self.EVALUATION_BASE_URL = os.getenv("EVALUATION_BASE_URL", "https://api.openai.com/v1")
        self.EVALUATION_API_KEY = os.getenv("EVALUATION_API_KEY", "")
        self.EVALUATION_SLEEP_TIME = int(os.getenv("EVALUATION_SLEEP_TIME", "10"))

        # Shared Langfuse credentials
        self.LANGFUSE_PUBLIC_KEY = os.getenv("LANGFUSE_PUBLIC_KEY", "")
        self.LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY", "")
        self.LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

        # Logging configuration
        self.LOG_LEVEL = os.getenv("EVAL_LOG_LEVEL", "INFO")
        self.LOG_FORMAT = os.getenv("EVAL_LOG_FORMAT", "console")
        self.LOG_DIR = Path(os.getenv("EVAL_LOG_DIR", "logs"))


settings = EvalSettings()
