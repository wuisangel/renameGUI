from operator import length_hint
from tkinter import *
from tkinter import filedialog
import os
import re
import subprocess
from tkinter import messagebox

root=Tk()
root.title("Renombrar")
tipoArchivos=[]
#Se crea un diccionario con las extenciones asociadas a su variable en el radiobutton
tipos={ 1 : ".JPG", 2 : ".MTS",  3 : ".MOV", 4 : ".mp4"}

def open_dir():
    global archivos, carpeta
    #Limpiamos el Text
    listaArchivos.delete(1.0, END)
    #Abrimos el dialog para seleccionar la carpeta
    try:
        carpeta=filedialog.askdirectory(title="Abrir")
        #Mostramos la direccion de la carpeta en el Entry
        varDir.set(carpeta)
        # archivos=os.listdir(carpeta)#Realizamos un dir y guardamos la salida en una lista
        #Realizamos un dir y comprobamos que lo obtenido no sea una carpeta
        #guardamos solo archivos en $archivos
        archivos=list(filter(lambda elemento: os.path.isdir(carpeta+"/"+elemento)==False,os.listdir(carpeta)))
        
        #Imprimimos la lista de archivos en el Text
        for i in archivos:
            listaArchivos.insert(str(len(archivos))+".0", i+"\n")
        listaArchivos.insert(1.0, "Archivos encontrados: "+str(len(archivos))+"\n")

        rb1.config(state=NORMAL)
        rb2.config(state=NORMAL)
        rb3.config(state=NORMAL)
        rb4.config(state=NORMAL)
        codEntry.config(state=NORMAL)
        indEntry.config(state=NORMAL)
        btRename.config(state=NORMAL)
    except FileNotFoundError:
        pass

##FRAME 1   
fr=Frame(root)
# fr.pack()
fr.grid(row=0, column=0)

##Variables
varDir=StringVar()

dirEntry=Entry(fr, textvariable=varDir, width=30, state=DISABLED)
selectDir=Button(fr, text="...", command=open_dir, width=3)

Label(fr, text="Carpeta: ").grid(row=0, column=0, sticky="e")
dirEntry.grid(row=0, column=1)
selectDir.grid(row=0, column=2, sticky="e")
# selectDir.grid()

##FRAME 2
fr2=Frame(root)
# fr2.pack()
fr2.grid(row=1, column=0)

#Impresion de lista de archivos
listaArchivos=Text(fr2, width=27, height=5)
scrollY=Scrollbar(fr2, command=listaArchivos.yview)

Label(fr2, text="Archivos:").grid(row=0, column=0, sticky="w")
listaArchivos.grid(row=1, column=0, pady=10, padx=5)
scrollY.grid(row=1, column=1, sticky="nsew")
listaArchivos.config(yscrollcommand=scrollY.set)

def impFileType():
    global tipoArchivos
    
    #Guardamos en una nueva lista la extension seleccionada
    tipoArchivos=list(filter(lambda fl: re.findall(tipos[varOp.get()]+"$",fl,re.IGNORECASE),archivos))
    
    #Imprimimos la lista de archivos en el Text
    for i in tipoArchivos:
        listaArchivos.insert(str(len(tipoArchivos))+".0", i+"\n")
    listaArchivos.insert(1.0, "Archivos encontrados: "+str(len(tipoArchivos))+"\n")

#Funciones Frame 3
def fileType():
    global archivos, tipoArchivos

    #Se limpia el Text
    listaArchivos.delete(1.0, END)
    
    #impFileType()
    #Guardamos en una nueva lista la extension seleccionada
    tipoArchivos=list(filter(lambda fl: re.findall(tipos[varOp.get()]+"$",fl,re.IGNORECASE),archivos))
    
    #Imprimimos la lista de archivos en el Text
    for i in tipoArchivos:
        listaArchivos.insert(str(len(tipoArchivos))+".0", i+"\n")
    listaArchivos.insert(1.0, "Archivos encontrados: "+str(len(tipoArchivos))+"\n")

"""Frame 3"""
fr3=Frame(root)
fr3.grid(row=1, column=1)
#Variable radiobutton
varOp=IntVar()

Label(fr3, text="Extensión").pack()
rb1=Radiobutton(fr3, text=".JPG", variable=varOp, value=1, command=fileType, state=DISABLED)
rb1.pack()
rb2=Radiobutton(fr3, text=".MTS", variable=varOp, value=2, command=fileType, state=DISABLED)
rb2.pack()
rb3=Radiobutton(fr3, text=".MOV", variable=varOp, value=3, command=fileType, state=DISABLED)
rb3.pack()
rb4=Radiobutton(fr3, text=".mp4", variable=varOp, value=4, command=fileType, state=DISABLED)
rb4.pack()

def limpiar():
    global listaArchivos, archivos, carpeta
    
    varOp.set(0)
    listaArchivos.delete(1.0, END)
    codVar.set("")
    indVar.set("")
    varDir.set("")
    #carpeta=""
    
    rb1.config(state=DISABLED)
    rb2.config(state=DISABLED)
    rb3.config(state=DISABLED)
    rb4.config(state=DISABLED)
    codEntry.config(state=DISABLED)
    indEntry.config(state=DISABLED)
    btRename.config(state=DISABLED)

#Funciones frame 4
def rename():
    global tipoArchivos, archivos, carpeta
        
    try:
        indice=int(indVar.get())
        # print(len(tipoArchivos))
        #renombramos los archivos
        if len(tipoArchivos) != 0:
            for renombrar in tipoArchivos:
                os.rename(carpeta+"/"+renombrar,carpeta+"/"+codVar.get()+str(indice)+tipos[int(varOp.get())])
                indice+=1
            #se reemplaza la direccion de la carpeta, para poder usarla en elsubprocess
            carp=carpeta.replace("/","\\")
            #abrimos la carpeta en el explorador
            subprocess.Popen(f'explorer {carp}')
            #volvemos a leer los archivos
            archivos=list(filter(lambda elemento: os.path.isdir(carpeta+"/"+elemento)==False,os.listdir(carpeta)))
            #fileType()
            limpiar()
        else:
            messagebox.showerror("Error", "No existen archivos con la extensión "+tipos[int(varOp.get())])
    except KeyError:
        messagebox.showerror("Error", "No ha seleccionado una extensión")
    except UnboundLocalError:
        messagebox.showerror("Error", "Ingrese los campos requeridos. Codigo* e Indice*")
    except ValueError:
        messagebox.showwarning("Advertencia", "Ingrese valores correctos.")

# function to validate mark entry. only numbers
def only_numbers(char):
    return char.isdigit()
 
#Frame 4
fr4=Frame(root)
fr4.grid(row=2, column=0, columnspan=2)
codVar=StringVar()
indVar=StringVar()

#para validar solo numeros en indEntry
validation = fr4.register(only_numbers)

Label(fr4, text="Codigo: ").grid(row=0, column=0, sticky="e")
codEntry=Entry(fr4, textvariable=codVar, width=10, justify="right", state=DISABLED)
codEntry.grid(row=0, column=1)
Label(fr4, text="Indice inicial: ").grid(row=0, column=2, sticky="e")
##Configurado para solo aceptar numeros
indEntry=Entry(fr4, textvariable=indVar, width=10, justify="right", state=DISABLED, validate="key", validatecommand=(validation, '%S'))
indEntry.grid(row=0, column=3)
#Boton para rename
btRename=Button(fr4, text="Renombrar", command=rename, state=DISABLED)
btRename.grid(row=0, column=4, columnspan=2)

root.mainloop()