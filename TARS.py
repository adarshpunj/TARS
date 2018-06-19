import Tkinter as tk
import tkFileDialog, ttk, tkMessageBox
from Tkinter import *
from bs4 import BeautifulSoup
import requests
import os
import threading
import time
switch=0
def About(evnt=None):
	os.system('''python -m webbrowser -t "https://github.com/adarshpunj/TARS"''')
def Download():
	user_querry = str(entry.get())
	filename = user_querry
	if user_querry=="":
		tkMessageBox.showinfo("Error","Please enter a movie title.")
		return
	user_querry=user_querry.replace(' ','+')
	default_link="http://www.imdb.com/find?&q="
	imdb_link=default_link+user_querry
	status.config(text="Querry Recieved")
	try:
		status.config(text="Sending Request...")
		response=requests.get(imdb_link)
		status.config(text="Request Sent")
	except:
		tkMessageBox.showinfo("Request Failed","Please check your internet connection, and try again.")
		return
	html=response.text
	soup=BeautifulSoup(html,'html.parser')
	try:
		link=soup.find('table',class_='findList').a['href']
	except:
		tkMessageBox.showinfo("Error","The entered title is invalid. Please enter a valid title, and try again.")
		return
	imdb_code=link[:16][::-1][:-7][::-1]
	status.config(text="Movie Located")
	response=requests.get("http://www.yifysubtitles.com/movie-imdb/"+imdb_code)
	html=response.text
	soup=BeautifulSoup(html,'html.parser')
	rating_list=[]
	href_list=[]
	for article in soup.find_all('tr'):
	    data=article.text
	    if "English" in data:
	        for a in article.find_all('span',class_='label label-success'):
	            rating_list.append(int(a.text))
	            href_list.append(str(article.a.get('href')))
	subtitles = dict(zip(rating_list, href_list))
	linklist=[]
	constant_url="http://www.yifysubtitles.com/subtitle/"
	for i in sorted(subtitles):
	    linklist.append(subtitles[i])
	if linklist==[]:
	    tkMessageBox.showinfo("Failed!","Sorry! No subtitles found. Please check for spelling errors")
	else:
		url=linklist[-1].split('/')[2]
		status.config(text="Subtitle Found")
		root.directory = tkFileDialog.askdirectory()
		file = requests.get(constant_url+url+'.zip',allow_redirects=True)
		open(root.directory+'/'+filename+'-TARS'+'.zip','wb').write(file.content)
		switch = 1
	if switch==1:
		tkMessageBox.showinfo("Success!","The subtitle has been successfully downloaded!")
def downloadThread(event):
	global thread
	thread = threading.Thread(target=Download)
	thread.daemon=True
	thread.start()
if __name__ == '__main__':
	root = tk.Tk()
	root.title("TARS Subtitle Downloader")
	root.geometry("500x400")
	root.resizable(False, False)
	label = tk.Label(root,text="   ")
	label.pack()
	label = tk.Label(root,text="   ")
	label.pack()
	label = tk.Label(root,text="   ")
	label.pack()
	logo = tk.PhotoImage(file="logo.gif")
	label = tk.Label(root,text="ENTER MOVIE TITLE",font=("Helvetica",16))
	label.pack()
	entry = tk.Entry(root)
	entry.pack()
	button = tk.Button(root,text="Download Subtitle",font=("Sans",12),command=lambda:downloadThread(None))
	button.pack()
	status = tk.Label(root,text="",fg="lightblue",font=("Sans",18,"bold"))
	status.pack(pady=60)
	label = tk.Label(root,text="TARS Subtitle Downloader",font=("Sans",12,"bold"),fg='medium slate blue')
	label.pack()
	label = tk.Label(root,text="is a quick and free way to download movie subtitles",font=("Sans",12,"bold"),fg='light slate blue')
	label.pack()
	label = tk.Label(root,text="   ")
	github = tk.Label(root, image=logo)
	github.pack(pady=10)
	github.bind('<Button-1>',About)
	root.mainloop()
