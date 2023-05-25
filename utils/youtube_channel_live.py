from googleapiclient.discovery import build
import dotenv
import os
import requests
import re
import json

dotenv.load_dotenv()

api_key = os.environ.get("API_GOOGLE_YOUTUBE")


def get_api_video_id(channel_name):
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
    try:
        video_id = response['items'][0]['id']['videoId']
        # O ID do primeiro vídeo ao vivo no canal agora está armazenado na variável `video_id`
        print(f'O ID do primeiro vídeo ao vivo em {channel_name} é {video_id}.')

        return video_id
    except IndexError as e:
        print(response, " and ", e)
        return "Nenhum video encontrado"


def get_youtube_live_url(channel_name):
    """ THIS IS OPTIMIZED TO USE API JUST IS NEEDLED """
    # open json file to get last link, if not link get a new

    video_id = None
    try:
        with open('last_url_id.json', 'r') as reading:
            data = json.load(reading)
    except FileNotFoundError:
        data = {}
    if not data.get('video_id'):
        # Replace YOUR_API_KEY with your API key in .env
        video_id = get_api_video_id(channel_name)
        json_data = {'video_id': video_id}
        with open('last_url_id.json', 'w') as json_file:
            json.dump(json_data, json_file)
    else:
        video_id_tested = data['video_id']
        # substitua com o ID do vídeo ao vivo que você deseja verificar
        # video_id = "x_Gb2NaVoKY"

        # faça uma solicitação GET para a página do vídeo ao vivo
        response = requests.get(f"https://www.youtube.com/watch?v={video_id_tested}")

        # analise o HTML da página com a biblioteca BeautifulSoup
        resolution_pattern = re.compile(r'"width":(\d+),"height":(\d+)')
        match = resolution_pattern.search(response.text)

        if match:
            # obtenha a resolução do vídeo a partir dos resultados da expressão regular
            width = match.group(1)
            height = match.group(2)
            video_resolution = f"{width}x{height}"
            print(f"A resolução do vídeo ao vivo é: {video_resolution}")
            if int(width) < 400:
                video_id = get_api_video_id(channel_name)
                json_data = {'video_id': video_id}
                with open('last_url_id.json', 'w') as json_file:
                    json.dump(json_data, json_file)
                    print("Gravado", json_data)
            else:
                video_id = video_id_tested

        else:
            print("Não foi possível encontrar o vídeo ao vivo.")
    return video_id
    # return f"https://www.youtube.com/embed/{video_id}"


if __name__ == '__main__':
    print(get_youtube_live_url("@RITTVOficial"))
