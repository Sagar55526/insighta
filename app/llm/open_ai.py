import os
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from typing import Optional, Dict, Any
from pydantic import SecretStr
from sqlalchemy import false
from dotenv import load_dotenv

load_dotenv()


class LLMProvider:
    """
    A class that initializes the appropriate LLM (ChatOpenAI or AzureChatOpenAI)
    based on environment variables.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        in_json: bool = False,
        temperature=0.7,
        streaming=False,
    ):
        """
        Initialize the LLM provider.

        Args:
            model_name: The model name to use (defaults to environment variable or fallback)
            temperature: The temperature setting for the model
            **kwargs: Additional arguments to pass to the underlying LLM
        """
        self.use_azure = os.getenv("USE_AZURE_OPENAI", "false").lower() == "true"
        self.llm = self._initialize_llm(model_name, in_json, temperature, streaming)

    def _initialize_llm(
        self,
        model_name: Optional[str],
        in_json: bool,
        temperature: float,
        streaming: bool,
    ) -> ChatOpenAI | AzureChatOpenAI:
        """
        Initialize the appropriate LLM based on environment variables.

        Returns:
            An instance of either ChatOpenAI or AzureChatOpenAI
        """
        if self.use_azure:
            return self._initialize_azure_openai(
                model_name,
                in_json,
                temperature,
                streaming,
            )
        else:
            return self._initialize_openai(
                model_name,
                in_json,
                temperature,
                streaming,
            )

    def _initialize_openai(
        self,
        model_name: Optional[str],
        in_json: bool = False,
        temperature: float = 0.7,
        streaming: bool = False,
    ) -> ChatOpenAI:
        """Initialize a ChatOpenAI instance."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required when using OpenAI"
            )

        model = model_name or os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

        if in_json:
            return ChatOpenAI(
                model=model,
                base_url=os.getenv("OPENAI_ENDPOINT"),
                temperature=temperature,
                api_key=SecretStr(api_key),
                model_kwargs={"response_format": {"type": "json_object"}},
                streaming=streaming,
            )
        else:
            return ChatOpenAI(
                model=model,
                base_url=os.getenv("OPENAI_ENDPOINT"),
                temperature=temperature,
                api_key=SecretStr(api_key),
                streaming=streaming,
            )

    def _initialize_azure_openai(
        self,
        model_name: Optional[str],
        in_json: bool = False,
        temperature: float = 0.7,
        streaming: bool = False,
    ) -> AzureChatOpenAI:
        """Initialize an AzureChatOpenAI instance."""
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "AZURE_OPENAI_API_KEY environment variable is required when using Azure OpenAI"
            )

        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if not azure_endpoint:

            raise ValueError(
                "AZURE_OPENAI_ENDPOINT environment variable is required when using Azure OpenAI"
            )

        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        if not deployment_name:
            raise ValueError(
                "Either model_name parameter or AZURE_OPENAI_DEPLOYMENT_NAME environment variable is required"
            )

        params = {
            "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "deployment_name": model_name or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        }
        if not params["deployment_name"]:
            raise ValueError(
                "Either model_name parameter or AZURE_OPENAI_DEPLOYMENT_NAME environment variable is required"
            )
        if not params["api_key"]:
            raise ValueError(
                "AZURE_OPENAI_API_KEY environment variable is required when using Azure OpenAI"
            )
        if not params["azure_endpoint"]:
            raise ValueError(
                "AZURE_OPENAI_ENDPOINT environment variable is required when using Azure OpenAI"
            )
        if not params["api_version"]:
            raise ValueError(
                "AZURE_OPENAI_API_VERSION environment variable is required when using Azure OpenAI"
            )

        if in_json:
            return AzureChatOpenAI(
                azure_deployment=params["deployment_name"],
                api_version=params["api_version"],
                azure_endpoint=params["azure_endpoint"],
                api_key=SecretStr(params["api_key"]),
                model_kwargs={"response_format": {"type": "json_object"}},
                streaming=streaming,
            )
        else:
            return AzureChatOpenAI(
                azure_deployment=params["deployment_name"],
                api_version=params["api_version"],
                azure_endpoint=params["azure_endpoint"],
                api_key=SecretStr(params["api_key"]),
                streaming=streaming,
            )

    def get_llm(self) -> ChatOpenAI | AzureChatOpenAI:
        """
        Get the initialized LLM instance.

        Returns:
            The initialized LLM (either ChatOpenAI or AzureChatOpenAI)
        """
        return self.llm


if __name__ == "__main__":
    llm_provider = LLMProvider()
    chat_model = llm_provider.get_llm()
    print(f"Initialized LLM: {chat_model}")

    print(
        "Max Tokens:",
        chat_model.max_tokens if hasattr(chat_model, "max_tokens") else "Not Set",
    )
    print(
        "Temperature:",
        (
            chat_model.temperature
            if hasattr(chat_model, "temperature")
            else "Default (0.7)"
        ),
    )
