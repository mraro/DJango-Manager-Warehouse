from googleapiclient.discovery import build
import dotenv
import os

dotenv.load_dotenv()

api_key = os.environ.get("API-GOOGLE-YOUTUBE")


def get_youtube_live_url(channel_name):
    # Replace YOUR_API_KEY with your API key
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Faz uma requisição para buscar o ID do canal
    request = youtube.search().list(q=channel_name, part='id', maxResults=1)

    response = request.execute()
    channel_id = response['items'][0]['id']['channelId']

    # Faz uma segunda requisição para buscar o ID do primeiro vídeo ao vivo no canal
    request = youtube.search().list(
        channelId=channel_id,
        part='id',
        type='video',
        eventType='live',
        maxResults=1
    )

    response = request.execute()
    video_id = response['items'][0]['id']['videoId']

    # O ID do primeiro vídeo ao vivo no canal agora está armazenado na variável `video_id`
    print(f'O ID do primeiro vídeo ao vivo em {channel_name} é {video_id}.')
    return f"https://www.youtube.com/embed/{video_id}"
