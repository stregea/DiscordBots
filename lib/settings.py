from lib.json_reader import read

JSON = read('config/config.json')
IMAGE_API_URL = JSON['api_urls']['open_ai']['image_generator']
CHAT_API_URL = JSON['api_urls']['open_ai']['chat']
API_KEY = JSON['api_tokens']['open_ai']
PREFIX = JSON['commands']['prefix']
IMAGE_COMMAND = JSON['commands']['generate_image']
CHAT_COMMAND = JSON['commands']['chat']
