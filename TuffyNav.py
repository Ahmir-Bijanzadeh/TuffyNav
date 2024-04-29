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
    WIDTH = 1920
    HEIGHT = 1080

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
        
        
        #image_1 = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "arbor.jpg")).resize((300, 200)))        
        #marker_1 = self.map_widget.set_marker(33.88844,-117.88433, text="arboretum", image=image_1,image_zoom_visibility=(0, float("inf")), command=click_marker_event)
        #marker_1.hide_image(True)
        #image_2 = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "nutwood.jpg")).resize((300, 200)))        
        #marker_2 = self.map_widget.set_marker(33.87930,-117.88858, text="nutwood parking structure", image=image_2,image_zoom_visibility=(0, float("inf")), command=click_marker_event)
        #marker_2.hide_image(True)
        #defualt paths between nodes
        #path_1 = self.map_widget.set_path([marker_2.position, marker_1.position])#add color= '#FF0000' (red color) argument for when we print the specified path determined by an algo
        #serch bar and search button, commented out since we probably wont use it
        #self.entry = customtkinter.CTkEntry(master=self.frame_right, placeholder_text="type address")
        #self.entry.grid(row=0, column=0, sticky="we", padx=(12, 0), pady=12)
        #self.entry.bind("<Return>", self.search_event)

        image_1 = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "pin.png")).resize((35, 35)))        
        mihaylo = self.map_widget.set_marker(33.878809374053155, -117.88341836262659, text = "Mihaylo Hall", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        langsdorf = self.map_widget.set_marker(33.879065171017324, -117.88435302604127, text = "Langsdorf Hall", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        university_hall = self.map_widget.set_marker(33.879743528510005, -117.88413979569506, text = "University Hall", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        McCarthy = self.map_widget.set_marker(33.879645405637, -117.88551155450016, text = "McCarthy Hall", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        dan_black = self.map_widget.set_marker(33.879278246672776, -117.88585654819984, text= "Dan Black Hall", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        art_center = self.map_widget.set_marker(33.88059975992103, -117.88665536468746,  text= "Art Center", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        h_s_science = self.map_widget.set_marker(33.880589167555, -117.8841163633055, text= "H-S Sciences", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        ec = self.map_widget.set_marker(33.88137321024358, -117.88434730161424, text= "EC", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        Pollak = self.map_widget.set_marker(33.88131806495993, -117.88525384316719, text = "Pollak Library", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        Visual_Arts = self.map_widget.set_marker(33.88022688609634, -117.88863635944018, text = "Visual Arts Building", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        tsu = self.map_widget.set_marker(33.88186676883376, -117.88845279258894, text = "TSU", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        ecs = self.map_widget.set_marker(33.882310882303656, -117.8830018704961, text = "ECS", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        REC_Center = self.map_widget.set_marker(33.88335255103566, -117.88782583780849, text = "REC Center", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        Gym = self.map_widget.set_marker(33.882798357595945, -117.8861484851946, text = "Gym", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        Health_Center = self.map_widget.set_marker(33.88315934073165, -117.884411671363, text = "Health Center", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        
        # new waypoints between gym and rec center
        waypoint1 = (33.882602650147476, -117.8868106853238)
        waypoint2 = (33.88261935054992, -117.88730689397043)
        waypoint3 = (33.882946677776076, -117.88734310378898)

        # Update the path to include the new waypoints
        path_23 = self.map_widget.set_path([
            Gym.position, 
            waypoint1, 
            waypoint2, 
            waypoint3,
            REC_Center.position
        ], width=5)

        # new waypoints between  rec center and pollak libary path 20
        # use waypoint1 2 and 3 from above
        waypoint4 = (33.881817532188336, -117.88590024107901)
        path_20 = self.map_widget.set_path([
            REC_Center.position,
            waypoint3, 
            waypoint2,
            waypoint1,
            waypoint4,  # New waypoint closer to Pollak Library
            Pollak.position
        ], width=5)

        # new waypoints between  gym and health center path 24
        waypoint5 = (33.8825232141922, -117.88576605421719)
        waypoint6 = (33.88262453001256, -117.88499357802259)
        waypoint7 = (33.88264123041209, -117.88458856446181)

        path_24 = self.map_widget.set_path([
            Gym.position,
            waypoint5,
            waypoint6,
            waypoint7,
            Health_Center.position
        ], width=5)

        # new waypoints between health center and ecs path 25
        waypoint8 = (33.88266906440476, -117.88396629197007)
        waypoint9 = (33.88249204007139, -117.88356932503433)
        waypoint10 = (33.88256552191342, -117.88337486488042)
        waypoint11 = (33.88256329519189, -117.88300472003867)

        path_25 = self.map_widget.set_path([
            Health_Center.position,
            waypoint7,
            waypoint8,
            waypoint9,
            waypoint10,
            waypoint11,
            ecs.position
        ], width=5)

        # new waypoints between health center and pollak libary path 18
        waypoint12 = (33.88243296117279, -117.88454350154562)
        waypoint13 = (33.88217688741815, -117.8845542303816)
        waypoint14 = (33.88192749310965, -117.88475807826549)
        waypoint15 = (33.88164781086861, -117.88489449926779)

        path_18 = self.map_widget.set_path([
            Health_Center.position,
            waypoint7,
            waypoint12,
            waypoint13,
            waypoint14,
            waypoint15,
            Pollak.position
        ], width=5)

        # new waypoints between gym and pollak libary path 19
        waypoint16 = (33.88172653818047, -117.88576314581675)
        path_19 = self.map_widget.set_path([
            Gym.position,
            waypoint5,
            waypoint16,
            Pollak.position
        ], width=5)

        # new waypoints between tsu and pollak libary path 21
        waypoint17 = (33.881689087671674, -117.8874359156723)
        waypoint18 = (33.88157257294104, -117.88714884249009)
        waypoint19 = (33.881558008586616, -117.88587296167476)
        path_21 = self.map_widget.set_path([
            tsu.position,
            waypoint17,
            waypoint18,
            waypoint19,
            Pollak.position
        ], width=5)

        # new waypoints between tsu and visual arts path 12
        waypoint20 = (33.88129203249792, -117.8882133976765)
        waypoint21 = (33.88124007222078, -117.88777148797256)
        waypoint22 = (33.88036146636662, -117.88776390153939)
        path_12 = self.map_widget.set_path([
            tsu.position,
            waypoint20,
            waypoint21,
            waypoint22,
            Visual_Arts.position
        ], width=5)

        # new waypoints between visual arts and art center path 13
        path_13 = self.map_widget.set_path([
            Visual_Arts.position,
            waypoint22,
            art_center.position
        ], width=5)

        # new waypoints between art center and mccarthy hall path 8
        waypoint23 = (33.87999144147297, -117.88660128072428)
        waypoint24 = (33.879978844853966, -117.88553159370852)
        path_8 = self.map_widget.set_path([
            art_center.position,
            waypoint23,
            waypoint24,
            McCarthy.position
        ], width=5)

        # new waypoints between mccarthy hall and dan black path
        waypoint25 = (33.87936245143126, -117.88554267586429)
        path_9 = self.map_widget.set_path([
            McCarthy.position,
            waypoint25,
            dan_black.position
        ], width=5)

        # new waypoints between dan black and langsdorf path 4
        waypoint26 = (33.87936008954797, -117.88496326206568)
        waypoint27 = (33.87932389076451, -117.88445218443688)
        path_4 = self.map_widget.set_path([
            dan_black.position,
            waypoint25,
            waypoint26,
            waypoint27,
            langsdorf.position
        ], width=5)

        # new waypoints between langsdorf and university hall path 3
        waypoint28 = (33.879743528510005, -117.88413979569506)
        path_3 = self.map_widget.set_path([
            langsdorf.position,
            waypoint27,
            waypoint28,
            university_hall.position
        ], width=5)

        # new waypoints between langsdorf and mihaylo path 2
        waypoint29 = (33.87927521075621, -117.88428146488879)
        waypoint30 = (33.87913664666704, -117.883826278925)
        path_2 = self.map_widget.set_path([
            langsdorf.position,
            waypoint29,
            waypoint30,
            mihaylo.position
        ], width=5)

        # new waypoints mihaylo and university hall path 1
        waypoint31 = (33.87929882960703, -117.88394766184797)
        path_1 = self.map_widget.set_path([
            mihaylo.position,
            waypoint30,
            waypoint31,
            university_hall.position
        ], width=5)

        # new waypoints between mccarthy hall and h-s sciences path 11
        waypoint32 = (33.880656455803155, -117.8845783866796)
        waypoint33 = (33.88046049970182, -117.8845998443516)
        waypoint34 = (33.88047163358327, -117.88494316710339)
        waypoint35 = (33.880021823616325, -117.88496998919338)
        path_11 = self.map_widget.set_path([
            h_s_science.position,
            waypoint32,
            waypoint33,
            waypoint34,
            waypoint35,
            waypoint24,
            McCarthy.position
        ], width=5)

        # no new waypoints between h_s science and art center
        path_16 = self.map_widget.set_path([
            h_s_science.position,
            waypoint32,
            waypoint33,
            waypoint34,
            waypoint35,
            waypoint24,
            waypoint23,
            art_center.position
        ], width=5)

        # new waypoints between ec and art center path 15
        waypoint36 = (33.88096979970818, -117.88444965239393)
        waypoint37 = (33.880881088894725, -117.88499030688999)
        path = self.map_widget.set_path([
            ec.position,
            waypoint36,
            waypoint37,
            waypoint34,
            waypoint35,
            waypoint24,
            waypoint23,
            art_center.position
        ], width=5)

        # new waypoints between ec and ecs path 17
        waypoint38 = (33.882135802376645, -117.88300096139653)
        waypoint39 = (33.88213050628372, -117.8834092432557)
        waypoint40 = (33.88217552306324, -117.88342838146785)
        waypoint41 = (33.88215963479082, -117.88364528120552)
        waypoint42 = (33.882029880455384, -117.88373459286221)
        waypoint43 = (33.881603543392536, -117.88385261183714)
        waypoint44 = (33.88150556500872, -117.88397701021609)
        path_17 = self.map_widget.set_path([
            ecs.position,
            waypoint38,
            waypoint39,
            waypoint40,
            waypoint41,
            waypoint42,
            waypoint43,
            waypoint44,
            ec.position
        ], width=5)

        # no new waypoints between langsdorf and mccarthy hall
        path_5 = self.map_widget.set_path([
            McCarthy.position,
            waypoint25,
            waypoint26,
            waypoint27,
            langsdorf.position
        ], width=5)

        # no new waypoints between university hall and mccarthy hall
        path_6 = self.map_widget.set_path([
            McCarthy.position,
            waypoint25,
            waypoint26,
            waypoint27,
            university_hall.position
        ], width=5)

        # new waypoints between mccarthy hall and pollak libary path 10
        waypoint45 = (33.8808469561944, -117.88538026678752)
        waypoint46 = (33.880421823506914, -117.88537457696303)
        waypoint47 = (33.88015901820872, -117.88541611172404)
        path_10 = self.map_widget.set_path([
            McCarthy.position,
            waypoint24,
            waypoint47,
            waypoint46,
            waypoint45,
            Pollak.position
        ], width=5)

        # new waypoints between art center and pollak libary path 14
        waypoint48 = (33.88147850126386, -117.88576508762874)
        waypoint49 = (33.881051546914655, -117.88577287661465)
        waypoint50 = (33.88104095459409, -117.88671383871406)
        path_14 = self.map_widget.set_path([
            art_center.position,
            waypoint50,
            waypoint49,
            waypoint48,
            Pollak.position
        ], width=5)

        # new waypoints between rec center and tsu
        waypoint51 = (33.882372377291134, -117.88746252669439)
        waypoint52 = (33.88187984060702, -117.8874370090782)
        path_22 = self.map_widget.set_path([
            REC_Center.position,
            waypoint3,
            waypoint51,
            waypoint52,
            tsu.position
        ], width=5)

        # new waypoints between ec and h-s sciences path 26
        waypoint53 = (33.880840183281336, -117.88434163034049)
        path_26 = self.map_widget.set_path([
            ec.position,
            waypoint36,
            waypoint53,
            h_s_science.position
        ], width=5)

        # this path is good dont remove or adjust
        path_7 = self.map_widget.set_path([university_hall.position, h_s_science.position],width=5)

        
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
