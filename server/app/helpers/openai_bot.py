import os
import openai
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")

FREEZE_PROMPT = False

PROMPT = """
You are a barista. You are helping a customer get their order. 
Your goal is to generate an order ticket at the end of the conversation. 
You will welcome there into the cafe, and then ask them questions about their order. 
Also, ask their name. When they are done, you must say: 
'Alright! We'll let you know when your order is ready.', followed by a summary order ticket. 

YOU CAN ONLY SPEAK ONE TURN AT A TIME.
Begin by welcoming them into our 'Way of Ikigai' cafe.
"""

DEFAULT_CONVERSATION = {
    "bot_id": "one",
    "bot_type": "openai",
    "topic": "Ordering at the cafe",
    "when": f"{datetime.now().isoformat()}",
    "messages": [
        {
            "role": "system",
            "content": PROMPT,
        },
    ],
}


class OpenAIBot:
    """Stateless bot for open ai"""

    def get_response(self, conversation):
        if conversation.get("messages", []):
            messages = conversation["messages"]
            if FREEZE_PROMPT:
                messages[0] = DEFAULT_CONVERSATION["messages"][0]
            cleaned_up_messages = []
            for i, message in enumerate(messages):
                if i == 0:
                    cleaned_up_messages.append(message)
                else:
                    if message["role"] == "system":
                        pass  # prevent system injection
                    else:
                        cleaned_up_messages.append(message)
            conversation["messages"] = cleaned_up_messages
        else:
            conversation = DEFAULT_CONVERSATION
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=conversation["messages"]
        )
        conversation["when"] = (f"{datetime.now().isoformat()}",)
        response_message = response["choices"][0]["message"]
        print(conversation["messages"], response_message)
        conversation["messages"].append(response_message)
        return conversation
