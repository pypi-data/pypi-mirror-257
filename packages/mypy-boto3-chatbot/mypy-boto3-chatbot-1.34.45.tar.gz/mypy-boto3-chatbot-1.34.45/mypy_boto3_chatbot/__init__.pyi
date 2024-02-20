"""
Main interface for chatbot service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_chatbot import (
        Client,
        chatbotClient,
    )

    session = Session()
    client: chatbotClient = session.client("chatbot")
    ```
"""

from .client import chatbotClient

Client = chatbotClient

__all__ = ("Client", "chatbotClient")
