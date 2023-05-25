# docker build -t pscript . \
#  && docker run -it \
#     -e OPENAI_API_KEY=Secret \
#     -e DISCORD_API_KEY=Secret \
#     -e BASE_CHANNEL_ID=ChannelId \
#     -e CHANNEL_CATEGORY_ID=CategoryId \
#     -v /var/discord-openai-bot/conversations:/app/conversations \
#     discordbot-openai

FROM python:3.11.3-bullseye

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
