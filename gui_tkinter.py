import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import scrolledtext
from lexer import tokenize
from parser import Parser
from codegen import generate
import keyword
import re
import threading
import speech_recognition as sr
import time

# Syntax Highlighting Rules
HIGHLIGHT_RULES = {
    "keyword": r"\b(if|else|for|while|return|int|float|char|print)\b",
    "operator": r"[\+\-\*/=]",
    "number": r"\b\d+\b",
    "identifier": r"\b[A-Za-z_][A-Za-z0-9_]*\b"
}

# Real-time Syntax Validation
def validate_syntax(event=None):
    code = input_text.get("1.0", tk.END)
    try:
        tokens = list(tokenize(code))
        Parser(tokens).parse()
        syntax_label.config(text="✅ No syntax errors", fg="lightgreen")
    except Exception as e:
        syntax_label.config(text=f"❌ {str(e)}", fg="red")

# Syntax Highlighting
def highlight(event=None):
    input_text.tag_remove("keyword", "1.0", tk.END)
    input_text.tag_remove("operator", "1.0", tk.END)
    input_text.tag_remove("number", "1.0", tk.END)
    input_text.tag_remove("identifier", "1.0", tk.END)
    for tag, pattern in HIGHLIGHT_RULES.items():
        for match in re.finditer(pattern, input_text.get("1.0", tk.END)):
            start = f"1.0 + {match.start()} chars"
            end = f"1.0 + {match.end()} chars"
            input_text.tag_add(tag, start, end)

# Compile Code
def compile_code():
    code = input_text.get("1.0", tk.END)
    try:
        tokens = list(tokenize(code))
        parser = Parser(tokens)
        tree = parser.parse()
        output = ""
        output += "=== Lexer Output ===\n"
        output += "\n".join([f"{t[0]}: {t[1]}" for t in tokens]) + "\n\n"
        output += "=== Parser Output (AST) ===\n"
        output += "\n".join([str(node) for node in tree]) + "\n\n"
        output += "=== Code Generator Output ===\n"
        output += generate(tree) + "\n"
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, output)
        syntax_label.config(text="✅ Compilation successful!", fg="lightgreen")
        messagebox.showinfo("Success", "Compiled successfully!")
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {str(e)}")
        syntax_label.config(text=f"❌ {str(e)}", fg="red")

# File I/O
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as f:
            content = f.read()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, content)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, 'w') as f:
            f.write(input_text.get("1.0", tk.END))

# Toggle Light/Dark Theme
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#2e2e2e" if dark_mode else "white"
    fg = "white" if dark_mode else "black"
    input_text.config(bg=bg, fg=fg, insertbackground=fg)
    output_text.config(bg=bg, fg=fg, insertbackground=fg)
    root.config(bg=bg)
    syntax_label.config(bg=bg, fg=fg)
    theme_btn.config(text="🌙 Light Mode" if dark_mode else "🌙 Dark Mode")

# Voice Input Control Flag
stop_listening = threading.Event()

# Voice Input Handler
def voice_input():
    def listen_continuous():
        recognizer = sr.Recognizer()
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = True

        voice_btn.config(state="disabled")
        stop_btn.config(state="normal")
        stop_listening.clear()

        def animate():
            while not stop_listening.is_set():
                for state in ["🔴 Listening", "🟠 Listening", "🔴 Listening"]:
                    if stop_listening.is_set():
                        break
                    voice_status.config(text=state, fg="red")
                    time.sleep(0.5)
            voice_status.config(text="🎤 Ready", fg="gray")

        threading.Thread(target=animate, daemon=True).start()

        with sr.Microphone() as source:
            while not stop_listening.is_set():
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
                    text = recognizer.recognize_google(audio).lower()
                    print(f"[Voice]: {text}")

                    if "close" in text:
                        stop_listening.set()
                        break
                    elif "compile" in text:
                        syntax_label.config(text="⚙️ Compiling...", fg="orange")
                        compile_code()
                    elif "open file" in text:
                        open_file()
                    elif "save file" in text:
                        save_file()
                    elif "clear editor" in text:
                        input_text.delete("1.0", tk.END)
                    elif "next" in text:
                        input_text.insert(tk.END, "\n")
                        input_text.see(tk.END)
                    elif "change" in text or "dark mode" in text:
                        toggle_theme()
                    else:
                        input_text.insert(tk.END, text + " ")
                        input_text.see(tk.END)
                        highlight()
                        validate_syntax()
                except sr.UnknownValueError:
                    continue
                except sr.WaitTimeoutError:
                    continue
                except sr.RequestError:
                    messagebox.showerror("Error", "voice speech recognition service failed.")
                    break
                except Exception as e:
                    messagebox.showerror("Error", f"Voice error: {e}")
                    break

        voice_btn.config(state="normal")
        stop_btn.config(state="disabled")
        stop_listening.set()

    threading.Thread(target=listen_continuous, daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("Mini Compiler GUI")
root.geometry("800x600")
try:
    root.iconbitmap("icon.ico")
except:
    pass
root.configure(bg="#444444")

# Main Frame
main_frame = tk.Frame(root, bg="#2e2e2e", bd=4, relief="groove")
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Top Controls
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X, pady=5)

open_btn = tk.Button(top_frame, text="📂 Open", command=open_file)
open_btn.pack(side=tk.LEFT, padx=5)

save_btn = tk.Button(top_frame, text="💾 Save", command=save_file)
save_btn.pack(side=tk.LEFT, padx=5)

theme_btn = tk.Button(top_frame, text="🌙 Dark Mode", command=toggle_theme)
theme_btn.pack(side=tk.LEFT, padx=5)

compile_btn = tk.Button(top_frame, text="⚙️ Compile", command=compile_code)
compile_btn.pack(side=tk.LEFT, padx=5)

voice_btn = tk.Button(top_frame, text="🎤 Voice Input", command=voice_input)
voice_btn.pack(side=tk.LEFT, padx=5)

syntax_label = tk.Label(top_frame, text="Ready", fg="green")
syntax_label.pack(side=tk.RIGHT, padx=10)

stop_btn = tk.Button(top_frame, text="🛑 Stop", command=stop_listening.set, state="disabled")
stop_btn.pack(side=tk.LEFT, padx=5)

voice_status = tk.Label(top_frame, text="🎤 Ready", fg="gray", font=("Arial", 10))
voice_status.pack(side=tk.RIGHT, padx=10)

# Input Box
input_label = tk.Label(root, text="Input Code:")
input_label.pack()
input_text = scrolledtext.ScrolledText(root, height=12, wrap=tk.WORD, undo=True)
input_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

# Output Box
output_label = tk.Label(root, text="Output:")
output_label.pack()
output_text = scrolledtext.ScrolledText(root, height=12, wrap=tk.WORD, state="normal")
output_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

# Highlight Tags
input_text.tag_configure("keyword", foreground="blue")
input_text.tag_configure("operator", foreground="purple")
input_text.tag_configure("number", foreground="darkorange")
input_text.tag_configure("identifier", foreground="green")

input_text.bind("<KeyRelease>", lambda e: [highlight(), validate_syntax()])

# Initial Settings
dark_mode = False
toggle_theme()

root.mainloop()
