from PIL import Image, ImageDraw, ImageFont

def test():
    img = Image.new('RGB', (25, 25), color=(73, 109, 137))

    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)
    draw = ImageDraw.Draw(img)
    WIDTH, HEIGHT = (25, 25)
    width, height = draw.textsize("I", font=fnt)
    draw.text(((WIDTH - width) / 2, (HEIGHT - height) / 2), "I", font=fnt, fill="black")
    img.save('answer.png')