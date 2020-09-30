from tkinter import *
import datetime
import random
import requests

def get_api(app):

    URL = "https://api.openweathermap.org/data/2.5/weather"
    PARAMS = {
       #'appid' : '',
        'lat'   : -23.5537088,
        'lon'   : -46.7086153,
        'units' : 'metric'
    }

    res = requests.get(url=URL, params = PARAMS)
    data = res.json()
    print(data)
    #header
    app.time_label['text'] = datetime.datetime.fromtimestamp(data['dt'])
    #l body 
    app.temp_label      ['text'] = str(data['main']['temp'])     + 'ºC'
    app.umidade_label   ['text'] = str(data['main']['humidity']) + ' %'
    app.pressao_label   ['text'] = str(data['main']['pressure']) + ' hPa'
    app.vel_label       ['text'] = str(data['wind']['speed'])    + ' m/s'
    #r body
    app.umidade_solo_label  ['text'] = str(random.random() * 100) + ' %'

    app.do_grids()

def trocar_luz(app):
    if (app.light_label['text'] == "ON"):
        app.light_label['text'] = "OFF"
    else:
        app.light_label['text'] = "ON"

    app.do_grids();

def regar_planta(app):
    #mandar o pedido etc...
    app.last_regado_label['text'] = str(datetime.datetime.now())

class Application(Frame):
    '''
    bucetalandia, o novo planeta
    '''

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.master.title("ClimaPI")

        for c in range(2):
            self.master.columnconfigure(c, weight=1)
        for r in range(4):
            self.master.rowconfigure(r, weight=1)

        self.header_frame = Frame(master)
        self.lbody_frame =  Frame(master)
        self.rbody_frame =  Frame(master)
        self.footer_frame = Frame(master)

        #App frames
        self.header_frame   .grid(row=0,column=0, rowspan=1, columnspan=2, sticky= W+E+N+S)
        self.lbody_frame    .grid(row=1,column=0, rowspan=2, columnspan=1, sticky= W+E+N+S)
        self.rbody_frame    .grid(row=1,column=1, rowspan=2, columnspan=1, sticky= W+E+N+S)
        self.footer_frame   .grid(row=3,column=0, rowspan=1, columnspan=2, sticky= W+E+N+S)

        #header frame 
        self.time_label = Label(self.header_frame, text="")

        #L_BODY
        self.temp_label =       Label(self.lbody_frame, text=" ")
        self.umidade_label =    Label(self.lbody_frame, text=" ")
        self.pressao_label =    Label(self.lbody_frame, text=" ")
        self.vel_label =        Label(self.lbody_frame, text=" ")
        
        self.temp_label_l =     Label(self.lbody_frame, text="Temperatura: ")
        self.umidade_label_l =  Label(self.lbody_frame, text="Umidade: ")
        self.pressao_label_l =  Label(self.lbody_frame, text="Pressao: ")
        self.vel_label_l =      Label(self.lbody_frame, text="Velocidade do Ar: ")

        #R_BODY        
        self.umidade_solo_label_l = Label(self.rbody_frame, text="Umidade Do Solo: ")
        self.last_regado_label_l =  Label(self.rbody_frame, text="Regado última vez em: ")
        self.light_label_l =        Label(self.rbody_frame, text="Luz: ")

        self.umidade_solo_label =   Label(self.rbody_frame, text=" ")
        self.last_regado_label =    Label(self.rbody_frame, text=" ")
        self.light_label =          Label(self.rbody_frame, text=" ")

        self.regar_btn =            Button(self.rbody_frame, text="Regar Planta", command=lambda:regar_planta(self))
        self.light_switch_btn =     Button(self.rbody_frame, text="Trocar Luz", command=lambda:trocar_luz(self))

        #FOOTER
        self.debug_btn = Button(self.footer_frame, text="GET API", command=lambda:get_api(self))

        self.do_grids()

    def do_grids(self):
        #header
        self.time_label.grid(row=1,column=0,columnspan=2,sticky=W)

        #l body
        self.temp_label_l.      grid(row=0, column=0, sticky=W, padx=1)
        self.umidade_label_l.   grid(row=1, column=0, sticky=W, padx=1)
        self.pressao_label_l.   grid(row=2, column=0, sticky=W, padx=1)
        self.vel_label_l.       grid(row=3, column=0, sticky=W, padx=1)

        self.temp_label.    grid(row=0,column=1,sticky=W,padx=1)
        self.umidade_label. grid(row=1,column=1,sticky=W,padx=1)
        self.pressao_label. grid(row=2,column=1,sticky=W,padx=1)
        self.vel_label.     grid(row=3,column=1,sticky=W,padx=1)

        #r body
        self.umidade_solo_label_l   .grid(row=0, column=0, sticky=W+N, padx=1)
        self.last_regado_label_l    .grid(row=1, column=0, sticky=W+N, padx=1)
        self.light_label_l          .grid(row=3, column=0, sticky=W+N, padx=1)

        self.umidade_solo_label     .grid(row=0, column=1, sticky=W+N, padx=1)
        self.last_regado_label      .grid(row=1, column=1, sticky=W+N, padx=1)
        self.light_label            .grid(row=3, column=1, sticky=W+N, padx=1)

        self.regar_btn              .grid(row=2, column=0, sticky=W+N+E, columnspan=2, padx=10)
        self.light_switch_btn       .grid(row=4, column=0, sticky=W+N+E, columnspan=2, padx=10)

        #footer
        self.debug_btn      .grid(sticky=W+E+N+S, padx=15)
        pass



root = Tk()
root.geometry("500x200+200+200")
app = Application(master=root)
app.mainloop()
