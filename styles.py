#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
styles.py
- Estilos y configuración de la interfaz gráfica
- Tema futurista para el sistema de dispensación biométrica
"""

import tkinter as tk
from tkinter import ttk
from config import *

def setup_futuristic_styles(root):
    """Configura estilos futuristas para la interfaz"""
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    
    # Configurar estilos personalizados básicos
    try:
        style.configure("Futuristic.TLabelframe", 
                       background=BG_MEDIUM, 
                       foreground=ACCENT_BLUE, 
                       borderwidth=2, 
                       relief="solid")
        
        style.configure("Futuristic.TLabelframe.Label", 
                       background=BG_MEDIUM, 
                       foreground=ACCENT_BLUE,
                       font=FONT_LABEL)
        
        style.configure("Futuristic.TButton", 
                       background=BG_LIGHT, 
                       foreground=TEXT_WHITE,
                       borderwidth=2, 
                       relief="solid", 
                       font=FONT_LABEL)
        
        style.configure("Accent.TButton", 
                       background=ACCENT_BLUE, 
                       foreground=BG_DARK,
                       borderwidth=2, 
                       relief="solid", 
                       font=FONT_LABEL)
        
        style.configure("Futuristic.TLabel", 
                       background=BG_MEDIUM, 
                       foreground=TEXT_WHITE,
                       font=FONT_LABEL)
        
        style.configure("Futuristic.Treeview", 
                       background=BG_LIGHT, 
                       foreground=TEXT_WHITE,
                       fieldbackground=BG_LIGHT, 
                       borderwidth=0)
        
        style.configure("Futuristic.Treeview.Heading", 
                       background=ACCENT_BLUE, 
                       foreground=BG_DARK,
                       font=FONT_LABEL)
        
    except Exception as e:
        print(f"⚠️ Advertencia: No se pudieron configurar algunos estilos: {e}")

def create_futuristic_button(parent, text, command, **kwargs):
    """Crea un botón con estilo futurista"""
    btn = tk.Button(parent, text=text, command=command, **kwargs)
    
    # Aplicar estilo base
    btn.configure(
        font=FONT_BUTTON,
        fg=TEXT_WHITE,
        bg=BG_MEDIUM,
        activebackground=BG_LIGHT,
        activeforeground=TEXT_WHITE,
        relief="solid",
        borderwidth=3,
        padx=BUTTON_PADDING_X,
        pady=BUTTON_PADDING_Y,
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT
    )
    
    # Aplicar el estilo futurista con bordes metálicos y efectos de luz
    btn.configure(
        highlightthickness=2,
        highlightbackground=ACCENT_BLUE,
        highlightcolor=ACCENT_CYAN
    )
    
    return btn

def create_small_button(parent, text, command, **kwargs):
    """Crea un botón pequeño con estilo futurista"""
    btn = tk.Button(parent, text=text, command=command, **kwargs)
    
    # Aplicar estilo base
    btn.configure(
        font=FONT_BUTTON_SMALL,
        fg=TEXT_WHITE,
        bg=BG_LIGHT,
        activebackground=ACCENT_BLUE,
        activeforeground=BG_DARK,
        relief="solid",
        borderwidth=2,
        padx=15,
        pady=5
    )
    
    return btn

def create_accent_button(parent, text, command, **kwargs):
    """Crea un botón de acento con estilo futurista"""
    btn = tk.Button(parent, text=text, command=command, **kwargs)
    
    # Aplicar estilo base
    btn.configure(
        font=FONT_BUTTON_SMALL,
        fg=TEXT_WHITE,
        bg=ACCENT_BLUE,
        activebackground=ACCENT_CYAN,
        activeforeground=BG_DARK,
        relief="solid",
        borderwidth=2,
        padx=15,
        pady=5
    )
    
    return btn

def create_danger_button(parent, text, command, **kwargs):
    """Crea un botón de peligro con estilo futurista"""
    btn = tk.Button(parent, text=text, command=command, **kwargs)
    
    # Aplicar estilo base
    btn.configure(
        font=FONT_BUTTON_SMALL,
        fg=TEXT_WHITE,
        bg='#ff4444',
        activebackground='#ff6666',
        activeforeground=TEXT_WHITE,
        relief="solid",
        borderwidth=2,
        padx=15,
        pady=5
    )
    
    return btn

def create_warning_button(parent, text, command, **kwargs):
    """Crea un botón de advertencia con estilo futurista"""
    btn = tk.Button(parent, text=text, command=command, **kwargs)
    
    # Aplicar estilo base
    btn.configure(
        font=FONT_BUTTON_SMALL,
        fg=TEXT_WHITE,
        bg='#ff8800',
        activebackground='#ffaa00',
        activeforeground=TEXT_WHITE,
        relief="solid",
        borderwidth=2,
        padx=15,
        pady=5
    )
    
    return btn

def create_title_label(parent, text):
    """Crea una etiqueta de título con estilo futurista"""
    return tk.Label(parent, text=text, 
                   font=FONT_TITLE, 
                   fg=ACCENT_BLUE, 
                   bg=BG_DARK)

def create_subtitle_label(parent, text):
    """Crea una etiqueta de subtítulo con estilo futurista"""
    return tk.Label(parent, text=text, 
                   font=FONT_SUBTITLE, 
                   fg=ACCENT_CYAN, 
                   bg=BG_DARK)

def create_info_label(parent, text):
    """Crea una etiqueta de información con estilo futurista"""
    return tk.Label(parent, text=text, 
                   font=FONT_LABEL, 
                   fg=ACCENT_CYAN, 
                   bg=BG_DARK)

def create_status_label(parent, text):
    """Crea una etiqueta de estado con estilo futurista"""
    return tk.Label(parent, text=text, 
                   font=FONT_BUTTON_SMALL, 
                   fg=ACCENT_CYAN, 
                   bg=BG_DARK)

def create_main_frame(parent):
    """Crea un frame principal con estilo futurista"""
    frame = tk.Frame(parent, bg=BG_DARK)
    return frame

def create_content_frame(parent):
    """Crea un frame de contenido con estilo futurista"""
    frame = tk.Frame(parent, bg=BG_MEDIUM, relief="solid", borderwidth=2)
    return frame

def create_text_widget(parent, **kwargs):
    """Crea un widget de texto con estilo futurista"""
    text_widget = tk.Text(parent, 
                          wrap="word", 
                          bg=BG_DARK, 
                          fg=ACCENT_CYAN,
                          font=FONT_TEXT, 
                          relief="flat", 
                          borderwidth=0,
                          insertbackground=ACCENT_BLUE, 
                          selectbackground=BG_LIGHT,
                          selectforeground=TEXT_WHITE,
                          **kwargs)
    return text_widget

def create_entry_widget(parent, **kwargs):
    """Crea un widget de entrada con estilo futurista"""
    entry = tk.Entry(parent, 
                     font=FONT_TEXT, 
                     bg=TEXT_WHITE, 
                     fg='#333333', 
                     relief="solid", 
                     borderwidth=2,
                     **kwargs)
    return entry

def create_listbox_widget(parent, **kwargs):
    """Crea un widget de lista con estilo futurista"""
    listbox = tk.Listbox(parent, 
                         bg=BG_DARK, 
                         fg=ACCENT_CYAN,
                         font=FONT_TEXT,
                         selectbackground=BG_LIGHT,
                         selectforeground=TEXT_WHITE,
                         relief="flat", 
                         borderwidth=0,
                         **kwargs)
    return listbox

def create_treeview_widget(parent, columns, **kwargs):
    """Crea un widget de árbol con estilo futurista"""
    tree = ttk.Treeview(parent, 
                        columns=columns, 
                        show="headings", 
                        style="Futuristic.Treeview",
                        **kwargs)
    return tree

def create_scrollbar(parent, orient="vertical", **kwargs):
    """Crea una barra de desplazamiento con estilo futurista"""
    scrollbar = tk.Scrollbar(parent, 
                             orient=orient, 
                             bg=BG_MEDIUM, 
                             troughcolor=BG_DARK, 
                             activebackground=ACCENT_BLUE,
                             **kwargs)
    return scrollbar

def apply_button_hover_effects(button):
    """Aplica efectos de hover a un botón"""
    def on_enter(event):
        button.configure(
            bg=BG_LIGHT,
            highlightbackground=ACCENT_CYAN,
            highlightcolor=ACCENT_CYAN
        )
    
    def on_leave(event):
        button.configure(
            bg=BG_MEDIUM,
            highlightbackground=ACCENT_BLUE,
            highlightcolor=ACCENT_CYAN
        )
    
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

def create_modal_window(parent, title, size):
    """Crea una ventana modal con estilo futurista"""
    modal = tk.Toplevel(parent)
    modal.title(title)
    modal.geometry(size)
    modal.resizable(False, False)
    modal.configure(bg=BG_DARK)
    modal.grab_set()
    modal.focus_set()
    modal.transient(parent)
    
    return modal

def center_window(window):
    """Centra una ventana en la pantalla"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
