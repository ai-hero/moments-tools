from helpers.openai_bot import OpenAIBot


def get_bot(bot_id: str, bot_type: str):
    print(f"Generating openai bot for bot_id: {bot_id} and bot_type: {bot_type}")
    return OpenAIBot()
