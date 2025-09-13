# Just a wrapper, actual functionality is carried out by core() function in the main.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading, webbrowser, time
from main import core


def insert_hyperlink(text_widget, url):
    def open_link(event):
        webbrowser.open_new(url)

    start = text_widget.index(tk.INSERT)
    text_widget.insert(tk.INSERT, url)
    end = text_widget.index(tk.INSERT)
    text_widget.tag_add("link", start, end)
    text_widget.tag_config("link", foreground="blue", underline=1)
    text_widget.tag_bind("link", "<Button-1>", open_link)


def run_scraper():
    query = entry.get().strip()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a course query!")
        return

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"🔍 Searching for playlist: {query}...\n")

    # Enable indeterminate mode for progress bar
    progress_bar.start()

    def task():
        try:
            title, creator, url, texts, result = core(query)

            # Stop the progress bar after scraping is done
            progress_bar.stop()

            output_box.insert(tk.END, f"\n🎵 Top Playlist Name: {title}")
            output_box.insert(tk.END, f"\n👤 Creator: {creator}")
            output_box.insert(tk.END, f"\n🔗 URL: ")
            insert_hyperlink(output_box, url)
            output_box.insert(tk.END, "\n")

            output_box.insert(tk.END, f"\n📺 Total number of videos: {len(texts)}")
            output_box.insert(tk.END, f"\n⏳ Total Duration: {result} hours\n")

            output_box.insert(tk.END, "\n📝 Video Durations:\n")
            for t in texts[:15]:  # show first 15 only
                output_box.insert(tk.END, f"{t}\n")

            if len(texts) > 15:
                output_box.insert(tk.END, f"... and {len(texts) - 15} more.\n")

        except Exception as e:
            progress_bar.stop()
            # Popup for actual exception
            messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

            # Friendly message in the output box
            output_box.delete(1.0, tk.END)
            output_box.insert(tk.END, "❌ Sorry, there was a problem.\n")
            output_box.insert(tk.END, "👉 Kindly check your input or try searching for some other query.\n")

    threading.Thread(target=task).start()


# -------------------- GUI -------------------- #
root = tk.Tk()
root.title("📚 CourseFinder – Saami Abbas Khan.")
root.geometry("520x750")
root.configure(bg="#f8f9fa")

# Load image
img = tk.PhotoImage(file="images/books.png")

# Create background label
bg_label = tk.Label(root, image=img)
bg_label.place(relwidth=1, relheight=1)  # fill the whole window

# --------------------------------------------------
style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 12), padding=6)
style.configure("TEntry", padding=4)

# Title
title_label = tk.Label(root, text="📚 Yt-CourseFinder",
                       font=("Segoe UI", 18, "bold"), bg="#f8f9fa", fg="#d32f2f")
title_label.pack(pady=15)

# Input Frame
frame = tk.Frame(root, bg="#f8f9fa")
frame.pack(pady=10)

label = tk.Label(frame, text="Enter your course query:",
                 font=("Segoe UI", 12), bg="#f8f9fa")
label.pack(side=tk.LEFT, padx=5)

entry = ttk.Entry(frame, width=30, font=("Segoe UI", 11))
entry.pack(side=tk.LEFT, padx=5)

run_btn = ttk.Button(root, text="Run", command=run_scraper)
run_btn.pack(pady=10)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="indeterminate", length=400)
progress_bar.pack(pady=5)

# Output box
output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD,
                                       width=60, height=25, font=("Consolas", 10))
output_box.pack(padx=10, pady=10)

root.mainloop()
