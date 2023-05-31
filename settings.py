import os

openai_token = os.getenv("OPENAI_API_KEY")
discord_token = os.getenv("DISCORD_API_KEY")
base_channel_id = int(os.getenv("BASE_CHANNEL_ID"))
channel_category_id = int(os.getenv("CHANNEL_CATEGORY_ID"))
