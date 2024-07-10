
from openai import OpenAI

from Secure.models import XpoKey


def GenerateImage(prompt, size="1024x1024", quality="hd"):
    """
        Available Sizes : ['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024']
    """
    if not prompt:
        return None

    key = XpoKey.objects.filter(is_active=True, is_deleted=False).order_by('-token_used')[0]
    client = OpenAI(api_key=key.key)

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        n=1,
    )

    image_url = response.data[0].url
    return image_url