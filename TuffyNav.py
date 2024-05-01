import customtkinter
from tkintermapview import TkinterMapView
import os
from PIL import Image, ImageTk
import heapq
from collections import deque

from PIL import Image


customtkinter.set_default_color_theme("blue")

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, weight):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges.setdefault(from_node, []).append((to_node, weight))
        self.edges.setdefault(to_node, []).append((from_node, weight))

def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0

    #queue to hold nodes with their current known shortest distance from start
    priority_queue = [(0, start)]

    #keep track of the previous node in the shortest path
    previous_node = {node: None for node in graph.nodes}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph.edges[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_node[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    node = end
    while node:
        path.append(node)
        node = previous_node[node]
    path.reverse()

    return distances[end], path

#Breadth First Search
def bfs(graph, start, end):
    queue = deque()
    visited = set()
    queue.append((start, [start]))

    while queue:
        current_node, path = queue.popleft()
        if current_node == end:
            return path
    
        for neighbor, _ in graph.edges[current_node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return []


#DFS
def dfs(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph.nodes:
        return []
    paths = []
    for neighbor, _ in graph.edges[start]:
        if neighbor not in path:
            new_paths = dfs(graph, neighbor, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths
#End of algorithms

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
        
        List = ["Mihaylo Hall", "Langsdorf Hall", "University Hall", "McCarthy Hall", "Dan Black Hall", "Art Center", "H-S Sciences",
                    "EC", "Pollak Library", "Visual Arts Building", "TSU", "ECS", "REC Center", "Gym", "Health Center"]
        #sorts List A-Z
        nodeList = sorted(List) 


        # ------- transparent marker for waypoints -------

        # Create a transparent icon
        transparent_icon = Image.new("RGBA", (35, 35), (255, 255, 255, 0))  # 35x35 transparent icon
        transparent_icon_path = os.path.join(image_path, "transparent_icon.png")
        transparent_icon.save(transparent_icon_path)

        # Now load this as an image in Tkinter
        transparent_icon_image = ImageTk.PhotoImage(Image.open(transparent_icon_path))

        # Set the text color to the background color (assuming white background) or use a very tiny font size
        background_color = "#ffffff"  # this should match your map's background color
        tiny_font_size = 1  # Making the font size very small to make it nearly invisible

        # ------- end of transparent marker for waypoints -------


        def new_path():
            graph = Graph()
            graph.add_edge('University Hall', 'H-S Sciences', 3)

            # Adding new segment: edges with waypoints between ec and h-s sciences
            graph.add_edge('EC', 'Waypoint 36', 1)
            graph.add_edge('Waypoint 36', 'Waypoint 53', 1)
            graph.add_edge('Waypoint 53', 'H-S Sciences', 1)
            
            # Adding new segment: edges with waypoints between rec center and tsu
            graph.add_edge('REC Center', 'Waypoint 3', 1)
            graph.add_edge('Waypoint 3', 'Waypoint 51', 1)
            graph.add_edge('Waypoint 51', 'Waypoint 52', 1)
            graph.add_edge('Waypoint 52', 'TSU', 1)


            # Adding new segment: edges with waypoints between art center and pollak library
            graph.add_edge('Art Center', 'Waypoint 50', 1)
            graph.add_edge('Waypoint 50', 'Waypoint 49', 1)
            graph.add_edge('Waypoint 49', 'Waypoint 48', 1)
            graph.add_edge('Waypoint 48', 'Pollak Library', 1)

            # Adding new segment: edges with waypoints between mcCarthy hall and pollak library
            graph.add_edge('McCarthy Hall', 'Waypoint 24', 1)
            graph.add_edge('Waypoint 24', 'Waypoint 47', 1)
            graph.add_edge('Waypoint 47', 'Waypoint 46', 1)
            graph.add_edge('Waypoint 46', 'Waypoint 45', 1)
            graph.add_edge('Waypoint 45', 'Pollak Library', 1)

            # Adding new segment: edges with waypoints between mcCarthy hall and university hall
            graph.add_edge('McCarthy Hall', 'Waypoint 25', 1)
            graph.add_edge('Waypoint 25', 'Waypoint 26', 1)
            graph.add_edge('Waypoint 26', 'Waypoint 27', 1)
            graph.add_edge('Waypoint 27', 'University Hall', 1)

            # Adding new segment: edges with waypoints between ec and art center
            graph.add_edge('EC', 'Waypoint 36', 1)
            graph.add_edge('Waypoint 36', 'Waypoint 37', 1)
            graph.add_edge('Waypoint 37', 'Waypoint 34', 1)
            graph.add_edge('Waypoint 34', 'Waypoint 35', 1)
            graph.add_edge('Waypoint 35', 'Waypoint 24', 1)
            graph.add_edge('Waypoint 24', 'Waypoint 23', 1)
            graph.add_edge('Waypoint 23', 'Art Center', 1)

            # Adding new segment: edges with waypoints between h-s sciences and mccarthy hall
            graph.add_edge('H-S Sciences', 'Waypoint 32', 1)
            graph.add_edge('Waypoint 32', 'Waypoint 33', 1)
            graph.add_edge('Waypoint 33', 'Waypoint 34', 1)
            graph.add_edge('Waypoint 34', 'Waypoint 35', 1)
            graph.add_edge('Waypoint 35', 'Waypoint 24', 1)
            graph.add_edge('Waypoint 24', 'McCarthy Hall', 1)

            # Adding new segment: edges with waypoints between mihaylo and university hall
            graph.add_edge('Mihaylo Hall', 'Waypoint 30', 1)
            graph.add_edge('Waypoint 30', 'Waypoint 31', 1)
            graph.add_edge('Waypoint 31', 'University Hall', 1)

            # Adding new segment: edges with waypoints between langsdorf and mihaylo
            graph.add_edge('Langsdorf Hall', 'Waypoint 29', 1)
            graph.add_edge('Waypoint 29', 'Waypoint 30', 1)
            graph.add_edge('Waypoint 30', 'Mihaylo Hall', 1)

            # Adding new segment: edges with waypoints between langsdorf and university hall
            graph.add_edge('Langsdorf Hall', 'Waypoint 27', 1)
            graph.add_edge('Waypoint 27', 'Waypoint 28', 1)
            graph.add_edge('Waypoint 28', 'University Hall', 1)

            # Adding new segment: edges with waypoints between Dan Black Hall and Langsdorf Hall
            graph.add_edge('Dan Black Hall', 'Waypoint 25', 1)
            graph.add_edge('Waypoint 25', 'Waypoint 26', 1)
            graph.add_edge('Waypoint 26', 'Waypoint 27', 1)
            graph.add_edge('Waypoint 27', 'Langsdorf Hall', 1)

            # Adding new segment: edges with waypoints between McCarthy Hall and Dan Black Hall
            graph.add_edge('McCarthy Hall', 'Waypoint 25', 1)
            graph.add_edge('Waypoint 25', 'Dan Black Hall', 1)

            # Adding new segment: edges with waypoints between Art Center and McCarthy Hall
            graph.add_edge('Art Center', 'Waypoint 23', 1)
            graph.add_edge('Waypoint 23', 'Waypoint 24', 1)
            graph.add_edge('Waypoint 24', 'McCarthy Hall', 1)

            # Adding new segment: edges with waypoints between Visual Arts and Art Center
            graph.add_edge('Visual Arts Building', 'Waypoint 22', 1)
            graph.add_edge('Waypoint 22', 'Art Center', 1)

            # Adding new segment: edges with waypoints between TSU and Visual Arts
            graph.add_edge('TSU', 'Waypoint 20', 1)
            graph.add_edge('Waypoint 20', 'Waypoint 21', 1)
            graph.add_edge('Waypoint 21', 'Waypoint 22', 1)
            graph.add_edge('Waypoint 22', 'Visual Arts Building', 1)

            # Adding new segment: edges with waypoints between TSU and Pollak Library
            graph.add_edge('TSU', 'Waypoint 17', 1)  # Assuming weight is 1
            graph.add_edge('Waypoint 17', 'Waypoint 18', 1)
            graph.add_edge('Waypoint 18', 'Waypoint 19', 1)
            graph.add_edge('Waypoint 19', 'Pollak Library', 1)

            # Adding new segment: edges with waypoints between Gym and Pollak Library
            graph.add_edge('Gym', 'Waypoint 5', 1)  # Assuming weight is 1
            graph.add_edge('Waypoint 5', 'Waypoint 16', 1)
            graph.add_edge('Waypoint 16', 'Pollak Library', 1)

            # Adding new segment: edges with waypoints between Health Center and Pollak
            graph.add_edge('Health Center', 'Waypoint 7', 0)
            graph.add_edge('Waypoint 7', 'Waypoint 12', 0)
            graph.add_edge('Waypoint 12', 'Waypoint 13', 0)
            graph.add_edge('Waypoint 13', 'Waypoint 14', 0)
            graph.add_edge('Waypoint 14', 'Waypoint 15', 0)
            graph.add_edge('Waypoint 15', 'Pollak Library', 0)
            
            # Adding edges with waypoints between Gym and REC Center (previous segment)
            graph.add_edge('Gym', 'Waypoint 1', 1)  # Assuming weight is 1
            graph.add_edge('Waypoint 1', 'Waypoint 2', 1)
            graph.add_edge('Waypoint 2', 'Waypoint 3', 1)
            graph.add_edge('Waypoint 3', 'REC Center', 1)

            # Adding new segment: edges with waypoints between REC Center and Pollak Library
            graph.add_edge('REC Center', 'Waypoint 3', 1)  # Adjust weight as necessary
            graph.add_edge('Waypoint 3', 'Waypoint 2', 1)
            graph.add_edge('Waypoint 2', 'Waypoint 1', 1)
            graph.add_edge('Waypoint 1', 'Waypoint 4', 1)
            graph.add_edge('Waypoint 4', 'Pollak Library', 1)

            # Adding new segment: edges with waypoints between Gym and Health Center
            graph.add_edge('Gym', 'Waypoint 5', 1)
            graph.add_edge('Waypoint 5', 'Waypoint 6', 1)
            graph.add_edge('Waypoint 6', 'Waypoint 7', 1)
            graph.add_edge('Waypoint 7', 'Health Center', 1)

            # Adding new segment: edges with waypoints between Health Center and ECS
            graph.add_edge('Health Center', 'Waypoint 7', 1)
            graph.add_edge('Waypoint 7', 'Waypoint 8', 1)
            graph.add_edge('Waypoint 8', 'Waypoint 9', 1)
            graph.add_edge('Waypoint 9', 'Waypoint 10', 1)
            graph.add_edge('Waypoint 10', 'Waypoint 11', 1)
            graph.add_edge('Waypoint 11', 'ECS', 1)

            # BLOCK 1: this block is not neeed
            # Adding new segment: edges with waypoints between h-s sciences and art center
            # graph.add_edge('H-S Sciences', 'Waypoint 32', 1)
            # graph.add_edge('Waypoint 32', 'Waypoint 33', 1)
            # graph.add_edge('Waypoint 33', 'Waypoint 34', 1)
            # graph.add_edge('Waypoint 34', 'Waypoint 35', 1)
            # graph.add_edge('Waypoint 35', 'Waypoint 24', 1)
            # graph.add_edge('Waypoint 24', 'Waypoint 23', 1)
            # graph.add_edge('Waypoint 23', 'Art Center', 1)

            # Adding new segment: edges with waypoints between ecs and ec
            graph.add_edge('ECS', 'Waypoint 38', 1)
            graph.add_edge('Waypoint 38', 'Waypoint 39', 1)
            graph.add_edge('Waypoint 39', 'Waypoint 40', 1)
            graph.add_edge('Waypoint 40', 'Waypoint 41', 1)
            graph.add_edge('Waypoint 41', 'Waypoint 42', 1)
            graph.add_edge('Waypoint 42', 'Waypoint 43', 1)
            graph.add_edge('Waypoint 43', 'Waypoint 44', 1)
            graph.add_edge('Waypoint 44', 'EC ', 1)



            graph.add_edge('EC ', 'H-S Sciences', 3)

            #saves user selection to start and end
            start = self.optionmenu_startLoc.get()
            end = self.optionmenu_endLoc.get()

            
            bfspath= bfs(graph, start, end)
            bfs_path = []
            for i in range(len(bfspath)):
                for j in range(len(markers)):
                    if markers[j].text is bfspath[i]:
                        bfs_path.append(markers[j])
            for n in range(len(bfs_path)-1):
                path_000 = self.map_widget.set_path([bfs_path[n].position, bfs_path[n+1].position],width=11, color= 'black')

            shortest_distance, shortest_path = dijkstra(graph, start, end)            
            dijkstrapath = []
            for i in range(len(shortest_path)):
                for j in range(len(markers)):
                    if markers[j].text is shortest_path[i]:
                        dijkstrapath.append(markers[j])
                        
            for n in range(len(dijkstrapath)-1):
                path_5 = self.map_widget.set_path([dijkstrapath[n].position, dijkstrapath[n+1].position],width=8, color= 'red')


        
            
        def clear_path():
            self.destroy()

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
        self.optionmenu_startLoc.set("Starting Location")
        
        self.optionmenu_endLoc = customtkinter.CTkOptionMenu(master=self.frame_left, dynamic_resizing=False, values=nodeList)
        self.optionmenu_endLoc.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.optionmenu_endLoc.set("Ending Location")

         #submit button
        self.submit_button = customtkinter.CTkButton(master=self.frame_left, text="Submit", command=new_path)
        self.submit_button.grid(row=2, column=0)
        #clear button
        #self.submit_button = customtkinter.CTkButton(master=self.frame_left, text="Clear", command=clear_path)
        #self.submit_button.grid(row=2, column=0, pady=50)

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
        arboretum = self.map_widget.set_marker(33.884544550336955, -117.883457701246513, text = "Arboretum", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        lotD= self.map_widget.set_marker(33.88409886074794, -117.88781307685497, text = "Lot D Parking", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        eastParking = self.map_widget.set_marker(33.88152838780693, -117.88164928744573, text = "East Side Parking", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        nutwoodpark = self.map_widget.set_marker(33.879135218086454, -117.88842651662075, text = "Nutwood Parking", icon = image_1, font=("Helvetica Bold", 12), text_color="black")
        
        
        image_2= ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "dash.png")).resize((35, 35))) 

    
        
        # new waypoints between gym and rec center
        waypoint1 = self.map_widget.set_marker(33.882602650147476, -117.8868106853238, icon=transparent_icon_image, text="Waypoint 1", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint2 = self.map_widget.set_marker(33.88261935054992, -117.88730689397043, icon=transparent_icon_image, text="Waypoint 2", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint3 = self.map_widget.set_marker(33.882946677776076, -117.88734310378898, icon=transparent_icon_image, text="Waypoint 3", text_color=background_color, font=("Helvetica", tiny_font_size))
        path_23 = self.map_widget.set_path([REC_Center.position, waypoint3.position, waypoint2.position, waypoint1.position, Gym.position],width=5)
        placeholder1 = self.map_widget.set_marker(33.8827039, -117.8864431, icon=image_2, text="490ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        # # new waypoints between  rec center and pollak libary path 20
        # # use waypoint1 2 and 3 from above
        waypoint4 = self.map_widget.set_marker(33.881817532188336, -117.88590024107901, icon=transparent_icon_image, text="Waypoint 4", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder22 = self.map_widget.set_marker(33.8831381, -117.8875599, icon=image_2, text="900ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path_20 = self.map_widget.set_path([
            REC_Center.position,
            waypoint3.position,
            waypoint2.position,
            waypoint1.position,
            waypoint4.position,
            Pollak.position
        ], width=5)

        # # new waypoints between  gym and health center path 24
        waypoint5 = self.map_widget.set_marker(33.8825232141922, -117.88576605421719, icon=transparent_icon_image, text="Waypoint 5", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint6 = self.map_widget.set_marker(33.88262453001256, -117.88499357802259, icon=transparent_icon_image, text="Waypoint 6", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint7 = self.map_widget.set_marker(33.88264123041209, -117.88458856446181, icon=transparent_icon_image, text="Waypoint 7", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder2 = self.map_widget.set_marker(33.88262453001256, -117.88499357802259, icon=image_2, text="500ft", text_color='blue', font=("Helvetica", 17, 'bold'))#

        path_24 = self.map_widget.set_path([
            Gym.position,
            waypoint5.position,
            waypoint6.position,
            waypoint7.position,
            Health_Center.position
        ], width=5)

        # # new waypoints between health center and ecs path 25
        waypoint8 = self.map_widget.set_marker(33.88266906440476, -117.88396629197007, icon=transparent_icon_image, text="Waypoint 8", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint9 = self.map_widget.set_marker(33.88249204007139, -117.88356932503433, icon=transparent_icon_image, text="Waypoint 9", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint10 = self.map_widget.set_marker(33.88256552191342, -117.88337486488042, icon=transparent_icon_image, text="Waypoint 10", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint11 = self.map_widget.set_marker(33.88256329519189, -117.88300472003867, icon=transparent_icon_image, text="Waypoint 11", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder3 = self.map_widget.set_marker(33.88249204007139, -117.88356932503433, icon=image_2, text="400ft", text_color='blue', font=("Helvetica", 17, 'bold') )

        path_25 = self.map_widget.set_path([
            Health_Center.position,
            waypoint7.position,
            waypoint8.position,
            waypoint9.position,
            waypoint10.position,
            waypoint11.position,
            ecs.position
        ], width=5)

        # # new waypoints between health center and pollak libary path 18
        waypoint12 = self.map_widget.set_marker(33.88243296117279, -117.88454350154562, icon=transparent_icon_image, text="Waypoint 12", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint13 = self.map_widget.set_marker(33.88217688741815, -117.8845542303816, icon=transparent_icon_image, text="Waypoint 13", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint14 = self.map_widget.set_marker(33.88192749310965, -117.88475807826549, icon=transparent_icon_image, text="Waypoint 14", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint15 = self.map_widget.set_marker(33.88164781086861, -117.88489449926779, icon=transparent_icon_image, text="Waypoint 15", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder4 = self.map_widget.set_marker(33.88217688741815, -117.8845542303816, icon=image_2, text="800ft", text_color='blue', font=("Helvetica",17, 'bold'))

        path_18 = self.map_widget.set_path([
            Health_Center.position,
            waypoint7.position,
            waypoint12.position,
            waypoint13.position,
            waypoint14.position,
            waypoint15.position,
            Pollak.position
        ], width=5)

        # # new waypoints between gym and pollak libary path 19
        waypoint16 = self.map_widget.set_marker(33.88172653818047, -117.88576314581675, icon=transparent_icon_image, text="Waypoint 16", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder5 = self.map_widget.set_marker(33.8821805, -117.8857666, icon=transparent_icon_image, text="700ft", text_color='blue', font=("Helvetica",17, 'bold'))

        path_19 = self.map_widget.set_path([
            Gym.position,
            waypoint5.position,
            waypoint16.position,
            Pollak.position
        ], width=5)

        # # new waypoints between tsu and pollak libary path 21
        waypoint17 = self.map_widget.set_marker(33.881689087671674, -117.8874359156723, icon=transparent_icon_image, text="Waypoint 17", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint18 = self.map_widget.set_marker(33.88157257294104, -117.88714884249009, icon=transparent_icon_image, text="Waypoint 18", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint19 = self.map_widget.set_marker(33.881558008586616, -117.88587296167476, icon=transparent_icon_image, text="Waypoint 19", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder6 = self.map_widget.set_marker(33.88157257294104, -117.88714884249009, icon=image_2, text="850ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path_21 = self.map_widget.set_path([
            tsu.position,
            waypoint17.position,
            waypoint18.position,
            waypoint19.position,
            Pollak.position
        ], width=5)

        # # new waypoints between tsu and visual arts path 12
        waypoint20 = self.map_widget.set_marker(33.88129203249792, -117.8882133976765, icon=transparent_icon_image, text="Waypoint 20", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint21 = self.map_widget.set_marker(33.88124007222078, -117.88777148797256, icon=transparent_icon_image, text="Waypoint 21", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint22 = self.map_widget.set_marker(33.88036146636662, -117.88776390153939, icon=transparent_icon_image, text="Waypoint 22", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder7 = self.map_widget.set_marker(33.88124007222078, -117.88777148797256, icon=image_2, text="750ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path_12 = self.map_widget.set_path([
            tsu.position,
            waypoint20.position,
            waypoint21.position,
            waypoint22.position,
            Visual_Arts.position
        ], width=5)

        # # new waypoints between visual arts and art center path 13
        path_13 = self.map_widget.set_path([Visual_Arts.position, waypoint22.position, art_center.position],width=5)
        placeholder23 = self.map_widget.set_marker(33.8804261, -117.8873853, icon=image_2, text="350ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        # # new waypoints between art center and mccarthy hall path 8
        waypoint23 = self.map_widget.set_marker(33.87999144147297, -117.88660128072428, icon=transparent_icon_image, text="Waypoint 23", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint24 = self.map_widget.set_marker(33.879978844853966, -117.88553159370852, icon=transparent_icon_image, text="Waypoint 24", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder8 = self.map_widget.set_marker(33.87999144147297, -117.88660128072428, icon=transparent_icon_image, text="550ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path = self.map_widget.set_path([
            art_center.position,
            waypoint23.position,
            waypoint24.position,
            McCarthy.position
        ], width=5)

        # # new waypoints between mccarthy hall and dan black path
        waypoint25 = self.map_widget.set_marker(33.87936245143126, -117.88554267586429, icon=transparent_icon_image, text="Waypoint 25", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder9 = self.map_widget.set_marker(33.87936245143126, -117.88554267586429, icon=transparent_icon_image, text="60ft", text_color='blue', font=("Helvetica", 17,'bold' ))

        path_9 = self.map_widget.set_path([
            McCarthy.position,
            waypoint25.position,
            dan_black.position
        ], width=5)

        # # new waypoints between dan black and langsdorf path 4
        waypoint26 = self.map_widget.set_marker(33.87936008954797, -117.88496326206568, icon=transparent_icon_image, text="Waypoint 26", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint27 = self.map_widget.set_marker(33.87932389076451, -117.88445218443688, icon=transparent_icon_image, text="Waypoint 27", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder10 = self.map_widget.set_marker(33.8793720, -117.8850137, icon=image_2, text="400ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path_4 = self.map_widget.set_path([
            dan_black.position,
            waypoint25.position,
            waypoint26.position,
            waypoint27.position,
            langsdorf.position
        ], width=5)

        # # new waypoints between langsdorf and university hall path 3
        waypoint28 = self.map_widget.set_marker(33.879743528510005, -117.88413979569506, icon=transparent_icon_image, text="Waypoint 28", text_color=background_color, font=("Helvetica", tiny_font_size))
        path_3 = self.map_widget.set_path([langsdorf.position, waypoint27.position, waypoint28.position, university_hall.position],width=5)
        placeholder11 = self.map_widget.set_marker(33.8795451, -117.8842824, icon=transparent_icon_image, text="450ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        # # new waypoints between langsdorf and mihaylo path 2
        waypoint29 = self.map_widget.set_marker(33.87927521075621, -117.88428146488879, icon=transparent_icon_image, text="Waypoint 29", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint30 = self.map_widget.set_marker(33.87913664666704, -117.883826278925, icon=transparent_icon_image, text="Waypoint 30", text_color=background_color, font=("Helvetica", tiny_font_size))
        path_2 = self.map_widget.set_path([langsdorf.position, waypoint29.position, waypoint30.position, mihaylo.position],width=5)
        placeholder12 = self.map_widget.set_marker(33.8792038, -117.8840659, icon=image_2, text="300ft", text_color='blue', font=("Helvetica", 17,'bold'))

        # # new waypoints mihaylo and university hall path 1
        waypoint31 = self.map_widget.set_marker(33.87929882960703, -117.88394766184797, icon=transparent_icon_image, text="Waypoint 31", text_color=background_color, font=("Helvetica", tiny_font_size))
        path_1 = self.map_widget.set_path([mihaylo.position, waypoint30.position, waypoint31.position, university_hall.position],width=5)
        placeholder13 = self.map_widget.set_marker(33.8794698 ,-117.8840180, icon=image_2, text="400ft", text_color='blue', font=("Helvetica", 17,'bold'))

        # # new waypoints between mccarthy hall and h-s sciences path 11
        waypoint32 = self.map_widget.set_marker(33.880656455803155, -117.8845783866796, icon=transparent_icon_image, text="Waypoint 32", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint33 = self.map_widget.set_marker(33.88046049970182, -117.8845998443516, icon=transparent_icon_image, text="Waypoint 33", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint34 = self.map_widget.set_marker(33.88047163358327, -117.88494316710339, icon=transparent_icon_image, text="Waypoint 34", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint35 = self.map_widget.set_marker(33.880021823616325, -117.88496998919338, icon=transparent_icon_image, text="Waypoint 35", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder14 = self.map_widget.set_marker(33.88046049970182, -117.8845998443516, icon=transparent_icon_image, text="650ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path_11 = self.map_widget.set_path([
            h_s_science.position,
            waypoint32.position,
            waypoint33.position,
            waypoint34.position,
            waypoint35.position,
            waypoint24.position,
            McCarthy.position
        ], width=5)

        # BLOCK 1: this block is not neeed
        # # no new waypoints between h_s science and art center
        # path_16 = self.map_widget.set_path([
        #     h_s_science.position,
        #     waypoint32.position,
        #     waypoint33.position,
        #     waypoint34.position,
        #     waypoint35.position,
        #     waypoint24.position,
        #     waypoint23.position,
        #     art_center.position
        # ], width=5)

        # # new waypoints between ec and art center path 15
        waypoint36 = self.map_widget.set_marker(33.88096979970818, -117.88444965239393, icon=transparent_icon_image, text="Waypoint 36", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint37 = self.map_widget.set_marker(33.880881088894725, -117.88499030688999, icon=transparent_icon_image, text="Waypoint 37", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder15= self.map_widget.set_marker(33.8809222 ,-117.8847464, icon=image_2, text="1,250ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path_16 = self.map_widget.set_path([
            ec.position,
            waypoint36.position,
            waypoint37.position,
            waypoint34.position,
            waypoint35.position,
            waypoint24.position,
            waypoint23.position,
            art_center.position
        ], width=5)

        # # new waypoints between ec and ecs path 17
        waypoint38 = self.map_widget.set_marker(33.882135802376645, -117.88300096139653, icon=transparent_icon_image, text="Waypoint 38", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint39 = self.map_widget.set_marker(33.88213050628372, -117.8834092432557, icon=transparent_icon_image, text="Waypoint 39", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint40 = self.map_widget.set_marker(33.88217552306324, -117.88342838146785, icon=transparent_icon_image, text="Waypoint 40", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint41 = self.map_widget.set_marker(33.88215963479082, -117.88364528120552, icon=transparent_icon_image, text="Waypoint 41", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint42 = self.map_widget.set_marker(33.882029880455384, -117.88373459286221, icon=transparent_icon_image, text="Waypoint 42", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint43 = self.map_widget.set_marker(33.881603543392536, -117.88385261183714, icon=transparent_icon_image, text="Waypoint 43", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint44 = self.map_widget.set_marker(33.88150556500872, -117.88397701021609, icon=transparent_icon_image, text="Waypoint 44", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder16 = self.map_widget.set_marker(33.88213050628372, -117.8834092432557, icon=image_2, text="650ft", text_color='blue', font=("Helvetica", 17, 'bold'))
        
        path_17 = self.map_widget.set_path([
            ecs.position,
            waypoint38.position,
            waypoint39.position,
            waypoint40.position,
            waypoint41.position,
            waypoint42.position,
            waypoint43.position,
            waypoint44.position,
            ec.position
        ], width=5)


        # # no new waypoints between langsdorf and mccarthy hall
        # path_5 = self.map_widget.set_path([
        #     McCarthy.position,
        #     waypoint25,
        #     waypoint26,
        #     waypoint27,
        #     langsdorf.position
        # ], width=5)

        # # no new waypoints between university hall and mccarthy hall
        path_6 = self.map_widget.set_path([
            McCarthy.position,
            waypoint25.position,
            waypoint26.position,
            waypoint27.position,
            university_hall.position
        ], width=5)

        # # new waypoints between mccarthy hall and pollak libary path 10
        waypoint45 = self.map_widget.set_marker(33.8808469561944, -117.88538026678752, icon=transparent_icon_image, text="Waypoint 45", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint46 = self.map_widget.set_marker(33.880421823506914, -117.88537457696303, icon=transparent_icon_image, text="Waypoint 46", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint47 = self.map_widget.set_marker(33.88015901820872, -117.88541611172404, icon=transparent_icon_image, text="Waypoint 47", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder18 = self.map_widget.set_marker(33.8807108, -117.8853624, icon=transparent_icon_image, text="550ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path_10 = self.map_widget.set_path([
            McCarthy.position,
            waypoint24.position,
            waypoint47.position,
            waypoint46.position,
            waypoint45.position,
            Pollak.position
        ], width=5)

        # # new waypoints between art center and pollak libary path 14
        waypoint48 = self.map_widget.set_marker(33.88147850126386, -117.88576508762874, icon=transparent_icon_image, text="Waypoint 48", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint49 = self.map_widget.set_marker(33.881051546914655, -117.88577287661465, icon=transparent_icon_image, text="Waypoint 49", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint50 = self.map_widget.set_marker(33.88104095459409, -117.88671383871406, icon=transparent_icon_image, text="Waypoint 50", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder19 = self.map_widget.set_marker(33.8810529, -117.8862261, icon=image_2, text="550ft", text_color='blue', font=("Helvetica", 17, 'bold'))
        
        path_14 = self.map_widget.set_path([
            art_center.position,
            waypoint50.position,
            waypoint49.position,
            waypoint48.position,
            Pollak.position
        ], width=5)

        # # new waypoints between rec center and tsu
        waypoint51 = self.map_widget.set_marker(33.882372377291134, -117.88746252669439, icon=transparent_icon_image, text="Waypoint 51", text_color=background_color, font=("Helvetica", tiny_font_size))
        waypoint52 = self.map_widget.set_marker(33.88187984060702, -117.8874370090782, icon=transparent_icon_image, text="Waypoint 52", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder20 = self.map_widget.set_marker(33.8822827, -117.8874599, icon=transparent_icon_image, text="700ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path_22 = self.map_widget.set_path([
            REC_Center.position,
            waypoint3.position,
            waypoint51.position,
            waypoint52.position,
            tsu.position
        ], width=5)

        # # new waypoints between ec and h-s sciences path 26
        waypoint53 = self.map_widget.set_marker(33.880840183281336, -117.88434163034049, icon=transparent_icon_image, text="Waypoint 53", text_color=background_color, font=("Helvetica", tiny_font_size))
        placeholder21 = self.map_widget.set_marker(33.8807520, -117.8842648, icon=transparent_icon_image, text="350ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        path_26 = self.map_widget.set_path([
            ec.position,
            waypoint36.position,
            waypoint53.position,
            h_s_science.position
        ], width=5)
        # path_26 = self.map_widget.set_path([
        #     ec.position,
        #     waypoint36,
        #     waypoint53,
        #     h_s_science.position
        # ], width=5)

        markers = [ mihaylo, langsdorf, university_hall, McCarthy, dan_black, art_center, h_s_science, ec, 
                        Pollak, Visual_Arts, tsu, ecs, REC_Center, Gym, Health_Center, waypoint1, waypoint2, waypoint3, 
                        waypoint4, waypoint5, waypoint6, waypoint7, waypoint8, waypoint9, waypoint10, waypoint11, waypoint12,
                        waypoint13, waypoint14, waypoint15, waypoint16, waypoint17, waypoint18, waypoint19, waypoint20, waypoint21, waypoint22, waypoint23, waypoint24, waypoint25, 
                        waypoint26, waypoint27, waypoint28, waypoint29, waypoint30, waypoint31, waypoint32, waypoint33, waypoint34, waypoint35, waypoint36, waypoint37, waypoint38, 
                        waypoint39, waypoint40, waypoint41, waypoint42, waypoint43, waypoint44, waypoint45, waypoint46, waypoint47, waypoint48, waypoint49, waypoint50, waypoint51, waypoint52, waypoint53]

        # this path is good dont remove or adjust
        path_7 = self.map_widget.set_path([university_hall.position, h_s_science.position],width=5)
        placeholder17 = self.map_widget.set_marker(33.8802421, -117.8841281, icon=transparent_icon_image, text="200ft", text_color='blue', font=("Helvetica", 17, 'bold'))

        
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
