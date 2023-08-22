import customtkinter as ctk
from CTkColorPicker import *
from tkinter import *
from tkinter import filedialog
from tkinter import colorchooser
from PIL import Image, ImageDraw, ImageFont
import os
import csv


app = ctk.CTk()
ctk.set_appearance_mode("dark")
app.geometry("800x600")
app.title("고전어학당 이미지 자동생성")
data_lines = []
colors = ["", "", ""]
letter_spacing = -10

script_dir = os.path.dirname(os.path.abspath(__file__))

def openFile():
    global data_lines
    initial_dir = os.path.join(script_dir, "relative_folder")

    filepath = filedialog.askopenfilename(initialdir=initial_dir, filetypes=(("csv files", "*.csv"), ("csv files", "*.CSV")))
    if (filepath):
        fileStr.set(filepath)
        with open(filepath, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            data_lines = [[cell.strip() if isinstance(cell, str) else cell for cell in row] for row in csv_reader]
    file.close()


def insert_text(image, text, position, font_path, font_size, text_color):
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(image)

    global letter_spacing

    x, y = position
    for char in text:
        char_width = draw.textlength(char, font=font)
        draw.text((x, y), char, font=font, fill=text_color)
        x += char_width + letter_spacing

def MakeFile2(result_image, s1, s2):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    font_path = os.path.join(script_dir, "asset", "NeoExtraBold.ttf")
    font_size = 242
    pronounce = "[" + s2 + "]"
    text_color1 = "#f3a530"
    text_color2 = "#f9c87d"

    global letter_spacing

    width, height = result_image.size

    font = ImageFont.truetype(font_path, font_size)
    textLength = font.getlength(s1) + letter_spacing * (len(s1) - 1)
    print(textLength, (width - textLength) / 2)
    insert_text(result_image, s1, ((width - textLength) / 2, height / 2 - 400 // 2 - 242 / 2), font_path, font_size, text_color1)
    textLength = font.getlength(pronounce) + letter_spacing * (len(s2) - 1)
    insert_text(result_image, pronounce, ((width - textLength) / 2, height / 2 + 400 // 2 - 242 / 2), font_path, font_size, text_color2)

def MakeFile1(result_image, s1, s2, prefix):
    font_path = os.path.join(script_dir, "asset", "NeoExtraBold.ttf")
    font_size = 242
    front_color = "#f3a530"
    back_color = "#f9c87d"

    arrow_color = colors[1]
    arrow_color = tuple(int(arrow_color[i:i+2], 16) for i in (1, 3, 5))

    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(result_image)

    width = 2048
    height = 2048
    draw.text(((width)/2, (height)/2), "↕", font=font, fill=arrow_color, anchor='mm')

    s1length = font.getlength(s1)
    s2length = font.getlength(s2)

    i = 0
    if (s1length >= s2length): 
        x1, y1 = (width - s1length) / 2, height / 2 - 700 // 2 - 242 / 2
        for char in s1:
            if char == prefix[i]:
                text_color = front_color
            else:
                text_color = back_color
            char_width = draw.textlength(char, font=font)
            x1 += char_width + letter_spacing
            if i < len(prefix):
                i += 1
        x2, y2 = (width - s1length) / 2, height / 2 + 700 // 2 - 242 / 2

    # else:
    #     x1, y1 = (width - s2length) / 2, height / 2 - 700 // 2 - 242 / 2
    #     for char in s1:
    #         char_width = draw.textlength(char, font=font)
    #         x1 += char_width + letter_spacing
    #     x2, y2 = (width - s2length) / 2, height / 2 + 700 // 2 - 242 / 2


def submitOnClick():
    global data_lines
    width, height = 2048, 2048
    bg_color = colors[0]
    background_color_rgb = tuple(int(bg_color[i:i+2], 16) for i in (1, 3, 5))

    background_image_path = os.path.join(script_dir, "asset", "bg_image.png")

    background_image = Image.open(background_image_path).convert("RGBA")
    background_image = background_image.resize((width, height)) 

    image2_path = os.path.join(script_dir, "asset", "CA_logo_ko_in_template.png")
    logo = Image.open(image2_path)

    result_image = Image.new("RGBA", (width, height), background_color_rgb)

    alpha_channel = background_image.getchannel("A")

    result_image.paste(background_image, (0, 0), alpha_channel)
    result_image.paste(logo, (820, 1850), logo)

    defaultText = "라틴어 ↔ 영어"
    position1 = (90, 90)
    position2 = (90, 220)

    font_path = os.path.join(script_dir, "asset", "NeoHeavy.ttf")
    font_size = 93

    text1_color = colors[1]
    text2_color = colors[2]
    text1_color = tuple(int(text1_color[i:i+2], 16) for i in (1, 3, 5))
    text2_color = tuple(int(text2_color[i:i+2], 16) for i in (1, 3, 5))

    insert_text(result_image, defaultText, position1, font_path, font_size, text1_color)

    for row in data_lines:
        output_folder = os.path.join(script_dir, "result", row[1])
        os.makedirs(output_folder, exist_ok=True)

        new_result_image1 = result_image.copy()
        new_result_image2 = result_image.copy()

        insert_text(new_result_image1, row[0], position2, font_path, font_size, text2_color)
        insert_text(new_result_image2, row[0], position2, font_path, font_size, text2_color)

        MakeFile1(new_result_image2, row[1], row[2], row[4])
        # MakeFile2(new_result_image2, row[1], row[3])

        # fileName1 = row[1] + "_1.png"
        # output_path = os.path.join(output_folder, fileName1)
        # new_result_image1.save(output_path)

        # fileName2 = row[1] + "_2.png"
        # output_path = os.path.join(output_folder, fileName2)
        # new_result_image2.save(output_path)
        # print("텍스트 삽입 완료")



fileOpenButton = ctk.CTkButton(app, text="Open", command=openFile)
fileOpenButton.pack()

fileStr=StringVar()
fileLabel = ctk.CTkLabel(app, textvariable=fileStr)
fileStr.set("file...")
fileLabel.pack()

# def ask_color(button, index):
#     pick_color = AskColor()  # open the color picker
#     my_color = pick_color.get()  # get the color string
#     if my_color is not None:
#         colors[index] = my_color
#     button.configure(fg_color=my_color)

# # 앱을 생성하고 초기화하는 코드 (생략)

# bgColorButton = ctk.CTkButton(app, text="배경", command=lambda: ask_color(bgColorButton, 0))
# bgColorButton.pack(padx=30, pady=20)

# meanColorButton = ctk.CTkButton(app, text="뜻 색", command=lambda: ask_color(meanColorButton, 1))
# meanColorButton.pack(padx=30, pady=20)

# arrowColorButton = ctk.CTkButton(app, text="화살표색", command=lambda: ask_color(arrowColorButton, 2))
# arrowColorButton.pack(padx=30, pady=20)

# submitButton = ctk.CTkButton(app, text="제출", command=submitOnClick)
# submitButton.pack(padx=30, pady=20)


def color(index):
    global colors 
    my_color = colorchooser.askcolor()
    if my_color[1] is not None: 
        colors[index] = my_color[1]  
        update_label() 

def update_label():
    colors_str = ", ".join(colors)
    my_label.config(text=f"Selected Colors: {colors_str}")

for i in range(3):
    button = Button(app, text=f"Choose Color {i+1}", command=lambda i=i: color(i))
    button.pack(pady=10)

my_label = Label(app, text="Selected Colors:")
my_label.pack()

button = Button(app, text="제출", command=submitOnClick)
button.pack()

app.mainloop()

