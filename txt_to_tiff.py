# import PIL
from PIL import ImageFont, ImageDraw, Image, ImageOps
import re,os

Image.MAX_IMAGE_PIXELS = 933120000
# 821737572

def main():
    image = text_image('word_ind.txt', "fonts/cour.ttf")
    # image.show()
    image.save('contentok.tiff')

def text_image(text_path, font_path=None):

    grayscale = 'L'
    # parse the file into lines
    with open(text_path,  encoding='utf-8') as text_file:
        lines = tuple(l.rstrip() for l in text_file.readlines())

    large_font = 12
    font_path = font_path or 'cour.ttf'  
    try:
        font = ImageFont.truetype(font_path, size=large_font)
        print("proscessing with selected font")
    except IOError:
        font = ImageFont.load_default()
        print('Could not use chosen font. Using default.')
    pt2px = lambda pt: int(round(pt * 96.0 / 72))
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines) # perfect or a little oversized
    width = int(round(max_width + 5))  # a little oversized

    image = Image.new(grayscale, (width, height))
    draw = ImageDraw.Draw(image)
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 1.0))
    for line in lines:
        # print("processing {}".format(line))
        draw.text((horizontal_position, vertical_position),
                  line, font=font)

        vertical_position += line_spacing
    c_box = ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image

def getSize(txt, font):
    testImg = Image.new('L', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

def pre_txt(txt, text_width=20, text_height=55):
    data = []
    per = []
    with open(txt, "r", encoding="utf8") as target:
        text = re.sub(r'[^\x00-\x7F]+',' ', target.read().rstrip())
        text = " ".join(text.split())
        lines = text.split()
    sisa = len(lines) % text_width
    panjang = int(len(lines)/text_width)
    # print(sisa)
    if sisa != 0:
        panjang = int ((len(lines) - sisa) / text_width + 1)
    # print(panjang)
    tmp_panjang = len(lines) - text_width
    p = text_width
    start = 0
    for i in range(panjang):
        tmp_panjang = tmp_panjang
        if tmp_panjang < 0:
            panjang = sisa

        data.append(lines[start:p])
        tmp_panjang = tmp_panjang - text_width
        p = p + text_width
        start = start + text_width
    sisa = len(data)%text_height
    panjang = int(len(data)/text_height)
    # print(sisa)
    if sisa != 0:
        panjang = int ((len(data) - sisa) / text_height + 1)
    # print(panjang)
    tmp_panjang = len(data) - text_height
    p = text_height
    start = 0
    for i in range(panjang):
        tmp_panjang = tmp_panjang
        if tmp_panjang < 0:
            panjang = sisa

        per.append(data[start:p])
        tmp_panjang = tmp_panjang - text_height
        p = p + text_height
        start = start + text_height
    # print(len(data[1]))
    return (len(data), per)


def make_tiff(text_path):
    lines = []
    text_array = pre_txt(text_path, text_width=15)
    count = 0
    for item in text_array[1]:
        print("generate", count,".tiff")
        generate = generate_tiff(str(count)+".tif", item, fontsize=12)
        # break
        # for i in item:         
            # print(i)
            # pass
        count += 1
     
def generate_tiff(filename, arr,fontdir="fonts", fontname="cour.ttf", fontsize=11):
    fontDir = fontdir+"/"
    fontname = fontname
    outputDir = fontname.split(".")[0]
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)
    fontpath = fontDir+fontname
    colorText = "black"
    colorOutline = "red"
    colorBackground = "white"
    font = ImageFont.truetype(fontname, fontsize)
    pt2px = lambda pt: int(round(pt * 96.0 / 72))
    max_width_line = max(arr[0], key=lambda s: font.getsize(s)[0])
    max_width = pt2px(font.getsize(max_width_line)[0])
    width = int(round(max_width + 5))  # a little oversized

    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    height = max_height * len(arr) # perfect or a little oversized

    img = Image.new("L", (900, 900), colorBackground)
    d = ImageDraw.Draw(img)
    vertical_position = 2
    horizontal_position = 2
    line_spacing = int(round(max_height * 1.0))
    for line in arr:
        # print("processing {}".format(line))
        text = " ".join(line)
        d.text((horizontal_position, vertical_position),
                  text, fill=colorText, font=font)

        vertical_position += line_spacing
    img.save(outputDir+"/"+filename)
    return img

def run(text_path):

    with open(text_path,  encoding='utf-8') as text_file:
    # text = re.sub(r'[^\x00-\x7F]+',' ', l.rstrip())

        lines = tuple(" ".join(re.sub(r'[^\x00-\x7F]+',' ', l.rstrip()).split()) for l in text_file.readlines())
    # print((len(lines)+1)%55)

    fontDir = "fonts/"
    fontname = "cour.ttf"
    outputDir = fontname.split(".")[0]
    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)
    fontname = fontDir+fontname
    fontsize = 11   
    
    colorText = "black"
    colorOutline = "red"
    colorBackground = "white"


    font = ImageFont.truetype(fontname, fontsize)
    pt2px = lambda pt: int(round(pt * 96.0 / 72))
    # max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    # max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines) # perfect or a little oversized
    # width = int(round(max_width + 5))  # a little oversized
    # print(width, height)
    # print(lines)
    # width, height = getSize(text, font)
    img = Image.new("L", (500, 900), colorBackground)
    d = ImageDraw.Draw(img)
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 1.0))
    for line in lines:
        # print("processing {}".format(line))
        d.text((horizontal_position, vertical_position),
                  line, font=font)

        vertical_position += line_spacing
    # d.text((2, height/2), text, fill=colorText, font=font)
    # d.rectangle((0, 0, width+3, height+3), outline=colorOutline)
    # c_box = ImageOps.invert(img).getbbox()
    # img = img.crop(c_box)
    
    img.save("image.tif")
if __name__ == "__main__":
    make_tiff("indo.txt")
    # run("indo.txt")

# text2image --find_fonts --fonts_dir G:\resume\tesstrain\fonts --text G:\resume\tesstrain\langdata\ind\ind.training_text --min_coverage .9  --outputbase G:\resume\tesstrain\langdata\ind\ind 
# |& Select-string raw  | sed -e 's/ :.*/@ \\/g'  | sed -e "s/^/  '/"  | sed -e "s/@/'/g" >G:\resume\tesstrain\langdata\eng\fontslist.txt
    