import tkinter as tk
from tkinter import filedialog, ttk
import os, utils, database, openAI, webbrowser, wiki


class SearchResult(tk.Frame):
    filename_font = ("Arial", 12)
    keyword_font = ("Roboto", 10)

    def __init__(self, master, keywords: list, filepath: str, **kwargs):
        filename: str = filepath.split("/")[-1]
        super().__init__(master, **kwargs)
        self.configure(bg='lightgray', borderwidth=1, relief=tk.RIDGE)

        self.filename_label = tk.Label(self, text=filename, font=self.filename_font, bg='lightgray')
        self.filename_label.pack(pady=5, padx=10, fill='x')

        self.keywords_label = tk.Label(self, text=f"Keywords: {keywords}", font=self.keyword_font, bg='lightgray')
        self.keywords_label.pack(pady=(0, 5), padx=10, fill='x')

        self.open_button = tk.Button(self, text="Open", command=self.open_file)
        self.open_button.pack(pady=(0, 5), padx=10, fill='both', expand=True)

        self.filepath = filepath

    def open_file(self):
        if self.filepath and os.path.isfile(self.filepath):
            os.startfile(self.filepath)


# Create a function for the search action
def search():
    # Clear previous search results
    clear_search_results()

    # You can implement the search functionality here
    search_query = entry.get()
    keywords = openAI.generate_keywords_from_term(search_query)
    keywords.append(search_query)
    for keyword in keywords:
        wiki_data = wiki.wiki_search(keyword, method=1)
        title = wiki_data.get("title")
        url = wiki_data.get("url")
        add_additional_button(title, url)
    results = database.query_files_by_keywords(keywords)
    progress_increment = 100 / (len(results))
    total_progress = 0
    print(results)
    for result in results:
        total_progress += progress_increment
        update_progress(total_progress)
        add_search_result(keywords=result.get("keywords"), filepath=result.get("filepath"))



def clear_search_results():
    # Clear previous search results from the UI
    for widget in result_frame.winfo_children():
        widget.destroy()

    for widget in summary_frame.winfo_children():
        widget.destroy()


def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        print(f"Selected Folder: {folder_selected}")
        # Update the text of the entry widget with the folder name
        entry.delete(0, tk.END)  # Clear the current text
        entry.insert(0, f"Search in {folder_selected}")  # Set the text to the selected folder
        for root, dirs, files in os.walk(folder_selected):
            progress_increment = 100 / (len(files))
            total_progress = 0
            for file in files:
                # Get the absolute file path
                total_progress += progress_increment
                update_progress(total_progress)
                file_path = os.path.join(root, file)
                utils.upload_file(file_path)


def add_search_result(keywords, filepath):
    result = SearchResult(master=result_frame, keywords=keywords, filepath=filepath)
    result.pack(fill='x')


entry_font = ("Roboto", 15)
button_font = ("Roboto", 13)
# Create the main window
root = tk.Tk()

# Maximize the window
root.state('zoomed')
root.title("Seeker")

left_panel = tk.Frame(root, bg='grey', border=True, borderwidth=2,
                      relief=tk.RIDGE)  # You can change the background color and width as desired

result_frame = tk.Frame(root, bg='white', borderwidth=1, relief=tk.RIDGE)
result_frame.pack(side='right', fill='both', expand=True)

progress_bar = ttk.Progressbar(root, mode='determinate')
progress_bar.pack(side='top', fill='x')


# Function to update the progress bar
def update_progress(value):
    progress_bar['value'] = value
    root.update_idletasks()


left_panel.pack(side='left', fill='y')  # Place it on the left side and fill the entire height

entry = tk.Entry(left_panel, width=40, font=entry_font, relief=tk.SUNKEN, borderwidth=2)
entry.pack(pady=10, padx=10)  # Add padding for spacing

# Create a search button (Button widget)
search_button = tk.Button(left_panel, text="Search", command=search, font=button_font, width=15)
search_button.pack(pady=10, padx=10)

# Create a "Select Folder" button in the toolbar
select_folder_button = tk.Button(left_panel, text="Select Folder", command=select_folder, font=button_font, width=15)
select_folder_button.pack(padx=10, pady=5)

summary_frame = tk.Frame(left_panel, bg='white', border=True, borderwidth=2, relief=tk.RIDGE)
summary_frame.pack(side='top', fill='both', expand=True, padx=10, pady=(0, 10))
summary_frame.pack_propagate(False)

header_label = tk.Label(summary_frame, text="Additional Resources", font=("Arial", 14, "bold"), bg='lightgrey')
header_label.pack(side='top', fill='x', pady=(0, 5))

def add_additional_button(title, url):
    # Define a function to open the URL in a web browser
    def open_url():
        webbrowser.open(url)

    button = tk.Button(summary_frame, text=title, font=("Arial", 10), bg='white', command=open_url)
    button.pack(fill='x', padx=10, pady=(5, 0))

# Run the Tkinter event loop
root.mainloop()
