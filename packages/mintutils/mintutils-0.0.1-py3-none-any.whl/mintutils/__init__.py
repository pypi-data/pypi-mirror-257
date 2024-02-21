from tkinter import *
from install_apps import install_apps
# Global variable to store selected apps
apps_to_install = []

def read_apps_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read app names from file and remove leading/trailing whitespaces
            apps = [line.strip() for line in file.readlines()]
        return apps
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

def submit():
    # Print selected apps (for testing purposes)
    print(apps_to_install)
    install_apps(apps_to_install)

def app_checkbox(frame, text, row, column):
    chk_state = BooleanVar()
    chk_state.set(False)  # Set check state to False initially
    chk = Checkbutton(
        frame,
        bg="#2E3436",
        fg="#FFFFFF",
        activebackground="#2E3436",
        activeforeground="#FFFFFF",
        font=("monospace", 11, "normal"),
        selectcolor="#2E3436",
        text=text,
        var=chk_state,
        command=lambda: clicked(chk_state, name=text)
    )
    chk.grid(row=row, column=column, sticky=W, padx=5, pady=5)
    chk.config(highlightthickness=0, bd=0)
    return chk_state

def clicked(state, name):
    if state.get():
        apps_to_install.append(name)
        print("Checked", name)
    else:
        apps_to_install.remove(name)
        print("Unchecked", name)

def create_window():
    window = Tk()
    window.title("Linux Utils - Muhiris")
    window.configure(background='#2E3436')
    logo_path = 'pfp.png'
    try:
        logo_image = PhotoImage(file=logo_path)
        window.iconphoto(True, logo_image)
    except Exception as e:
        print(f"Error loading logo: {e}")

    center_window(window, width=600, height=300)

    return window

def center_window(window, width, height):
    window.update_idletasks()
    x = window.winfo_screenwidth() // 2 - width // 2
    y = window.winfo_screenheight() // 2 - height // 2
    window.geometry(f'{width}x{height}+{x}+{y}')

def create_checkboxes(frame, app_names, columns_per_row):
    for i, text in enumerate(app_names):
        app_checkbox(frame, text, i // columns_per_row, i % columns_per_row)

def create_submit_button(window):
    submit_button = Button(
        window,
        text="Submit",
        bg="#2E3436",
        fg="#FFFFFF",
        font=("monospace", 11, "normal"),
        command=submit
    )
    submit_button.pack(side="bottom", pady=10)

def create_support_link(window):
    support_text = Text(
        window,
        bg="#B0B0B0",
        font=("monospace", 10),
        cursor="hand2",
        width=28,
        height=1,
        highlightthickness=0,


    )
    support_text.insert(END, "Follow or Support on Github!")
    support_text.tag_add("link", "1.0", "1.end")
    support_text.tag_config("link", foreground="blue", underline=True)
    support_text.pack(pady=5)
    support_text.bind("<Button-1>", lambda event: open_support_link())

def open_support_link():
    # Replace 'https://your-support-website.com' with the actual support link
    import webbrowser
    webbrowser.open("https://github.com/muhiris")

def main():
    # Read app names from the external file
    file_path = 'apps.txt'
    app_names = read_apps_from_file(file_path)
    # Create the main window
    window = create_window()
    # Create a frame for checkboxes
    checkbox_frame = Frame(window, bg="#2E3436")
    checkbox_frame.pack(pady=10)
    # Show checkboxes
    columns_per_row = 4
    create_checkboxes(checkbox_frame, app_names, columns_per_row)
    # Add support link
    create_support_link(window)

    # Add submit button
    create_submit_button(window)
    # Run the main loop
    window.mainloop()

if __name__ == "__main__":
    main()
