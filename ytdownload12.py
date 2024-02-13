from pytube import YouTube
import tkinter as tk
from tkinter import filedialog, ttk
import threading
import os

def download_video():
    url = url_entry.get()
    save_path = save_path_var.get()

    try:
        yt = YouTube(url)
        title_label.config(text="Title: " + yt.title)

        # Populate the combobox with quality options
        streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution')
        resolutions = [stream.resolution for stream in streams]
        quality_combobox['values'] = resolutions
        quality_combobox.current(0)  # Set default quality

        quality_choice = quality_combobox.get()
        stream = streams[resolutions.index(quality_choice)]

        file_size = stream.filesize
        download_progress['maximum'] = file_size

        def download_with_progress():
            stream.download(output_path=save_path, filename='downloaded_video')
            download_btn['state'] = 'normal'  # Re-enable download button after download completion
            download_progress['value'] = 0  # Reset progress bar after download completion
            status_label.config(text="Video downloaded successfully!")
            os.startfile(save_path)  # Open the download folder after completion

        download_thread = threading.Thread(target=download_with_progress)
        download_thread.start()

    except Exception as e:
        print(e)
        # Show error message to the user
        status_label.config(text="Error downloading video")

# GUI setup
root = tk.Tk()
root.title("YouTube Video Downloader")

url_label = ttk.Label(root, text="Enter YouTube URL:")
url_label.grid(row=0, column=0, padx=5, pady=5)

url_entry = ttk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

save_path_label = ttk.Label(root, text="Save to:")
save_path_label.grid(row=1, column=0, padx=5, pady=5)

save_path_var = tk.StringVar()
save_path_entry = ttk.Entry(root, textvariable=save_path_var, width=40)
save_path_entry.grid(row=1, column=1, padx=5, pady=5)

browse_button = ttk.Button(root, text="Browse", command=lambda: save_path_var.set(filedialog.askdirectory()))
browse_button.grid(row=1, column=2, padx=5, pady=5)

quality_label = ttk.Label(root, text="Quality:")
quality_label.grid(row=2, column=0, padx=5, pady=5)

quality_combobox = ttk.Combobox(root, width=20)
quality_combobox.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

download_btn = ttk.Button(root, text="Download", command=download_video)
download_btn.grid(row=3, column=0, columnspan=3, pady=10)

download_progress = ttk.Progressbar(root, orient='horizontal', mode='determinate')
download_progress.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

title_label = ttk.Label(root, text="Title: ")
title_label.grid(row=5, column=0, columnspan=3)

status_label = ttk.Label(root, text="")
status_label.grid(row=6, column=0, columnspan=3)

root.mainloop()
