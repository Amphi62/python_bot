from PIL import Image, ImageDraw, ImageFont


def test():
    img = Image.new('RGB', (25, 25), color=(73, 109, 137))

    font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)
    draw = ImageDraw.Draw(img)
    WIDTH, HEIGHT = (25, 25)
    width, height = draw.textsize("I", font=font)
    draw.text(((WIDTH - width) / 2, (HEIGHT - height) / 2), "I", font=font, fill="black")
    img.save('answer.png')
