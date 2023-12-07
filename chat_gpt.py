import os

from openai import OpenAI

GPT_VERSION = "gpt-3.5-turbo"


class ChatGPT:
    """A class to interact with OpenAI's ChatGPT model."""

    def __init__(self):
        self.openapi_client = OpenAI(
            # defaults to os.environ.get("OPENAI_API_KEY")
            # or you can explicitly pass in the key (NOT RECOMMENDED)
            api_key=os.getenv("OPENAI_KEY"),
        )

    def request_openai(self, messages):
        """
        Make a request to the OpenAI API.

        Args:
        - message (str): The message to be sent to the OpenAI API.
        - role (str, optional): The role associated with the message. Defaults to "system".

        Returns:
        - str: The response content from the OpenAI API.
        """

        # Create a chat completion with the provided message and role
        response = self.openapi_client.chat.completions.create(
            model=GPT_VERSION,
            messages=messages
        )

        print(response)
        return response.model_dump()["choices"][0]["message"]["content"]
