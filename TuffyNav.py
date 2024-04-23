import customtkinter
from tkintermapview import TkinterMapView
import os
from PIL import Image, ImageTk

customtkinter.set_default_color_theme("blue")

#def BFS_algo 
#def DFS_algo
#def Dijkestra_algo

def click_marker_event(marker):
    print("marker clicked:", marker.text)
    if marker.image_hidden is True:
        marker.hide_image(False)
    else:
        marker.hide_image(True) 

class App(customtkinter.CTk):

    APP_NAME = "TuffyNav"
    WIDTH = 800
    HEIGHT = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "tuffy2.png")), size=(26, 26))
        
        nodeList = ["nutwood","arboretum"]


        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)
        
        self.optionmenu_startLoc = customtkinter.CTkOptionMenu(master=self.frame_left, dynamic_resizing=False, values=nodeList)
        self.optionmenu_startLoc.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.optionmenu_startLoc.set("starting location")
        
        self.optionmenu_endLoc = customtkinter.CTkOptionMenu(master=self.frame_left, dynamic_resizing=False, values=nodeList)
        self.optionmenu_endLoc.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.optionmenu_endLoc.set("ending location")

        #label and theme ver, could be moved into a settings popup window dialog?
        self.map_label = customtkinter.CTkLabel(self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        
        
        image_1 = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "arbor.jpg")).resize((300, 200)))        
        marker_1 = self.map_widget.set_marker(33.88844,-117.88433, text="arboretum", image=image_1,image_zoom_visibility=(0, float("inf")), command=click_marker_event)
        marker_1.hide_image(True)
        image_2 = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "nutwood.jpg")).resize((300, 200)))        
        marker_2 = self.map_widget.set_marker(33.87930,-117.88858, text="nutwood parking structure", image=image_2,image_zoom_visibility=(0, float("inf")), command=click_marker_event)
        marker_2.hide_image(True)
        
        #defualt paths between nodes
        path_1 = self.map_widget.set_path([marker_2.position, marker_1.position])#add color= '#FF0000' (red color) argument for when we print the specified path determined by an algo


        #serch bar and search button, commented out since we probably wont use it
        #self.entry = customtkinter.CTkEntry(master=self.frame_right, placeholder_text="type address")
        #self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        #self.entry.bind("<Return>", self.search_event)

        #self.button_search = customtkinter.CTkButton(master=self.frame_right,text="Search",width=90,command=self.search_event)
        #self.button_search.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        # Set default values for map/settings 
        #use address OR pos + zoom, addy+zoom returns an error
        #self.map_widget.set_address("california state university fullerton")
        self.map_widget.set_position(33.88251, -117.88518)
        self.map_widget.set_zoom(15)
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")

    #search bar function for finding a location
    #def search_event(self, event=None):
        #self.map_widget.set_address(self.entry.get())

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()