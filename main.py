import tkinter as tk
from tkinter import filedialog, font, colorchooser
import webbrowser

class Notepad:
    def __init__(self, master):
        self.master = master
        self.master.title("Notepad")
        self.master.geometry("800x600")

        # Create text widget
        self.text = tk.Text(self.master, undo=True, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=1)

        # Create menu
        menubar = tk.Menu(self.master)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        filemenu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        filemenu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exit)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
        editmenu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
        editmenu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
        editmenu.add_separator()
        editmenu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo)
        editmenu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo)
        menubar.add_cascade(label="Edit", menu=editmenu)

        formatmenu = tk.Menu(menubar, tearoff=0)
        formatmenu.add_command(label="Font", command=self.select_font)
        formatmenu.add_command(label="Color Scheme", command=self.select_color_scheme)
        menubar.add_cascade(label="Format", menu=formatmenu)

        share_menu = tk.Menu(menubar, tearoff=0)
        share_menu.add_command(label="Share on Twitter",
                               command=lambda: self.share_on_social_media("https://twitter.com/intent/tweet?text={}",
                                                                          "Twitter"))
        share_menu.add_command(label="Share on Facebook", command=lambda: self.share_on_social_media(
            "https://www.facebook.com/sharer/sharer.php?u={}", "Facebook"))
        share_menu.add_command(label="Share on LinkedIn", command=lambda: self.share_on_social_media(
            "https://www.linkedin.com/shareArticle?mini=true&url={}", "LinkedIn"))
        menubar.add_cascade(label="Share", menu=share_menu)

        # Bind keyboard shortcuts
        self.master.bind("<Control-n>", lambda event: self.new_file())
        self.master.bind("<Control-o>", lambda event: self.open_file())
        self.master.bind("<Control-s>", lambda event: self.save_file())
        self.master.bind("<Control-S>", lambda event: self.save_file_as())


        # Add menu to master
        self.master.config(menu=menubar)

    def new_file(self):
        self.text.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as f:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, f.read())

    def save_file(self):
        pass # TODO: implement

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.txt')
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.text.get(1.0, tk.END))

    def exit(self):
        self.master.destroy()

    def cut(self):
        self.text.event_generate("<<Cut>>")

    def copy(self):
        self.text.event_generate("<<Copy>>")

    def paste(self):
        self.text.event_generate("<<Paste>>")

    def undo(self):
            self.text.event_generate("<<Undo>>")

    def redo(self):
            self.text.event_generate("<<Redo>>")

    def select_font(self):
        font_name = font.Font(font=self.text['font']).actual()['family']
        font_size = font.Font(font=self.text['font']).actual()['size']
        font_tuple = font.families()
        font_win = tk.Toplevel()
        font_win.title("Font")
        tk.Label(font_win, text="Font Family:").grid(row=0, column=0, padx=5, pady=5)
        font_family_var = tk.StringVar(font_win)
        font_family_var.set(font_name)
        font_family_dropdown = tk.OptionMenu(font_win, font_family_var, *font_tuple)
        font_family_dropdown.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(font_win, text="Font Size:").grid(row=1, column=0, padx=5, pady=5)
        font_size_var = tk.StringVar(font_win)
        font_size_var.set(str(font_size))
        font_size_entry = tk.Entry(font_win, textvariable=font_size_var)
        font_size_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(font_win, text="OK",
                    command=lambda: self.set_font(font_family_var.get(), font_size_var.get())).grid(row=2, column=1,
                                                                                                      padx=5, pady=5)

    def set_font(self, font_family, font_size):
        self.text.configure(font=(font_family, font_size))

    def select_color_scheme(self):
        text_color, bg_color = self.text.cget('fg'), self.text.cget('bg')
        fg_color = colorchooser.askcolor(title="Choose Text Color", initialcolor=text_color)[1]
        if fg_color:
            bg_color = colorchooser.askcolor(title="Choose Background Color", initialcolor=bg_color)[1]
            if bg_color:
                self.text.configure(fg=fg_color, bg=bg_color)

    def share_on_social_media(self, share_url, platform):
        share_text = self.text.get(1.0, tk.END)
        share_url = share_url.format(share_text)
        webbrowser.open(share_url)




root = tk.Tk()
notepad = Notepad(root)
root.mainloop()
