import os
import sys
import pytest
import asyncio
from typing import Optional
from unittest.mock import patch, AsyncMock

sys.path.insert(0, os.path.abspath("../.."))
import litellm
from litellm.integrations.custom_logger import CustomLogger
import json
from litellm.types.utils import StandardLoggingPayload
from litellm.types.llms.openai import (
    ResponseCompletedEvent,
    ResponsesAPIResponse,
    ResponseTextConfig,
    ResponseAPIUsage,
    IncompleteDetails,
)
from litellm.llms.custom_httpx.http_handler import AsyncHTTPHandler
from base_responses_api import BaseResponsesAPITest

class TestAzureResponsesAPITest(BaseResponsesAPITest):
    def get_base_completion_call_args(self):
        return {
            "model": "azure/computer-use-preview",
            "truncation": "auto",
            "api_base": os.getenv("AZURE_RESPONSES_OPENAI_ENDPOINT"),
            "api_key": os.getenv("AZURE_RESPONSES_OPENAI_API_KEY"),
            "api_version": os.getenv("AZURE_RESPONSES_OPENAI_API_VERSION"),
        }


@pytest.mark.asyncio
async def test_azure_responses_api_preview_api_version():
    """
    Ensure new azure preview api version is working
    """
    litellm._turn_on_debug()
    response = await litellm.aresponses(
        model="azure/computer-use-preview",
        truncation="auto",
        api_version="preview",
        api_base=os.getenv("AZURE_RESPONSES_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_RESPONSES_OPENAI_API_KEY"),
        input="Hello, can you tell me a short joke?",
    )