import Tkinter as tk
import tkMessageBox
from Tkinter import *
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
switch=0
def About():
	tkMessageBox.showinfo("About","TARS Subtitle Downloader v1.0. Made with Love using Python.")
def Download():
	user_querry = str(entry.get())
	if user_querry=="":
		tkMessageBox.showinfo("Error","Please enter a movie title.")
		return
	user_querry=user_querry.replace(' ','+')
	default_link="http://www.imdb.com/find?&q="
	imdb_link=default_link+user_querry
	try:
		response=requests.get(imdb_link)
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
	    tkMessageBox.showinfo("Failed!","Sorry! No subtitles found.")
	else:
	    url=linklist[-1].split('/')[2]
	    driver=webdriver.Chrome("/Users/adarshpunj/MSD/chromedriver")
	    driver.get(constant_url+url+'.zip')
	    time.sleep(3)
	    switch=1
	    driver.quit()
	if switch==1:
		tkMessageBox.showinfo("Success!","The subtitle has been successfully downloaded to the default Downloads directory!")
if __name__ == '__main__':
	root = tk.Tk()
	root.title("TARS Subtitle Downloader")
	root.geometry("500x400")
	label = tk.Label(root,text="   ")
	label.pack()
	label = tk.Label(root,text="   ")
	label.pack()
	label = tk.Label(root,text="   ")
	label.pack()
	label = tk.Label(root,text="ENTER MOVIE TITLE",font=("Helvetica",16))
	label.pack()
	entry = tk.Entry(root)
	entry.pack()
	button = tk.Button(root, text="Download Subtitle",command=Download)
	button.pack()
	label = tk.Label(root,text="   ")
	label.pack(padx=120,pady=50)
	label = tk.Label(root,text="TARS Subtitle Downloader")
	label.pack()
	label = tk.Label(root,text="is a quick and free way to download movie subtitles")
	label.pack()
	label = tk.Label(root,text="   ")
	label.pack()
	button = tk.Button(root, text="i", font=("Courier",15,"bold"),command=About)
	button.pack()
	root.mainloop()
