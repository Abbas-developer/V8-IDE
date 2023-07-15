from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import filedialog
import os
import sys
import re
import subprocess
path_d=''
folder_file=''
save_open=False
compiler = Tk()
compiler.title('v8-ide')
file_path = ''
editor_font_size = 14
def set_file_path(path):
    global file_path
    file_path = path
    compiler.title(f'bese-08-ide project -name {path_d} file -name {file_path} ')
    save_open = True
def highlight_syntax():
    print("start")
    keywords = ['and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
            'False', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'None',
            'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'True', 'try', 'while', 'with', 'yield',
            'print', 'input', 'int', 'float', 'str', 'list', 'dict', 'set', 'tuple', 'range', 'len',
            'min', 'max', 'sorted', 'reversed', 'enumerate', 'zip', 'sum', 'abs', 'round']
# Loop through each keyword and assign the appropriate color
    # Define the highlighting tags
    editor.tag_configure('keyword', foreground='blue')
    editor.tag_configure('string', foreground='red')
    editor.tag_configure('comment', foreground='green')

    # Get the text from the editor
    code = editor.get('1.0', 'end-1c')

    # Clear all previous tags
    editor.tag_remove('keyword', '1.0', 'end')
    editor.tag_remove('string', '1.0', 'end')
    editor.tag_remove('comment', '1.0', 'end')

    # Define the regular expressions to match
    keyword_regex = '|'.join(keywords)
    string_regex = r'"[^"\\]*(\\.[^"\\]*)*"|\'[^\'\\]*(\\.[^\'\\]*)*\''
    comment_regex = r'#.*'

    # Match and tag the keywords
    for match in re.finditer(r'\b({})\b'.format(keyword_regex), code):
        start = '1.0 + {}c'.format(match.start())
        end = '1.0 + {}c'.format(match.end())
        editor.tag_add('keyword', start, end)

    # Match and tag the strings
    for match in re.finditer(string_regex, code):
        start = '1.0 + {}c'.format(match.start())
        end = '1.0 + {}c'.format(match.end())
        editor.tag_add('string', start, end)

    # Match and tag the comments
    for match in re.finditer(comment_regex, code):
        start = '1.0 + {}c'.format(match.start())
        end = '1.0 + {}c'.format(match.end())
        editor.tag_add('comment', start, end)
def highlight_syntax_event(event=False):
    highlight_syntax()
def open_file_folder():
    save_open = True
    global path_d
    global folder_file
   
    path_d = filedialog.askdirectory()
    floader_file=os.listdir(path_d)
    os.chdir(path_d)
    print(path_d)
    print(floader_file)

def open_file():
    save_open = True
    global path
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)
    highlight_syntax()  # Call the syntax highlighting function here

def save_as():
    global path
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)
    highlight_syntax()  # Call the syntax highlighting function here
def save_as_w(event=False):
    save_as()
def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return
    subprocess.Popen([sys.executable, path], creationflags=subprocess.CREATE_NEW_CONSOLE,)
menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open file', command=open_file)
file_menu.add_command(label='Open folder', command=open_file_folder)

file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)
compiler.bind('<Control-s>', save_as_w)
s_width = compiler.winfo_screenwidth()
s_height = compiler.winfo_screenheight()
# Define the TrieNode class for the Trie data structure
class TrieNode:
    def __init__(self):
        self.children = {}
        self.end_of_word = False

# Define the Trie class
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.end_of_word

    def suggest_completions(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        completions = []
        self._collect_completions(node, prefix, completions)
        return completions

    def _collect_completions(self, node, prefix, completions):
        if node.end_of_word:
            completions.append(prefix)
        for char, child_node in node.children.items():
            self._collect_completions(child_node, prefix + char, completions)

# Initialize the Trie and insert some sample words
trie = Trie()
trie.insert("")
trie.insert("print")
trie.insert("input")
trie.insert("range")
trie.insert("for")
trie.insert("while")
trie.insert("if")
trie.insert("else")
trie.insert("elif")
trie.insert("def")
trie.insert("class")
trie.insert("import")
trie.insert("exec")
trie.insert("True")
trie.insert("False")

# Define the function to handle autocomplete suggestions
def autocomplete(event):
    cursor_pos = editor.index(INSERT)
    line_start = f"{editor.index('insert linestart')} linestart"
    prefix = editor.get(line_start, cursor_pos)
    completions = trie.suggest_completions(prefix)
    if completions:
        editor.delete(line_start, cursor_pos)
        editor.insert(INSERT, completions[0])

# Bind the function to the keypress event
# create a Text widget to display the code editor
editor = Text(compiler, width=s_width, height=s_height)
editor.pack()
editor.bind("<Tab>", autocomplete)
editor.bind('<<Key>>',highlight_syntax_event)

compiler.mainloop()