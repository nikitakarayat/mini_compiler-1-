import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear()
    print("==== Mini Compiler Launcher ====\n")
    print("Choose a mode:")
    print("1. Command-Line Compiler")
    print("2. GUI (Tkinter)")
    print("3. Web UI (Flask)")
    print("4. Exit")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == '1':
        os.system("python main.py")
    elif choice == '2':
        os.system("python gui_tkinter.py")
    elif choice == '3':
        os.system("python web_flask.py")
    elif choice == '4':
        print("Goodbye!")
    else:
        print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()