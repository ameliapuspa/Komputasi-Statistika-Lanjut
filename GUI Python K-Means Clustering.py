from tkinter import * 
from tkinter import filedialog #Load File
import pandas as pd #excel
from pandas import DataFrame
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Grafik
import scipy.stats as stats #uji
from factor_analyzer.factor_analyzer import calculate_kmo #uji kmo

window=Tk()
window.title("PROJECT GUI PYTHON")
window.resizable(width=FALSE, height=FALSE)

canvas1 = Canvas(window, width = 800, height =600, bg='lightblue')
canvas1.pack()

#Judul
labeljudul =Label(window, text="ANALISIS K-MEANS CLUSTER",bg='lightblue',fg="black", font=('helvetica', 14, 'bold'))
labeljudul.place(relx=0.5,rely=0.01,relwidth=0.5,relheight=0.1, anchor='n')


#Frame input
frameInput=Frame(window, bg='#0D324D')
frameInput.place(relx=0.2,rely=0.1,relwidth=0.35,relheight=0.3, anchor='n')

#Input
labelInput = Label(frameInput, text="INPUT",bg='#0D324D',fg="white", font=('helvetica', 15))
labelInput.place(relx=0.5,rely=0.02,relwidth=0.3,relheight=0.1, anchor='n')

labelData = Label(frameInput, text="Masukkan Data Excel",bg='#0D324D',fg="white", bd=8)
labelData.place(relx=0.5,rely=0.2,relwidth=0.8,relheight=0.1, anchor='n')

labelKluster = Label(frameInput, text="Jumlah Cluster",bg='#0D324D',fg="white", bd=8)
labelKluster.place(relx=0.5,rely=0.55,relwidth=0.6,relheight=0.2, anchor='n')

entry1=Entry(frameInput)
entry1.place(relx=0.4,rely=0.8,relwidth=0.2,relheight=0.15, anchor='w')

def getExcel ():
    
    global df
    import_file_path = filedialog.askopenfilename()
    read_file = pd.read_excel (import_file_path)
    df = DataFrame(read_file,columns=['x1','x2'])
    
buttonData=Button(frameInput, text="Pilih File",command=getExcel, font=('helvetica', 10, 'bold'))
buttonData.place(relx=0.33,rely=0.42,relwidth=0.35,relheight=0.15, anchor='w')

#Frame Uji Asumsi
frameUji=Frame(window, bg='#0D324D')
frameUji.place(relx=0.69,rely=0.1,relwidth=0.57,relheight=0.3, anchor='n')

labelAtas = Label(frameUji, text="UJI ASUMSI",bg='#0D324D',fg="white", font=('helvetica', 15))
labelAtas.place(relx=0.5,rely=0.02,relwidth=0.5,relheight=0.1, anchor='n')

#Multikolinearitas
def ujimult():
    global df

    mult=df.corr()
    labelmult=Label(frameUji, text=mult)
    labelmult.place(relx=0.57,rely=0.15,relwidth=0.3, anchor='n')
    
buttonmult=Button(frameUji, text= 'Uji Multikolinearitas', command=ujimult)
buttonmult.place(relx=0.2,rely=0.15,relwidth=0.3,relheight=0.12, anchor='n')

#Bartlett Test
def UjiBartlett():
    global df

    Bart=np.around(stats.bartlett(df.iloc[:,0],df.iloc[:,1]),6)
    labelBartlet=Label(frameUji, text=Bart)
    labelBartlet.place(relx=0.57,rely=0.5,relwidth=0.3, anchor='n')

buttonBartlett=Button(frameUji, text= 'Uji Bartlett', command=UjiBartlett)
buttonBartlett.place(relx=0.2,rely=0.5,relwidth=0.3,relheight=0.12, anchor='n')

#KMO Test
def Kmo():
    global df

    Kmo=np.round(calculate_kmo(df)[-1],4)
    labelKMO=Label(frameUji, text=Kmo)
    labelKMO.place(relx=0.57,rely=0.78, relwidth=0.3,relheight=0.12, anchor='n')

buttonKMO=Button(frameUji, text="KMO Test", command=Kmo)
buttonKMO.place(relx=0.2, rely=0.78,relwidth=0.3,relheight=0.12, anchor='n')

#KMEANS
#Frame Kmeans
frameKmeans=Frame(window, bg='#0D324D')
frameKmeans.place(relx=0.5,rely=0.42,relwidth=0.95,relheight=0.55, anchor='n')

labelUtama = Label(frameKmeans, text="K-MEANS",bg='#0D324D',fg="white", font=('helvetica', 15))
labelUtama.place(relx=0.5,rely=0.02,relwidth=0.5,relheight=0.1, anchor='n')

def Kmeans():
    global df
    global numberOfClusters
    numberOfClusters = int(entry1.get())
    
    kmeans = KMeans(n_clusters=numberOfClusters).fit(df)
    centroids = kmeans.cluster_centers_
    
    labelCen =Label(frameKmeans, text= 'Centroids', fg='white', bg='#0D324D', font=('helvetica', 10, 'bold'))
    labelCen.place(relx=0.1,rely=0.3,relwidth=0.2,relheight=0.1, anchor='n')
    
    labelIsi =Label(frameKmeans, text= centroids)
    labelIsi.place(relx=0.15,rely=0.4, anchor='n')
    
    figure1 = plt.Figure(figsize=(4,3), dpi=100)
    ax1 = figure1.add_subplot(111)
    ax1.scatter(df['x1'], df['x2'], c= kmeans.labels_.astype(float), s=50, alpha=0.5)
    ax1.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
    
    labelScatter=Label(frameKmeans, text= 'Scatter Plot', fg='white', bg='#0D324D', font=('helvetica', 10, 'bold'))
    labelScatter.place(relx=0.7,rely=0.1,relwidth=0.3,relheight=0.2, anchor='n')
    
    scatter1 = FigureCanvasTkAgg(figure1,frameKmeans) 
    scatter1.get_tk_widget().place(relx=0.7,rely=0.25,relwidth=0.45,relheight=0.7, anchor='n')
    
buttonKmeans =Button(frameKmeans, text=' Process k-Means ', command=Kmeans, fg='black', font=('helvetica', 10, 'bold'))
buttonKmeans.place(relx=0.15,rely=0.15,relwidth=0.2,relheight=0.08, anchor='n')

buttonExit = Button(frameKmeans, text = 'EXIT', command=window.destroy, fg='black', font=('helvetica', 10, 'bold'))
buttonExit.place(relx=0.15 , rely=0.85, relwidth=0.2,relheight=0.08, anchor='n')

window.mainloop()