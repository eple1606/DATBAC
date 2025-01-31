import tkinter as tk

def start_gui():
    root = tk.Tk()
    root.title("Wi-Fi Sniffer")
    tk.Label(root, text="Wi-Fi Sniffer Application").pack()
    root.mainloop()
