import openai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=os.path.join('secrets', '.env'))

openai.api_key = os.environ['API_KEY']

response = openai.images.generate(
  model = "dall-e-3",
  prompt="a chameleon at a disco",
  size="1024x1024",
  quality = "standard",
  n=1,
  
)
image_url = response.data[0].url

print(image_url)
