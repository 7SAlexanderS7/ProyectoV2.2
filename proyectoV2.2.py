#********LIBRERIAS*********
from tkinter import *
from tkinter import messagebox as msg
import os
import cv2
from matplotlib import pyplot as plt
from mtcnn.mtcnn import MTCNN
import database as db
from PIL import ImageTk, Image

path = "C:/Users/marce/Desktop/ProyectoFinal/"# Direccion de la carpeta del proyecto.
# Declaracion de variables y colores estaticos.
txt_login = "Iniciar Sesión"
txt_register = "Registrarse"

color_white = "#f4f5f4"# Color negro.
color_black = "#101010"# Color blanco.

color_black_btn = "#202020"# Color de boton.
color_background = "#050505"# Color de fondo.

font_label = "Century Gothic"# Tipo de fuente.
size_screen = "500x450"# Dimension de ventana.

# Colores de escape que se setean a un color normal para tener un limitador.
color_success = "\033[1;32;40m"# Color verde
color_error = "\033[1;31;40m"# Color rojo
color_normal = "\033[0;37;40m"# Color blanco

res_bd = {"id": 0, "affected": 0}# Valores que recuperamos de la base de datos.

def getEnter(screen):# Funcion para un label vacio para hacer de salto de linea.
    Label(screen, text="", bg=color_background).pack()

def printAndShow(screen, text, flag):# Creamos una funcion para poder mostrar una ventana emergente.
    if flag:# El parametro flag nos ayuda a hacer una validacion de si es exito o error por medio de una condicion.
        print(color_success + text + color_normal)# Imprimimos en consola un texto con 2 tipos de colores.
        screen.destroy()# Destruimos la ventana actual para que se pierda despues mostrarla.
        msg.showinfo(message=text, title="Éxito!")# Tipo de miniventana para exito con el titulo de la ventana. 
    else:
        print(color_error + text + color_normal)# Imprimimos en consola un texto con 2 tipos de colores.
        msg.showerror(message=text, title="Error!")# Tipo de miniventana para error con el titulo de la ventana.

def register():# Funcion de registro
    global user1 # Asignacion de variables globales
    global user_entry1
    global screen1

    screen1 = Toplevel(root)# Definimos a la variable screen1 para que aparezca encima la ventana root.
    user1 = StringVar()# Definimos a la varable user1 como string

    configure_screen(screen1, txt_register)# Configuramos la screen1 con la funcion ya creada y pasamos el texto del registro.
    user_entry1 = credentials(screen1, user1, 0)# Asignamos la varible a la funcion credentials llamando el else por el valor del flag.

def configure_screen(screen, text):# Funcion para hacer una configuracion ventana
    screen.title(text)# Titulo de la ventana
    screen.geometry(size_screen)# Dimencion de la ventana
    screen.configure(bg=color_background)# Color de fondo de la ventana
    Label(screen, text=f"¡{text}!", fg=color_white, bg=color_black, font=(font_label, 18), width="500", height="2").pack()# Un label que se muestra en la ventana con sus configuraciones respectivas.

def credentials(screen, var, flag):# Funcion para agregar el label "usuario" y un input para las ventanas.
    getEnter(screen)# Salto de linea (ya explicado)
    getEnter(screen)
    getEnter(screen)
    getEnter(screen)
    Label(screen, text="Usuario:", fg=color_white, bg=color_background, font=(font_label, 12)).pack()# Label de usuario con configuraciones.
    entry = Entry(screen, textvariable=var, justify=CENTER, font=(font_label, 12))# Variable input con sus configuraciones.
    entry.focus_force()# Este metodo por defecto nos posiciona en el input.
    entry.pack(side=TOP, ipadx=80, ipady=6)# Configurciones de dimenciones del input(posicion, ancho, alto).

    getEnter(screen)

    if flag:# el parametro flag nos ayuda a hacer una validacion de si es un boton u otro por medio de una condicion ya que flag es == 1 predeterminadamente.
        Button(screen, text="Capturar rostro", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login_capture).pack()# Boton con sus respectivas configuraciones y el cual ejecuta una funcion con el parametro command.
    else:
        Button(screen, text="Capturar rostro", fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=register_capture).pack()# Boton con sus respectivas configuraciones y el cual ejecuta una funcion con el parametro command.
    return entry# Retornamos a entry debido a que se ocupara.

def register_capture():
    cap = cv2.VideoCapture(0)# Se crea el video en la posicion 0 que seria la camara frontal
    user_reg_img = user1.get()# Almacenamos dentro de la variable user_reg_img, la variable que obtuvimos del input con el metodo get.
    img = f"{user_reg_img}.jpg"# Le definimos el nombre a la variable img con dato de la varible obtenido y concatenamos con .jpg para el formato de la img.

    while True:# Un bucle while inicializado en true.
        ret, frame = cap.read()# En la variable frame guardamos todos los frames generados por el video.
        cv2.imshow("Registro Facial", frame)# Mostramos todos los frames en una ventana creada por el imshow con el nombre del titulo.
        if cv2.waitKey(1) == 32:# En esta condicion definimos con que tecla detendremos la ventana del imshow.
            break
    
    cv2.imwrite(img, frame)# Con la funcion de imwrite creamos la imagen y la almacenamos en img con el ultimo frame capturado.
    cap.release()# Aqui liberamos el espacio almacenado. 
    cv2.destroyAllWindows()# Cerramos todas la ventanas creadas por OpenCV.

    user_entry1.delete(0, END)# Aqui limpiamos el input.
    
    pixels = plt.imread(img)# Creamos la variable y almacenamos los pixeles de imagen.
    faces = MTCNN().detect_faces(pixels)# Aqui con la libreria MTCNN leemos los pixeles y detectamos el rostro con un sistema de redes neuronales convulucionales.
    face(img, faces)# Mandamos la imagen y el rostro detectado a la funcion face.
    register_face_db(img)# Mandamos la imagen a la funcion register_face_db

def face(img, faces):
    data = plt.imread(img)
    for i in range(len(faces)):
        x1, y1, ancho, alto = faces[i]["box"]
        x2, y2 = x1 + ancho, y1 + alto
        plt.subplot(1,len(faces), i + 1)
        plt.axis("off")
        face = cv2.resize(data[y1:y2, x1:x2],(150,200), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(img, face)
        plt.imshow(data[y1:y2, x1:x2])

def register_face_db(img):
    name_user = img.replace(".jpg","").replace(".png","")# Almacenamos el nombre de la imagen quitando su extension de formato.
    res_bd = db.registerUser(name_user, path + img)# De database estamos optiendo la funcion registerUser y pasamos el nombre usuario y la imagen con el path que seria su ubicacion.

    getEnter(screen1)

    if(res_bd["affected"]):# Pregunta si inserto los datos.
        printAndShow(screen1, "Éxito! Se ha registrado correctamente", 1)
    else:
        printAndShow(screen1, "Error! No se ha registrado correctamente", 0)
    os.remove(img)# Elimina la imagen que esta en la carpeta local.

def login():# Funcion de logueo.
    global screen2 # Asignacion de variable locales.
    global user2
    global user_entry2

    screen2 = Toplevel(root)# Definimos a la variable screen2 para que aparezca encima la ventana root.
    user2 = StringVar()# Definimos a la varable user2 como string.

    configure_screen(screen2, txt_login)# Configuramos la screen2 con la funcion ya creada y pasamos el texto del login.
    user_entry2 = credentials(screen2, user2, 1)# Asignamos la varible a la funcion credentials llamando el boton por verdadero por el valor del flag (osea == 1).

def login_capture():
    cap = cv2.VideoCapture(0)# Se crea el video en la posicion 0 que seria la camara frontal.
    user_login = user2.get()# Almacenamos dentro de la variable user_login, la variable que obtuvimos del input con el metodo get.
    img = f"{user_login}_login.jpg"# Le definimos el nombre a la variable img con dato de la varible obtenido y concatenamos con _login.jpg para el formato de la img.
    img_user = f"{user_login}.jpg"# Aqui almacenamos la imagen de registro que esta en la base de datos.

    while True:
        ret, frame = cap.read()
        cv2.imshow("Login Facial", frame)
        if cv2.waitKey(1) == 32:
            break
    
    cv2.imwrite(img, frame)
    cap.release()
    cv2.destroyAllWindows()

    user_entry2.delete(0, END)
    
    pixels = plt.imread(img)
    faces = MTCNN().detect_faces(pixels)

    face(img, faces)
    getEnter(screen2)

    res_db = db.getUser(user_login, path + img_user)# Obtenemos el nombre de usuario y la imagen de la base de datos.
    if(res_db["affected"]):# Preguntamos si obtuvimos datos.
        my_files = os.listdir()# Asignamos la lista de datos en la variable.
        if img_user in my_files:# Preguntamos si la imagen imagen de registro esta en la variable
            face_reg = cv2.imread(img_user, 0)# Almacena la imagen de registro en la variable.
            face_log = cv2.imread(img, 0)#Almacena la imagen de logueo en la variable.

            comp = compatibility(face_reg, face_log)# Llamamos a la funcion para comparar imagenes.
            
            if comp >= 0.85:# Aqui preguntramos si la comparacion de imagenes es mayor al 85%.
                print("{}Compatibilidad del {:.1%}{}".format(color_success, float(comp), color_normal))
                printAndShow(screen2, f"Bienvenido al sistema usuario {user_login}", 1)
            else:
                print("{}Compatibilidad del {:.1%}{}".format(color_error, float(comp), color_normal))
                printAndShow(screen2, f"Error! Incopatibilidad de datos", 0)
            os.remove(img_user)# Eliminamos la imagen de registro de la carpeta local.
    
        else:
            printAndShow(screen2, "Error! Usuario no encontrado", 0)
    else:
        printAndShow(screen2, "Error! Usuario no encontrado", 0)
    os.remove(img)# Eliminamos la imagen de logueo de la carpeta local.

def compatibility(img1, img2):
    orb = cv2.ORB_create()#Creamos un objeto de comparacion

    kpa, dac1 = orb.detectAndCompute(img1, None)# Creamos un descriptor 1 extraemos los nodos enlazados
    kpa, dac2 = orb.detectAndCompute(img2, None)# Creamos un descriptor 2 extraemos los nodos enlazados

    comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)# Creamos un comparador de fuerza

    matches = comp.match(dac1, dac2)# Aplicamos el comparador a los descriptores

    similar = [x for x in matches if x.distance < 70]# Extraemos las regiones similares en base a los nodos enlazados
    if len(matches) == 0:
        return 0 #Si no hay regiones similares, entonces te devuelve cero
    return len(similar)/len(matches)# Exportamos el porcentaje de similitud

#*****PANTALLA PRINCIPAL******
root = Tk()# Inicializacion de la libreria TKinter y la ventana principal.
root.geometry(size_screen)# Dimension de pantalla.
root.title("Proyecto Final")# Titulo de ventana.
root.configure(bg=color_background)# Color de fondo.
Label(text="LOGIN AI", fg=color_white, bg=color_black, font=(font_label, 18), width="500", height="2").pack()# Label que funciona de titulo dentro la ventana.

getEnter(root)

imagen = Image.open("AI.png")# Creamos una variable para cargar una imagen
imagen = imagen.resize((200, int(imagen.size[1]*200/imagen.size[0])))# Dimensionamos la imagen.
imagen_tk = ImageTk.PhotoImage(imagen)# Aqui conviertimos la imagen redimensionada en un objeto.
widget_imagen = Label(root, image=imagen_tk)#  Creamos un widget Label de tkinter que muestra la imagen.
widget_imagen.pack()# Agregamos el widget Label a la ventana principal de la aplicación gráfica utilizando el método pack().

getEnter(root)

Button(text=txt_login, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=login).pack()# Boton con sus respectivas configuraciones y el cual ejecuta la funcion login con el parametro command.

getEnter(root)

Button(text=txt_register, fg=color_white, bg=color_black_btn, activebackground=color_background, borderwidth=0, font=(font_label, 14), height="2", width="40", command=register).pack()# Boton con sus respectivas configuraciones y el cual ejecuta la funcion register con el parametro command.

root.mainloop()# Este metodo se usa para iniciar el bucle principal de eventos de la aplicación gráfica para asegurarse de que la ventana permanezca abierta hasta que el usuario la cierre.