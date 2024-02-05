import tkinter as tk
from ToolTip import *
from get_romaji import get_romaji
from translate_text import translate_text

def change_background(event):
    pass

def reset_background(event):
    pass

root = tk.Tk()
font_style = ("Arial", 30)
token_list = ['それ', 'から', 'は', '与え', 'られ', 'た', '新', '事業', 'の', '仕事', 'を', 'こなし', '旦那', '様', 'を', '待ち', '続ける', '日々', '。', 'そうして', '三', '年', 'が', '経ち', '十', '七', '歳', 'で', '結婚', 'し', 'た', '私', 'は', '現在', '二', '十', '歳', 'に', 'なっ', 'て', 'い', 'た']

max_width = 1400
current_width = 0

frame = tk.Frame(root, padx=50, pady=30)

frame.pack()


for token in token_list:
    word_label = tk.Label(frame, text=token, font=font_style)
    word_label.bind("<Enter>", change_background)
    word_label.bind("<Leave>", reset_background)
    word_label.pack(side="left", padx=2)
    CreateToolTip(word_label, text = f'{get_romaji(token)}\n{translate_text(token)}')

    # Check if adding the width of the current word exceeds the maximum width
    current_width += word_label.winfo_reqwidth() + 2  # 2 is for the padx
    if current_width > max_width:
        frame = tk.Frame(root, padx=50, pady=30)
        frame.pack()
        current_width = 0


root.mainloop()

