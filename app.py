import customtkinter as ctk
# from CTkColorPicker import *
from tkinter import *
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw, ImageFont
import os
import csv

data_lines = []
colors = [((43, 43, 43), "#2b2b2b"), ((43, 43, 43), "#2b2b2b"), ((43, 43, 43), "#2b2b2b")]
letter_spacing = -10

script_dir = os.path.dirname(os.path.abspath(__file__))


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
    insert_text(result_image, s1, ((width - textLength) / 2, height / 2 - 400 // 2 - 242 / 2), font_path, font_size, text_color1)
    textLength = font.getlength(pronounce) + letter_spacing * (len(s2) - 1)
    insert_text(result_image, pronounce, ((width - textLength) / 2, height / 2 + 400 // 2 - 242 / 2), font_path, font_size, text_color2)


def MakeFile1(result_image, s1, s2, prefix):
    font_path = os.path.join(script_dir, "asset", "NeoExtraBold.ttf")
    font_size = 242
    front_color = "#f3a530"
    back_color = "#f9c87d"

    arrow_color = colors[1][1]
    arrow_color = tuple(int(arrow_color[i:i+2], 16) for i in (1, 3, 5))

    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(result_image)

    width = 2048
    height = 2048
    draw.text(((width)/2, (height)/2), "↕", font=font, fill=arrow_color, anchor='mm')

    global letter_spacing

    s1length = font.getlength(s1) + letter_spacing * (len(s1) - 1)
    s2length = font.getlength(s2) + letter_spacing * (len(s2) - 1)

    prefixLocation = (width - s1length) / 2

    i = 0
    flag = TRUE
    if (s1length >= s2length): 
        x1, y1 = (width - s1length) / 2, height / 2 - 780 // 2 - 242 / 2
        y2 = height / 2 + 780 // 2 - 242 / 2
        for char in s1:
            if prefix[0] == char and flag:
                prefixLocation = x1
                flag = FALSE
            if i < len(prefix) and char == prefix[i]:
                text_color = front_color
                i += 1
            else:
                text_color = back_color
            char_width = draw.textlength(char, font=font)
            draw.text((x1, y1), char, font=font, fill=text_color)
            x1 += char_width + letter_spacing
        i = 0
        for char in s2:
            if i < len(prefix) and char == prefix[i]:
                text_color = front_color
            else:
                text_color = back_color
            i += 1
            char_width = draw.textlength(char, font=font)
            draw.text((prefixLocation, y2), char, font=font, fill=text_color)
            prefixLocation += char_width + letter_spacing
    else:
        x2, y2 = (width - s2length) / 2, height / 2 - 700 // 2 - 242 / 2
        y1 = height / 2 + 780 // 2 - 242 / 2
        for char in s2:
            if prefix[0] == char and flag:
                prefixLocation = x2
                flag = FALSE
            if i < len(prefix) and char == prefix[i]:
                text_color = front_color
            else:
                text_color = back_color
            i += 1
            char_width = draw.textlength(char, font=font)
            draw.text((x2, y2), char, font=font, fill=text_color)
            x2 += char_width + letter_spacing
        i = 0
        for char in s1:
            if i < len(prefix) and char == prefix[i]:
                text_color = front_color
                i += 1
            else:
                text_color = back_color
            char_width = draw.textlength(char, font=font)
            draw.text((prefixLocation, y1), char, font=font, fill=text_color)
            prefixLocation += char_width + letter_spacing


def submitOnClick():
    global data_lines
    width, height = 2048, 2048
    if not data_lines:
        messagebox.showinfo("경고", "파일이 선택되지 않았습니다")
        return


    bg_color = colors[0][1]
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

    text1_color = colors[1][1]
    text2_color = colors[2][1]
    text1_color = tuple(int(text1_color[i:i+2], 16) for i in (1, 3, 5))
    text2_color = tuple(int(text2_color[i:i+2], 16) for i in (1, 3, 5))

    insert_text(result_image, defaultText, position1, font_path, font_size, text1_color)
    
    try:
        for row in data_lines:
            output_folder = os.path.join(script_dir, "result", row[1])
            os.makedirs(output_folder, exist_ok=True)

            new_result_image1 = result_image.copy()
            new_result_image2 = result_image.copy()

            insert_text(new_result_image1, row[0], position2, font_path, font_size, text2_color)
            insert_text(new_result_image2, row[0], position2, font_path, font_size, text2_color)

            MakeFile1(new_result_image1, row[1], row[2], row[4])
            MakeFile2(new_result_image2, row[1], row[3])

            fileName1 = row[1] + "_1.png"
            output_path = os.path.join(output_folder, fileName1)
            new_result_image1.save(output_path)

            fileName2 = row[1] + "_2.png"
            output_path = os.path.join(output_folder, fileName2)
            new_result_image2.save(output_path)
        messagebox.showinfo("성공", "변환 완료")
    except IndexError:
        messagebox.showinfo("실패", "csv 파일 내부 형식이 잘못되었습니다")


app = ctk.CTk()
app.geometry("400x300")
ctk.set_appearance_mode("dark")
app.title("고전어학당 이미지 자동생성")

class fileSegment(ctk.CTkFrame):
    def __init__(self, parent, label_text, button_text, onClickCommand):
        super().__init__(master=parent)

        # grid layout 
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        
        # widgets 
        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.grid(row=0, column=0)

        self.button = ctk.CTkButton(self, text=button_text, command=onClickCommand)
        self.button.grid(row=0, column=1)

        self.fileName = ctk.CTkLabel(self, text="file...", width=150)
        self.fileName.grid(row=0, column=2)

        self.pack(expand=False, fill='both', padx=10, pady=30)


class Segment(ctk.CTkFrame):
    def __init__(self, parent, label_text, button_text, onClickCommand, idx):
        super().__init__(master=parent)

        # grid layout 
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1, 2), weight=1, uniform='a')
        
        # widgets 
        self.label = ctk.CTkLabel(self, text=label_text)
        self.label.grid(row=0, column=0, sticky='nsew')

        self.button = ctk.CTkButton(self, text=button_text, command=onClickCommand)
        self.button.grid(row=0, column=1, sticky='nsew')

        self.colorLabel = ctk.CTkLabel(self, text="", fg_color="#2b2b2b", corner_radius=5)
        self.colorLabel.grid(row=0, column=2, sticky='nsew')

        self.pack(expand=False, fill='both', padx=10, pady=10)

def create_color_callback(index):
    def ask_color():
        global colors
        prev_color = colors[index]
        pick_color = colorchooser.askcolor() # open the color picker
        if pick_color is not None:
            if pick_color[0] is None:  # If user cancels color selection
                colors[index] = prev_color
            else:
                colors[index] = pick_color
            if (index == 0):
                segment1.colorLabel.configure(text=colors[index][1], fg_color=colors[index][1])
            elif (index == 1):
                segment2.colorLabel.configure(text=colors[index][1], fg_color=colors[index][1])
            elif (index == 2):
                segment3.colorLabel.configure(text=colors[index][1], fg_color=colors[index][1])
    return ask_color

def selectFile():
    def openFile():
        global data_lines
        initial_dir = os.path.join(script_dir, "relative_folder")
        filepath = filedialog.askopenfilename(initialdir=initial_dir, filetypes=(("csv files", "*.csv"), ("csv files", "*.CSV")))
        if (filepath):
            segment.fileName.configure(text=filepath)
            with open(filepath, 'r', newline='') as file:
                csv_reader = csv.reader(file)
                data_lines = [[cell.strip() if isinstance(cell, str) else cell for cell in row] for row in csv_reader]
        file.close()
    return openFile

segment = fileSegment(app, "파일 선택", "선택", selectFile())

segment1 = Segment(app, "배경", "선택", create_color_callback(0), 0)
segment2 = Segment(app, "뜻", "선택",  create_color_callback(1), 1)
segment3 = Segment(app, "화살표", "선택", create_color_callback(2), 2)

segment1.button.configure(command=create_color_callback(0))
segment2.button.configure(command=create_color_callback(1))
segment3.button.configure(command=create_color_callback(2))

submitButton = ctk.CTkButton(app, text="제출", command=submitOnClick, width=120)
submitButton.pack(padx=30, pady=20)

app.mainloop()

