import settings as s
import filters as f
import imageIO as io
import contrast as c
import stats as st
import binary as b
import utils as u
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk

import utils

matplotlib.use('TkAgg')


class Interface:
    def __init__(self, window):
        self.window = window
        self.window.iconphoto(False, tk.PhotoImage(file='icons/imgicn.png'))
        self.window.title('Traitement Images GL4')
        self.menu_initialisation()
        self.window.geometry(f'{self.window.winfo_screenwidth() - 100}x{self.window.winfo_screenheight() - 100}+10+10')
        self.currentimage = []
        self.previousimage = []

    def menu_initialisation(self):
        self.menubar = tk.Menu(self.window)

        menuContrast = tk.Menu(self.menubar, tearoff=0)
        menuContrast.add_command(label="Egalisation", command=self.equalisation_callback)
        menuContrast.add_command(label="Dilatation des zones sombres", command=self.darkd_callback)
        menuContrast.add_command(label="Dilatation des zones claires", command=self.lightd_callback)
        menuContrast.add_command(label="Inverse", command=self.inverse_callback)
        menuContrast.add_command(label="Transformation Manuelle", command=self.manual_transformation_window_callback)
        self.menubar.add_cascade(label="TP2", menu=menuContrast)

        menuFilter = tk.Menu(self.menubar, tearoff=0)
        menuFilter.add_command(label="Ajouter Bruit", command=self.noise_callback)
        menuFilter.add_command(label="Filtre Médian", command=self.median_callback)
        menuFilter.add_command(label="Filtre Moyenneur", command=self.average_callback)
        menuFilter.add_command(label="Filtre Gaussien", command=self.gaussian_callback)
        self.menubar.add_cascade(label="TP3", menu=menuFilter)

        menuBinary = tk.Menu(self.menubar, tearoff=0)
        menuBinary.add_command(label="Seuillage Manuel", command=self.manualthresholding_callback)
        menuBinary.add_command(label="Seuillage", command=self.thresholding_callback)
        menuBinary.add_command(label="Dilatation", command=self.dilatation_callback)
        menuBinary.add_command(label="Erosion", command=self.erosion_callback)
        menuBinary.add_command(label="Fermeture", command=self.closing_callback)
        menuBinary.add_command(label="Ouverture", command=self.opening_callback)
        self.menubar.add_cascade(label="TP4", menu=menuBinary)


        self.menubar.add_command(label="Quitter", command=self.QuitMenuButton_callback)

        self.window.config(menu=self.menubar)

        Frametools = tk.Frame(self.window, width=self.window.winfo_screenwidth() * 0.3)
        Frametools.pack_propagate(0)
        Frametools.pack(anchor=tk.W, side=tk.LEFT, fill=tk.Y, expand=tk.YES)

        FrameFile = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(FrameFile, text="Image:").grid(row=0, column=0, padx=2)
        self.entry_text = tk.StringVar()
        self.entry_text.set("input/mona.pgm")
        
        Frameopensave = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Button(Frameopensave, text="Voir", padx=10, pady=5, command=self.openButton_callback).grid(row=0, column=0,
                                                                                                      padx=10)
     
        tk.Entry(FrameFile, width=30, textvariable=self.entry_text).grid(row=0, column=1, padx=10)
        FrameFile.pack(anchor=tk.NW)
        Frameopensave.pack(anchor=tk.NE)
        
        tk.Button(Frameopensave, text="Enregistrer", padx=10, pady=5, command=self.saveButton_callback).grid(row=0, column=1,
                                                                                                      padx=10)
        self.original_button = tk.Button(Frameopensave, text="Originale", state=tk.DISABLED, padx=10, pady=5,
                                         command=self.originalButton_callback)
        self.original_button.grid(row=0, column=2, padx=10)
        self.undo_button = tk.Button(Frameopensave, text="Annuler", state=tk.DISABLED, padx=10, pady=5,
                                         command=self.undoButton_callback)
        self.undo_button.grid(row=0, column=3, padx=10)
        Frameopensave.pack(anchor=tk.NW)

        Framesize = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(Framesize, text="Taille des filtres et des opérations binaires: ").grid(row=0, column=0,
                                                                                                   padx=10)
        self.size_num = tk.Spinbox(Framesize, width=3, from_=3, to=29, increment=2)
        self.size_num.grid(row=0, column=2)
        Framesize.pack(anchor=tk.NW)

        Framethreshold = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(Framethreshold, text="Valeur du seuillage manuel: ").grid(row=0, column=0, padx=10)
        self.thresh_slider = tk.Scale(Framethreshold, from_=0, to=0,length=150,tickinterval=0, orient=tk.HORIZONTAL)
        self.thresh_slider.grid(row=0, column=2)
        Framethreshold.pack(anchor=tk.NW)
        Framewidth = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(Framewidth, text="Largeur:").grid(row=0, column=0, padx=10)
        self.width_text = tk.Label(Framewidth, text="0", width=15, relief=tk.SUNKEN)
        self.width_text.grid(row=0, column=2)
        Framewidth.pack(anchor=tk.NW)

        Frameheight = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(Frameheight, text="Longueur:").grid(row=0, column=0, padx=10)
        self.height_text = tk.Label(Frameheight, text="0", width=15, relief=tk.SUNKEN)
        self.height_text.grid(row=0, column=2)
        Frameheight.pack(anchor=tk.NW)

        Framepixel = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(Framepixel, text="Nombre de pixels:").grid(row=0, column=0, padx=10)
        self.pixel_text = tk.Label(Framepixel, text="0", width=15, relief=tk.SUNKEN)
        self.pixel_text.grid(row=0, column=2)
        Framepixel.pack(anchor=tk.NW)
        


        Frameaverage = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(Frameaverage, text="Moyenne:").grid(row=0, column=0, padx=10)
        self.average_text = tk.Label(Frameaverage, text="0", width=25, relief=tk.SUNKEN)
        self.average_text.grid(row=0, column=2)
        Frameaverage.pack(anchor=tk.NW)

        Framedeviation = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(Framedeviation, text="Déviation:").grid(row=0, column=0, padx=10)
        self.deviation_text = tk.Label(Framedeviation, text="0", width=25, relief=tk.SUNKEN)
        self.deviation_text.grid(row=0, column=2)
        Framedeviation.pack(anchor=tk.NW)

        Frameentropy = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(Frameentropy, text="Entropie:").grid(row=0, column=0, padx=10)
        self.entropy_text = tk.Label(Frameentropy, text="0", width=25, relief=tk.SUNKEN)
        self.entropy_text.grid(row=0, column=2)
        Frameentropy.pack(anchor=tk.NW)

        FrameSNR = tk.Frame(Frametools, height=100, width=100, pady=5)
        tk.Label(FrameSNR, text="SNR:").grid(row=0, column=0, padx=10)
        self.SNR_text = tk.Label(FrameSNR, text="0", width=25, relief=tk.SUNKEN)
        self.SNR_text.grid(row=0, column=2)
        FrameSNR.pack(anchor=tk.NW)

        FrameHistogram = tk.Frame(Frametools, width=self.window.winfo_screenwidth() * 0.3, height=300, pady=5)
        tk.Label(FrameHistogram, text="Histogramme:").pack(padx=10)
        self.fig2 = Figure(figsize=(5, 5), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.ax4 = self.ax2.twinx()
        self.fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(self.fig2, FrameHistogram)
        plot_widget2 = canvas2.get_tk_widget()
        plot_widget2.config(width=self.window.winfo_screenwidth() * 0.3, height=300)
        plot_widget2.pack(expand=tk.YES, anchor=tk.CENTER, pady=5, padx=5)
        FrameHistogram.pack_propagate(True)
        FrameHistogram.pack(anchor=tk.NW)

        self.imageframe = tk.Frame(self.window, width=self.window.winfo_screenwidth() * 0.7)
        self.imageframe.pack_propagate(False)
        self.imageframe.pack(side=tk.RIGHT, fill=tk.Y)
        self.fig1 = Figure(figsize=(6, 5), dpi=100)
        self.ax1 = self.fig1.add_subplot((111))
        canvas1 = FigureCanvasTkAgg(self.fig1, self.imageframe)
        plot_widget = canvas1.get_tk_widget()
        plot_widget.config(width=self.window.winfo_screenwidth() * 0.7, height=self.window.winfo_screenheight())
        plot_widget.pack(expand=tk.YES, anchor=tk.CENTER, pady=20, padx=20)

    def updateStats(self):
        self.width_text.config(text=str(s.width))
        self.height_text.config(text=str(s.height))
        self.pixel_text.config(text=str(st.nbPixels()))
        self.average_text.config(text=str(st.average(self.currentimage)))
        self.deviation_text.config(text=str(st.deviation(self.currentimage)))
        self.entropy_text.config(text=str(st.entropy(self.currentimage)))
        self.SNR_text.config(text=str(st.SNR(self.currentimage)))
        self.displayHistogram()
        self.displayImage()

    def displayImage(self):
        self.ax1.clear()
        self.ax1.imshow(self.currentimage, cmap='gray')
        self.fig1.canvas.draw()

    def displayHistogram(self):
        self.ax2.clear()
        self.ax4.clear()

        flat_image = u.matrixToArray(self.currentimage,s.height,s.width)
        self.ax2.hist(flat_image, bins=s.graylevel, color='skyblue')
        self.ax2.set_xlabel('NdG')
        self.ax2.set_ylabel('Nombre de points')
        self.ax4.hist(flat_image, bins=s.graylevel, cumulative=True, histtype='step', density=True, color='blue')
        self.ax4.set_ylabel('Pourcentage cumulative')
        self.fig2.canvas.draw()

    def openButton_callback(self):
        try:
            io.read(self.entry_text.get())
            self.thresh_slider.config(to=s.graylevel,tickinterval=s.graylevel//4+1)
            self.thresh_slider.set(s.graylevel//2+1)
            self.currentimage = s.image_orig.copy()
            self.updateStats()

        except Exception:
            print("Exception")


    def saveButton_callback(self):
        io.write(self.entry_text.get(), self.currentimage)



    def originalButton_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = s.image_orig.copy()
        self.updateStats()


    def undoButton_callback(self):
        self.currentimage = self.previousimage
        self.undo_button.config(state=tk.DISABLED)
        self.updateStats()


    def equalisation_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = c.equalization(self.currentimage)
        self.updateStats()


    def darkd_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = c.dark_dilatation(self.currentimage)
        self.updateStats()


    def lightd_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = c.light_dilatation(self.currentimage)
        self.updateStats()


    def inverse_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = c.inverse(self.currentimage)
        self.updateStats()


    def manual_transformation_window_callback(self):
        self.points=[]
        self.manualWindow=tk.Toplevel(self.window)
        self.manualWindow.title('Transformation manuelle du contrast')
        self.manualWindow.geometry("700x500")
        Framemain = tk.Frame(self.manualWindow)
        Framemain.pack_propagate(0)
        Framemain.pack(anchor=tk.W, side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        Framepoint = tk.Frame(Framemain, height=100, width=100, pady=5)
        tk.Label(Framepoint, text="Ancienne valeur (X): ").grid(row=0, column=0, padx=2)
        self.entry_X = tk.IntVar()
        self.entry_X.set(0)
        tk.Entry(Framepoint, width=5, textvariable=self.entry_X).grid(row=0, column=1, padx=10)
        tk.Label(Framepoint, text="Nouvelle valeur (Y): ").grid(row=0, column=2, padx=2)
        self.entry_Y = tk.IntVar()
        self.entry_Y.set(0)
        tk.Entry(Framepoint, width=5, textvariable=self.entry_Y).grid(row=0, column=3, padx=10)
        tk.Button(Framepoint, text="Ajouter le point", padx=10, pady=5,
                  command=self.add_point_callback).grid(row=0, column=4, padx=10)
        Framepoint.pack()

        self.fig3 = Figure(figsize=(6, 5), dpi=100)
        self.ax3 = self.fig3.add_subplot(111)
        self.ax3.set_xlim([0, s.graylevel])
        self.ax3.set_ylim([0, s.graylevel])
        canvas3 = FigureCanvasTkAgg(self.fig3, Framemain)
        plot_widget3 = canvas3.get_tk_widget()
        plot_widget3.config(width=600, height=300)
        plot_widget3.pack(expand=tk.YES, anchor=tk.CENTER, pady=5, padx=5)

        tk.Button(Framemain, text="Valider", padx=10, pady=5,
                                         command=self.submit_callback).pack()

    def add_point_callback(self):
        x=self.entry_X.get()
        y=self.entry_Y.get()
        if (x not in range(0,s.graylevel+1) or y not in range(0,s.graylevel+1)):
            return
        self.points.append([x,y])
        self.points.sort()
        pointX=[x[0] for x in self.points]
        pointY=[y[1] for y in self.points]
        self.ax3.clear()
        self.ax3.set_xlim([0,s.graylevel])
        self.ax3.set_ylim([0, s.graylevel])
        self.ax3.plot(pointX,pointY,color='red', marker='o')
        self.ax3.grid(True)
        self.fig3.canvas.draw()

    def submit_callback(self):
        if len(self.points)==0:
            self.points=[[0,0],[255,255]]
        if (self.points[0][0]!=0):
            self.points.insert(0,[0,0])
        if (self.points[-1][0]!=255):
            self.points.append([255,255])
        self.manual_transformation()
        self.manualWindow.destroy()


    def manual_transformation(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = c.linear_transformation(self.currentimage,self.points)
        self.updateStats()


    def median_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = f.filter_median(self.currentimage, int(self.size_num.get()))
        self.updateStats()


    def average_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = f.filter_average(self.currentimage, int(self.size_num.get()))
        self.updateStats()


    def gaussian_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = f.filter_gauss(self.currentimage, int(self.size_num.get()))
        self.updateStats()


    def manualthresholding_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = b.binarize(self.currentimage,self.thresh_slider.get())
        self.updateStats()


    def thresholding_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage,thmin = b.thresholding(self.currentimage)
        self.thresh_slider.set(thmin)
        self.updateStats()


    def dilatation_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = b.dilatation(self.currentimage, int(self.size_num.get()))
        self.updateStats()


    def erosion_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = b.erosion(self.currentimage, int(self.size_num.get()))
        self.updateStats()
 

    def closing_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = b.closing(self.currentimage, int(self.size_num.get()))
        self.updateStats()


    def opening_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = b.opening(self.currentimage, int(self.size_num.get()))
        self.updateStats()
 

    def noise_callback(self):
        self.previousimage = self.currentimage
        self.undo_button.config(state=tk.NORMAL)
        self.currentimage = utils.noise(self.currentimage, s.width, s.height, s.graylevel)
        self.updateStats()


    def QuitMenuButton_callback(self):
        self.window.destroy()


