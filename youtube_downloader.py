from __future__ import unicode_literals
import urllib.request
import youtube_dl
from tkinter import *
import tkinter as tk
from bs4 import BeautifulSoup


def show_entry_fields():
    print("First Name: %s\nLast Name:" % (e1.get()))


def get_stream():
    search_query = urllib.parse.quote(e1.get())
    url = "https://www.youtube.com/results?search_query=" + search_query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        if not vid['href'].startswith("https://googleads"):
            first_result = 'https://www.youtube.com' + vid['href']
            break

    print(first_result)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(first_result, download=False)
        video_title = info_dict.get('title', None)
        print(video_title)
        ydl.download([first_result])
        label['text'] = '\'' + video_title + '\'' + ' has been downloaded.'

    e1.delete(0, 'end')


if __name__ == '__main__':
    master = tk.Tk()
    master.geometry('600x400')

    tk.Label(master, text='Song name:').grid(row=0)

    e1 = tk.Entry(master)
    e1.grid(row=0, column=1)

    label = tk.Label(master)  # empty label for text
    label.grid(row=1, column=0)

    tk.Button(master,
              text='Download', command=get_stream).grid(row=3,
                                                        column=1,
                                                        sticky=tk.W,
                                                        pady=4)

    master.mainloop()
