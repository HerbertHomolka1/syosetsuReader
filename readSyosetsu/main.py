import tkinter as tk
from get_syosetsu_paragraph_list_from_url import get_syosetsu_paragraph_list_from_url 
from translate_text import translate_text
from get_romaji import get_romaji
from consts import *
from ToolTip import *
from get_romaji import get_romaji
from translate_text import translate_text
from tokenize_japanese_sentence import tokenize_japanese_sentence
from tkinter import ttk
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from janome.tokenizer import Tokenizer
import janome

Base = declarative_base()

class UrlDatabase(Base):
    __tablename__ = 'urls'
    id = Column(Integer, Sequence('url_id_seq'), primary_key=True)
    novel_name = Column(String(255))
    novel_url = Column(String(255))
    chapter = Column(Integer())
    index = Column(Integer())

# Replace 'sqlite:///your_database.db' with the actual path to your SQLite database file
database_url = 'sqlite:///novel_database.db'

engine = create_engine(database_url, echo=True)

# Automatically create the database tables
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

def get_url(url):
    global chapter
    if url[-1] != '/':
        url = url+'/'
    print(chapter)
    return  f'{url}{chapter}'

def get_paragraph_text_list():
    r = get_syosetsu_paragraph_list_from_url(get_url(url))
    print('get_paragraph_text_list',len(r))
    return r

def update_all_labels():
        global paragraph_text_list
        paragraph_text_list = get_paragraph_text_list()
        print('update_all_labels: ', len(paragraph_text_list))
        text = paragraph_text_list[index]
        translation_label.config(text=get_romaji(text))
        chapter_label.config(text=f'{index}/{len(paragraph_text_list)-1}\nchapter: {chapter}', background='lightgray') 
        # chapter_label.config(text=f'chapter: {chapter}')
        remove_all_frames()
        create_paragraph_label(text)


def add_aniki_flashcard(event):
    # first, install aniki on here. Then we'll see how to scrip adding new flashcards.
    pass

def create_paragraph_label(text):
    font_size = 30
    font_style = ("Helvetica", font_size)
    max_width = 1300
    current_width = 0
    frame = tk.Frame(root, padx=50, pady=10, background='lightgray')
    frame.pack()
    token_list = tokenize_japanese_sentence(text)

    for token in token_list:
        word_label = tk.Label(frame, text=token, font=font_style, background='lightgray')
        word_label.pack(side="left", padx=2)
        CreateToolTip(word_label, text = f'{token}')

        current_width += word_label.winfo_reqwidth() + 2  
        if current_width > max_width:
            frame = tk.Frame(root, padx=50, pady=10, background='lightgray')
            frame.pack()
            current_width = 0


def on_h_key(event):
    global index
    global chapter
    if chapter > 1:
        chapter -= 1
        index = 0
        update_all_labels()


def on_l_key(event):
    global index
    global chapter
    chapter += 1
    index = 0
    update_all_labels()
    print(len(paragraph_text_list),chapter)

def on_t_key(event):
    global index
    global toggle
    text = paragraph_text_list[index]
    if toggle:
        text = get_romaji(text)
    else:
        text = translate_text(text)
    translation_label.config(text=text)
    toggle = not toggle
    
def remove_all_frames():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

def on_k_key(event):
    global index
    global paragraph_text_list
    print('on_k_key',len(paragraph_text_list))
    if index < len(paragraph_text_list)-1:
        index+=1
        text = paragraph_text_list[index]
        translation_label.config(text=get_romaji(text))
        remove_all_frames()
        create_paragraph_label(text)
        chapter_label.config(text=f'{index}/{len(paragraph_text_list)-1}\nchapter: {chapter}',background='lightgray') 

def on_j_key(event):
    global index
    global paragraph_text_list
    if index >=1:
        index-=1
        text = paragraph_text_list[index]
        translation_label.config(text=get_romaji(text))
        remove_all_frames()
        create_paragraph_label(text)
        chapter_label.config(text=f'{index}/{len(paragraph_text_list)-1}\nchapter: {chapter}', background='lightgray') 


def create_gui(URL,CHAPTER,INDEX):
    print('create_gui: CHAPTER,INDEX ',CHAPTER,INDEX)
    global url 
    url = URL
    global translation_label
    global chapter_label
    global root
    global paragraph_text_list
    global chapter
    chapter = int(CHAPTER)
    global index
    index = int(INDEX)

    print('create_gui: chapter,index ',url,chapter,index)

    paragraph_text_list = get_paragraph_text_list()
    initial_paragraph_text = paragraph_text_list[index]

    root = tk.Tk() 
    root.configure(background='lightgray')
    root.title("Syosetsu Reader")
    root['padx'] = 100
    root['pady'] = 50

    root.geometry("{}x{}".format(WIDTH, HEIGHT))

    font_size = 30
    font_style = ("Helvetica", font_size)
    font_size_translation = 18
    font_style_translation = ("Helvetica", font_size_translation)

    translation_label = tk.Label(root, text=get_romaji(initial_paragraph_text), justify="left", wraplength=1400, font=font_style_translation, background='lightgray')
    translation_label.pack(padx=20, pady=20)

    create_paragraph_label(initial_paragraph_text)
    
    chapter_label = tk.Label(root, text=f'{index}/{len(paragraph_text_list)-1}\nchapter: {chapter}', font=font_size_translation, background='lightgray')
    
    # chapter_label = tk.Label(root, text=f'chapter: {chapter}', font=font_size_translation, background='lightgray')
    chapter_label.place(relx=1, rely=1, anchor='se')

    root.bind('k', on_k_key)
    root.bind('<Down>',on_k_key)
    root.bind('j', on_j_key)
    root.bind('<Up>', on_j_key)
    root.bind('t',on_t_key)
    root.bind('<space>',on_t_key)
    root.bind('h', on_h_key)
    root.bind('<Left>', on_h_key)
    root.bind('l',on_l_key)
    root.bind('<Right>',on_l_key)


    def on_closing():
        with Session() as session:
            entry_to_modify = session.query(UrlDatabase).filter_by(novel_url=URL).first()
            entry_to_modify.chapter = chapter
            entry_to_modify.index = index
            session.commit()
            quit()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

def read_selected_novel():
    selected_item = novels_tree.selection()

    if selected_item:
        values = novels_tree.item(selected_item, "values")
        print('read_selected_novel: values ',values)
        print('read_selected_novel: chapter,index',values[2],values[3])
        create_gui(values[1],values[2],values[3]) # ('villainess healer', 'https://ncode.syosetu.com/n3704he/1', 2nd chapter, 41st paragraph)
    else:
        print("Choose something.")

def add_novel_to_database(novel_name,novel_url, chapter, index):
    if novel_name and novel_url:
        add_novel(novel_name,novel_url, chapter, index)
        with Session() as session:
            new_novel = UrlDatabase(novel_url=novel_url, novel_name=novel_name, chapter = chapter, index=index  )
            session.add(new_novel)
            session.commit()
    else:
        print("Please enter both novel name and URL.")

def add_novel(novel_name,novel_url,chapter=1, index=0):
        novels_tree.insert("", "end", values=(novel_name, novel_url,chapter,index))
        # Clear the entry fields after adding a novel
        novel_name_entry.delete(0, 'end')
        novel_url_entry.delete(0, 'end')

def read_novel_urls_from_database():
    with Session() as session:
        novels = session.query(UrlDatabase).all()
        novels = [(novel.novel_name,novel.novel_url,novel.chapter, novel.index) for novel in novels]
        return novels

def create_novel_selection():
    global novel_name_entry
    global novel_url_entry
    global novels_tree
 
    root1 = tk.Tk()
    root1.title("Syosetsu Reader")

    Label(text="Name of your novel", width=25).grid(row=0, column=0)
    Label(text="URL to Ch1 of your novel", width=25).grid(row=1, column=0)

    novel_name_entry = Entry(root1, bd=1, width = 80)
    novel_name_entry.grid(row=0, column=1)

    novel_url_entry = Entry(root1, bd=1, width = 80)
    novel_url_entry.grid(row=1, column=1)

    add_novel_button = Button(root1, text="Add Novel", width=105, height=1, bd=1,command=lambda: add_novel_to_database(novel_name_entry.get(),novel_url_entry.get(),1,0))
    add_novel_button.grid(row=2, column=0, columnspan=2,pady=4)

    style = ttk.Style()
    style.configure("Treeview", rowheight=40)  


    novels_tree = ttk.Treeview(root1, columns=("Novel Name", "Novel URL",'Chapter','Paragraph'), show="headings")
    novels_tree.heading("Novel Name", text="Novel Name")
    novels_tree.heading("Novel URL", text="Novel URL")
    novels_tree.heading("Chapter", text="Chapter")
    novels_tree.heading("Paragraph", text="Paragraph")
    novels_tree.column("Novel Name", width=400)  
    novels_tree.column("Novel URL", width=900)  
    novels_tree.column("Chapter", width=150)  
    novels_tree.column("Paragraph", width=150)  
    novels_tree.grid(row=3, column=0, columnspan=2)
    
    novels_in_database = read_novel_urls_from_database()

    for novel in novels_in_database:
        add_novel(novel[0],novel[1],novel[2],novel[3])

    read_novel_button = Button(root1, text="Read Novel", width=105, height=2, bd=1,command=read_selected_novel)
    read_novel_button.grid(row=4, column=0, columnspan=2,pady=8)

    root1.mainloop()

# create_gui()
create_novel_selection()