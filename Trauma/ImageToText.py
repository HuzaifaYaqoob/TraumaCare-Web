import easyocr


class ImageToText:
    def __init__(self, image):
        self.image = image

    def get_text(self):
        reader = easyocr.Reader(['en']) # specify the language  
        result = reader.readtext(self.image)
        
        # print(result)
        imageText = ''
        for (bbox, text, prob) in result:
            # print(f'Text: {text}, Probability: {prob}')
            imageText += f'{text} '
        
        return imageText