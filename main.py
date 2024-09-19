import tkinter as tk
from ui import ContactManagerApp

def main():
    root = tk.Tk()
    app = ContactManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()