import requests
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

def getPokemonInfo(pokemon: str) -> dict:
    res = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemon)
    if res.status_code != 200:
        return {}
    pokemonInfo = res.json()
    infoBuilded = {
        "name": str(pokemonInfo["name"]).capitalize(),
        "types": str([str(t["type"]["name"]).capitalize() for t in pokemonInfo["types"]]),
        "weight": str(pokemonInfo["weight"]),
        "hp": str(pokemonInfo["stats"][0]["base_stat"]),
        "attack": str(pokemonInfo["stats"][1]["base_stat"]),
        "defense": str(pokemonInfo["stats"][2]["base_stat"]),
        "specialAttack": str(pokemonInfo["stats"][3]["base_stat"]),
        "specialDefense": str(pokemonInfo["stats"][4]["base_stat"]),
        "speed": str(pokemonInfo["stats"][5]["base_stat"]),
        "image": pokemonInfo["sprites"]['front_default']
    }
    return infoBuilded

class pokemonWindow:
    def __init__(self, window: Toplevel, pokeminInfo: dict) -> None:
        self.window = window
        self.window.resizable(0,0)
        self.window.title("POKéDEX")
        self.window.iconbitmap('pokeball.ico')
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        #Primer Frame
        frame1 = LabelFrame(self.window, text="Nombre del Pokémon")
        frame1.grid(row=0,column=0,padx=10,pady=10,columnspan=2,sticky="nswe")
        frame1.grid_columnconfigure(0,weight=1)
        frame1.grid_rowconfigure(0,weight=1)
        Label(frame1, text=pokeminInfo["name"]).grid(row=0,column=0,padx=5,pady=5, sticky='nswe')
        #Segundo Frame
        frame2 = LabelFrame(self.window, text="Estadisticas e Información")
        frame2.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")
        frame2.grid_columnconfigure(0,weight=1)
        frame2.grid_rowconfigure(0,weight=1)
        Label(frame2, text="Tipo:").grid(row=0,column=0,padx=5,pady=5,sticky="nswe")
        Label(frame2, text="Peso:").grid(row=1,column=0,padx=5,pady=5,sticky="nswe")
        Label(frame2, text="HP:").grid(row=2,column=0,padx=5,pady=5,sticky="nswe")
        Label(frame2, text="Ataque:").grid(row=3,column=0,padx=5,pady=5,sticky="nswe")        
        Label(frame2, text="Defensa:").grid(row=4,column=0,padx=5,pady=5,sticky="nswe")
        Label(frame2, text="Ataque Especial:").grid(row=5,column=0,padx=5,pady=5,sticky="nswe")
        Label(frame2, text="Defensa Especial:").grid(row=6,column=0,padx=5,pady=5,sticky="nswe")
        Label(frame2, text="Velocidad:").grid(row=7,column=0,padx=5,pady=5,sticky="nswe")
        Label(frame2, text=pokeminInfo["types"]).grid(row=0,column=1,padx=5,pady=5,sticky="nswe")
        Label(frame2, text=pokeminInfo["weight"]).grid(row=1,column=1,padx=5,pady=5,sticky="nswe")
        Label(frame2, text=pokeminInfo["hp"]).grid(row=2,column=1,padx=5,pady=5,sticky="nswe")
        Label(frame2, text=pokeminInfo["attack"]).grid(row=3,column=1,padx=5,pady=5,sticky="nswe")
        Label(frame2, text=pokeminInfo["defense"]).grid(row=4,column=1,padx=5,pady=5,sticky="nswe")
        Label(frame2, text=pokeminInfo["specialAttack"]).grid(row=5,column=1,padx=5,pady=5,sticky="nswe")
        Label(frame2, text=pokeminInfo["specialDefense"]).grid(row=6,column=1,padx=5,pady=5,sticky="nswe")
        Label(frame2, text=pokeminInfo["speed"]).grid(row=7,column=1,padx=5,pady=5,sticky="nswe")
        #Tercer Frame
        frame3 = LabelFrame(self.window, text="Imagen del Pokémon")
        frame3.grid(row=1,column=1, padx=10, pady=10, sticky="nswe")
        frame3.grid_rowconfigure(0,weight=1)
        frame3.grid_columnconfigure(0,weight=1)
        foto = Label(frame3)
        imagenPokemon = ImageTk.PhotoImage(Image.open(BytesIO(requests.get(pokeminInfo["image"]).content)).resize((200,200)))
        foto.config(image=imagenPokemon)
        foto.image = imagenPokemon
        foto.grid(row=0,column=0,padx=5,pady=5,sticky="nswe")

class mainWindow:
    def __init__(self, window: Tk) -> None:
        self.window = window
        self.window.resizable(0,0)
        self.window.title("POKéDEX")
        self.window.iconbitmap('pokeball.ico')
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        Label(self.window, text="INGRESE EL NOMBRE (MINUSCULAS) O ID del POKéMON").grid(row=0,column=0,padx=10,pady=10,sticky="nswe")
        self.pokemon = StringVar()
        e1 = Entry(self.window, textvariable=self.pokemon, width=30)
        e1.bind('<Return>', self.searchPokemon)
        e1.grid(row=1, column=0, padx=10,pady=10,sticky="nwse")
        #Button(self.window, text="BUSCAR", command=self.searchPokemon, width=30).grid(row=2,column=0,padx=10,pady=10,sticky="nwse")

    def searchPokemon(self,event):
        pokeInfo = getPokemonInfo(self.pokemon.get().lower())
        if len(pokeInfo) == 0:
            messagebox.showerror("ERROR :(","NO SE ENCONTRO AL POKéMON O LO ESCRIBIO MAL")
            self.pokemon.set("")
        else:
            windowPokemon = Toplevel()
            pokemonWindow(windowPokemon, pokeInfo)
            windowPokemon.mainloop()

if __name__ == "__main__":
    windowMain = Tk()
    mainWindow(windowMain)
    windowMain.mainloop()