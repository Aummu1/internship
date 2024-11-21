# from jnius import autoclass
# import jnius_config

from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
import requests
import asyncio
import threading
from bleak import BleakScanner
import math
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle, Line, Mesh, Translate
from math import radians, cos, sin
from kivy.core.window import Window

KV = '''
MDBoxLayout:
    orientation: "vertical"  
    MDTopAppBar:
        title: "Bluetooth Application"
        right_action_items: [["theme-light-dark", lambda x: app.switch_theme_style()], ["exit-to-app", lambda x: app.close_application()]]
    MDBottomNavigation:

        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Scanner'
            icon: 'bluetooth'

            MDLabel
                id: Ble
                text: "Bluetooth Scanner"
                size_hint: 0.5, 0.1
                halign: "center"
                bold: True
                font_style: "H4"
                pos_hint: {"center_x": .5, "center_y": .85}

            MDLabel
                id: status
                halign: "center"
                size_hint_y: None
                pos_hint: {"center_x": .5, "center_y": .15}
            
            MDCard:
                ripple_behavior: False
                md_bg_color: app.theme_cls.primary_light
                size_hint: 0.7, 0.3
                pos_hint: {"center_x": .5, "center_y": .6}
                MDLabel
                    id: label
                    theme_text_color: "Custom"
                    size_hint: 0.3, 0.1
                    halign: "center"
                    pos_hint: {"center_x": .5, "center_y": .5}

            MDRectangleFlatButton:
                text: "Start"
                text_color: "black"
                on_press: app.start_service()
                md_bg_color: app.theme_cls.primary_light
                pos_hint: {"center_x": .25, "center_y": .35}

            MDRectangleFlatButton:
                text: "Stop"
                text_color: "black"
                on_press: app.stop_service()
                md_bg_color: app.theme_cls.primary_light
                pos_hint: {"center_x": .75, "center_y": .35}
                
            MDRectangleFlatButton:
                text: "Send"
                text_color: "black"
                on_press: app.send_data()
                md_bg_color: app.theme_cls.primary_light
                pos_hint: {"center_x": .5, "center_y": .35}
                
        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'Map'
            icon: 'map'
            on_tab_press: app.plot_initial_point()  # เรียก

            ScreenManager:
                Screen:
                    name: 'image_screen'
                    
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height  # Allow it to adjust height based on content
        
                        # use MapWidget for map
                        MapWidget:
                            id: map_widget
                            size_hint: (1, None) 
                            height: dp(650)  
                        
                        BoxLayout:
                            orientation: 'horizontal'
                            size_hint_y: None
                            height: "20dp"  # Set height for button row
                            spacing: 40  
                            padding: [10, 10]  
                            
                            # spacer
                            Widget:
                                size_hint_x: 0.2

                            MDRaisedButton:
                                text: "Grid"
                                size_hint_x: None
                                on_release: map_widget.display_grid()
                                
                            MDRaisedButton:
                                text: "Pos."
                                size_hint_x: None
                                on_release: map_widget.toggle_labels()

                            MDRaisedButton:
                                text: "Angle(L)"
                                size_hint_x: None
                                on_release: map_widget.draw_lines_by_angle_L()

                            MDRaisedButton:
                                text: "Angle(R)"
                                size_hint_x: None
                                on_release: map_widget.draw_lines_by_angle_R()
                                
                            # spacer
                            Widget:
                                size_hint_x: 0.2
                
        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'Csi'
            icon: 'access-point-network'
            on_tab_press: app.csi_polygon()  # เรียก
            
            ScreenManager:
                Screen:
                    name: 'csi_screen'
                    
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height  # Allow it to adjust height based on content

                        # บรรทัดนี้บอกว่า MovingWaveShadowWidget อยู่ในหน้า CSI
                        MovingWaveShadowWidget:
                            # id: csi_widget
                            size_hint: (1, None) 
                            height: dp(650)  
                            
        MDBottomNavigationItem:
            name: 'screen 4'
            text: 'Table'
            icon: 'table'
            ScreenManager:
                DemoPage:
                
                ClientsTable:

        MDBottomNavigationItem:
            name: 'screen 5'
            text: 'Info'
            icon: 'information'
            MDCard:
                ripple_behavior: False
                md_bg_color: app.theme_cls.primary_light
                size_hint: 0.5, 0.6
                pos_hint: {"center_x": .5, "center_y": .5}
                MDLabel
                    id: info
                    font_style: "H5"
                    text: "App Info"
                    theme_text_color: "Custom"
                    size_hint: 0.3, 0.1
                    halign: "center"
                    pos_hint: {"center_x": .5, "center_y": .9}
                MDLabel
                    id: info2
                    text: "This Application Using Bleak and ABLE Bluetooth"
                    theme_text_color: "Custom"
                    size_hint: 0.3, 0.1
                    halign: "center"
                    pos_hint: {"center_x": .1, "center_y": .5}
                
<DemoPage>:
    MDRaisedButton:
        text: " Load Table "
        size_hint: 0.5, 0.06
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        on_release: 
            root.manager.current = 'Clientstable'
                
<ClientsTable>:
    name: 'Clientstable'

'''

class DemoPage(Screen):
    pass

sm = ScreenManager()
sm.add_widget(DemoPage(name='demopage'))

# รันบน Window
# if platform == "window":

class MovingWaveShadowWidget(Widget):
    def __init__(self, **kwargs):
        super(MovingWaveShadowWidget, self).__init__(**kwargs)
        self.x_pos = 400  # ตำแหน่งเริ่มต้นของก้อน
        self.y_pos = 300
        self.speed_x = 0.5  # ลดความเร็วในทิศทาง X
        self.speed_y = 0.25  # ลดความเร็วในทิศทาง Y
        self.time = 0  # ใช้สำหรับการทำให้เกิดคลื่น

        with self.canvas:
            # Add map picture
            self.image = Image(source='imagemap.png', allow_stretch=True, keep_ratio=True)

            # ขยายความสูงของภาพให้เต็มหน้าจอ
            self.image.height = Window.height * 0.8  # ตั้งความสูงเป็นขนาดหน้าจอ
            aspect_ratio = self.image.texture_size[0] / self.image.texture_size[1]  # คำนวณอัตราส่วนภาพ
            self.image.width = self.image.height * aspect_ratio  # คำนวณความกว้างตามอัตราส่วน

            # คำนวณตำแหน่งให้อยู่กลางหน้าจอ
            self.image.pos = ((Window.width - self.image.width) / 2, 0)  # ให้ตำแหน่ง x อยู่กลางหน้าจอ

            self.add_widget(self.image)

            # กำหนดตำแหน่งของการเลื่อน
            self.translation = Translate(self.x_pos, self.y_pos)
            
            # ฟังก์ชันสร้าง Mesh สำหรับวงกลม
            def create_circle_mesh(radius, num_points=50):
                vertices = []
                angle_step = 2 * math.pi / num_points
                for i in range(num_points):
                    angle = i * angle_step
                    x = radius * math.cos(angle)
                    y = radius * math.sin(angle)
                    vertices.extend([x, y])
                return vertices

            # เพิ่มเงาจาง ๆ ด้านนอกสุด
            Color(0, 0, 0, 0.2)
            vertices_blur = create_circle_mesh(70)
            self.outer_shadow_blur = Mesh(
                vertices=vertices_blur,
                indices=[i for i in range(len(vertices_blur) // 2)],
                mode='triangle_fan'
            )

            # ชั้นที่ 1: สีด้านนอกสุด
            Color(142 / 255, 174 / 255, 219 / 255)  # น้ำเงิน
            vertices_outer = create_circle_mesh(50)
            self.outer_shadow = Mesh(
                vertices=vertices_outer,
                indices=[i for i in range(len(vertices_outer) // 2)],
                mode='triangle_fan'
            )

            # ชั้นที่ 2: สีชั้นกลาง
            Color(114 / 255, 151 / 255, 207 / 255)  # น้ำเงิน
            vertices_middle = create_circle_mesh(35)
            self.middle_shadow = Mesh(
                vertices=vertices_middle,
                indices=[i for i in range(len(vertices_middle) // 2)],
                mode='triangle_fan'
            )

            # ชั้นที่ 3: สีชั้นในสุด
            Color(84 / 255, 125 / 255, 189 / 255)  # น้ำเงิน
            vertices_inner = create_circle_mesh(20)
            self.inner_shadow = Mesh(
                vertices=vertices_inner,
                indices=[i for i in range(len(vertices_inner) // 2)],
                mode='triangle_fan'
            )

        # ตรวจจับการเปลี่ยนแปลงขนาดของหน้าต่าง
        Window.bind(on_resize=self.update_background)

    def update(self, dt):
        # อัปเดตตำแหน่งของก้อนเงา
        self.x_pos += self.speed_x
        self.y_pos += self.speed_y

        # ตรวจสอบการชนกับขอบหน้าต่าง
        if self.x_pos > Window.width - 60 or self.x_pos < 0:
            self.speed_x = -self.speed_x
        if self.y_pos > Window.height - 60 or self.y_pos < 0:
            self.speed_y = -self.speed_y

        # สร้างคลื่นที่มีการแกว่ง
        self.time += dt
        y_offset = 30 * math.sin(self.time)

        # อัปเดตตำแหน่งการเลื่อน
        self.translation.x = self.x_pos
        self.translation.y = self.y_pos + y_offset

    def update_background(self, *args):
        # อัปเดตขนาดของภาพเมื่อขนาดหน้าต่างเปลี่ยน
        self.image.height = Window.height*0.82  # ตั้งความสูงเป็นขนาดหน้าจอ
        aspect_ratio = self.image.texture_size[0] / self.image.texture_size[1]  # คำนวณอัตราส่วนภาพ
        self.image.width = self.image.height * aspect_ratio  # คำนวณความกว้างตามอัตราส่วน

        # คำนวณตำแหน่งกลางเมื่อขนาดหน้าต่างเปลี่ยน
        self.image.pos = ((Window.width - self.image.width) / 2, 0)



# ------------------------------------------------------------------------------------------------------



class MapWidget(Widget):
    def __init__(self, **kwargs):
        super(MapWidget, self).__init__(**kwargs)
        
        # add map picture
        self.image = Image(source='imagemap.png', allow_stretch=True, keep_ratio=True)
        self.image.size_hint = (None, None)  
        self.image.size = (self.width, self.height) 
        self.image.pos_hint = {"center_x": .5, "top": 0.5}  
        self.add_widget(self.image)
        
        self.labels = []
        self.grid_drawn = False
        self.grid_lines = []
        
        self.angle_drawn_L = False
        self.angle_lines_L = []
        self.angle_drawn_R = False
        self.angle_lines_R = []
        
        self.start_L_x, self.start_L_y = 131, 405
        self.start_R_x, self.start_R_y = 907, 405
        
        # Initialize labels but don't add them to the widget yet
        self.coord_label_L = Label(text=f"(0, 0)", size_hint=(None, None), color=(0, 0, 0, 1), font_size=24)
        self.coord_label_R = Label(text=f"(14.924, 0)", size_hint=(None, None), color=(0, 0, 0, 1), font_size=24)
        self.coord_label_P = Label(text=f"(0, 0)", size_hint=(None, None), color=(1, 0, 0, 1), font_size=24)        

        # use canvas to draw
        with self.canvas:
            # ตั้งสีของกรอบ
            # Color(0, 1, 0, 1)  # สีเขียว
            # วาดเส้นกรอบสี่เหลี่ยมรอบจุด
            # self.rect = Line(rectangle=(131, 345, 776, 990), width=1.5)  
            
            Color(0, 0, 0, 1) # สีดำ
            self.point_A1 = Ellipse(pos=(self.start_L_x-5, self.start_L_y-5), size=(15, 15))  
            self.point_A2 = Ellipse(pos=(self.start_R_x-5, self.start_R_y-5), size=(15, 15))  
            Color(1, 0, 0, 1) # สีแดง
            self.point_Estimate = Ellipse(pos=(100, 100), size=(20, 20))  

    def on_size(self, *args):
        # เมื่อขนาดของ MapWidget เปลี่ยนแปลง จะอัปเดตขนาดของภาพให้เข้ากับ MapWidget
        self.image.size = (self.width, self.height)  # ตั้งขนาดให้เท่ากับขนาดของ MapWidget
        self.image.pos_hint = {"center_x": .5, "top": 0.5} 
        
    def toggle_labels(self):
        if not self.coord_label_L.parent:  # Check if the label is not displayed
            self.coord_label_L.pos = (self.start_L_x - 48, self.start_L_y - 75)
            self.coord_label_R.pos = (self.start_R_x - 48, self.start_R_y - 75)
            self.add_widget(self.coord_label_L)  # Add 
            self.add_widget(self.coord_label_R)
            self.add_widget(self.coord_label_P)
        else:
            self.remove_widget(self.coord_label_L)  # Remove 
            self.remove_widget(self.coord_label_R)
            self.remove_widget(self.coord_label_P)
    
    # Draw the grid
    def display_grid(self):
        if not self.grid_drawn:
            with self.canvas:
                Color(0.5, 0.5, 0.5, 1) # สีดำ
                num_cells_x = int(14.924 / 0.5)
                num_cells_y = int(18.191 / 0.5)
                grid_width = int(776 / num_cells_x) * 2
                grid_height = int(990 / num_cells_y) * 2
                width = 907 #14.924
                height = 1395 #18.191
                
                for x in range(self.start_L_x, width + grid_width, grid_width):
                    line = Line(points=[x, self.start_L_y, x, height + 36], width=1)
                    self.grid_lines.append(line)
                for y in range(self.start_R_y, height + grid_height, grid_height):
                    line = Line(points=[self.start_L_x, y, width + 4, y], width=1)
                    self.grid_lines.append(line)
                
            self.grid_drawn = True
            
        else:
            # Clear all grid lines
            for line in self.grid_lines:
                self.canvas.remove(line)
            self.grid_lines.clear()
            
            self.grid_drawn = False
            
    def draw_lines_by_angle_L(self):
        if not self.angle_drawn_L:
            length_line = 1300

            with self.canvas:
                Color(0, 0, 1, 1)  # สีน้ำเงิน
                for angle in range(0, 100, 10):
                    radians_angle = radians(angle)
                    end_L_x = self.start_L_x + length_line * cos(radians_angle)  
                    end_L_y = self.start_L_y + length_line * sin(radians_angle)
                    line = Line(points=[self.start_L_x, self.start_L_y, end_L_x, end_L_y], width=1)
                    self.angle_lines_L.append(line)
            
            self.angle_drawn_L = True
        else:
            # Clear all angle lines
            for line in self.angle_lines_L:
                self.canvas.remove(line)
            self.angle_lines_L.clear()
            self.angle_drawn_L = False
            
    def draw_lines_by_angle_R(self):
        if not self.angle_drawn_R:
            length_line = 1300
                    
            with self.canvas:
                Color(1, 0, 1, 1) # สีม่วง
                for angle in range(0, 100, 10):
                    radians_angle = radians(angle)
                    end_R_x = self.start_R_x - length_line * cos(radians_angle)  
                    end_R_y = self.start_R_y + length_line * sin(radians_angle)
                    line = Line(points=[self.start_R_x+4, self.start_R_y, end_R_x+4, end_R_y], width=1)
                    self.angle_lines_R.append(line)
            
            self.angle_drawn_R = True
        else:
            # Clear all angle lines
            for line in self.angle_lines_R:
                self.canvas.remove(line)
            self.angle_lines_R.clear()
            self.angle_drawn_R = False
            
    # ฟังก์ชันสำหรับพล็อตจุดใหม่
    def plot_point(self, x, y, real_coord):
        # อัปเดตพิกัดของจุด
        self.point_Estimate.pos = (x-10, y-15)
        
            # Update the label estimated coordinates
        self.coord_label_P.text = f"({real_coord[0]}, {real_coord[1]})"
        self.coord_label_P.pos = (x-48, y-78)

# -------------------------------------------------------------------------------------------------

class ClientsTable(Screen):
    def load_table(self):
        layout = AnchorLayout()
        devices = asyncio.run(self.async_scan_devices())
        for device in devices:
            name = device.name
            rssi = device.rssi
            if name in self.target_device_names:
                self.data_tables = MDDataTable(
                    pos_hint={'center_y': 0.5, 'center_x': 0.5},
                    size_hint=(0.6, 0.8),
                    use_pagination=True,
                    check=True,
                    column_data=[
                        ("No.", dp(30)),
                        ("Name", dp(30)),
                        ("RSSI", dp(30)), ],
                    row_data=[
                        (f"{i + 1}", f"{name}", f"{rssi}")
                        for i in range(5)], )
        self.add_widget(self.data_tables)
        return layout
        
        # bluetooth name 
    async def async_scan_devices(self):
        scanner = BleakScanner()
        self.target_device_names = ["P2N_09725", "P2N_09714", "ZLB_39612"]
        scanner.device_filter = lambda device: device.name in self.target_device_names
        return await scanner.discover()

    def on_enter(self):
        self.load_table()

sm = ScreenManager()
sm.add_widget(DemoPage(name='demopage'))
sm.add_widget(ClientsTable(name='Clientstable'))

# ---------------------------------------------------------------------------------------------------

class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Pink"
        self.scanning = False
        self.target_device_names = ["P2N_09725", "P2N_09714", "ZLB_39612"]
        return Builder.load_string(KV)
    
    def switch_theme_style(self):
        self.theme_cls.primary_palette = ("Pink" if self.theme_cls.primary_palette == "Blue" else "Blue")
        self.theme_cls.theme_style = ("Dark" if self.theme_cls.theme_style == "Light" else "Light")

    def close_application(self):
        App.get_running_app().stop()

    # ตรวจสอบว่าขณะนี้กำลังสแกนอุปกรณ์ Bluetooth อยู่หรือไม่ (self.scanning) ถ้าไม่กำลังสแกน จะเริ่มกระบวนการสแกน
    def start_service(self):
        if not self.scanning:
            self.root.ids.label.text = ""  # Clear the previous scan results
            self.scanning = True
            Logger.info('Bluetooth: Scanning...')
            threading.Thread(target=self.scan_devices).start()

    def scan_devices(self):
        self.root.ids.status.text = "Scanning..."
        devices = asyncio.run(self.async_scan_devices()) # เรียกใช้ฟังก์ชัน async_scan_devices ซึ่งเป็นฟังก์ชันแบบ Asynchronous ผ่าน asyncio.run เพื่อค้นหาอุปกรณ์
        Clock.schedule_once(lambda dt: self.display_scan_results(devices), 0)
        self.scanning = False

    # สร้างอินสแตนซ์ของ BleakScanner ซึ่งใช้สำหรับค้นหาอุปกรณ์ Bluetooth LE
    async def async_scan_devices(self):
        scanner = BleakScanner()
        # ตั้งค่าฟิลเตอร์ device_filter เพื่อกรองเฉพาะอุปกรณ์ที่มีชื่ออยู่ใน self.target_device_names
        scanner.device_filter = lambda device: device.name in self.target_device_names 
        return await scanner.discover() # เริ่มการสแกนอุปกรณ์ Bluetooth และรอจนกว่าการค้นหาจะเสร็จสิ้น
    
    # คำนวณ ระยะทาง จากค่า RSSI ที่ได้รับจากอุปกรณ์ Bluetooth.
    def calculate_distance(self, rssi, RSSI_0, n):
        ratio = (RSSI_0-rssi)/(10*n)
        return math.pow(10,ratio)
    
    # เพื่อหาตำแหน่ง (x, y) ของจุดที่ไม่ทราบตำแหน่ง โดยใช้ข้อมูลจากระยะทางจาก สามจุดที่มีตำแหน่งที่รู้
    # d1, d2, d3: ระยะทางจากแต่ละจุด (จากอุปกรณ์ที่รู้ตำแหน่งไปยังจุดที่เราต้องการหาตำแหน่ง)
    # x1, y1, x2, y2, x3, y3: พิกัด (x, y) ของสามจุดที่รู้ตำแหน่ง ซึ่งจะใช้ในการคำนวณหาตำแหน่งของจุดที่ไม่ทราบตำแหน่ง
    
    def trilateration(self, d1, d2, d3, x1, y1, x2, y2, x3, y3): 
            A = x1**2 + y1**2 - d1**2
            B = x2**2 + y2**2 - d2**2
            C = x3**2 + y3**2 - d3**2

            X32 = x3 - x2
            X13 = x1 - x3
            X21 = x2 - x1

            Y32 = y3 - y2
            Y13 = y1 - y3
            Y21 = y2 - y1

            xe = (A * Y32 + B * Y13 + C * Y21) / (2 * (x1 * Y32 + x2 * Y13 + x3 * Y21))
            ye = (A * X32 + B * X13 + C * X21) / (2 * (y1 * X32 + y2 * X13 + y3 * X21))

            return xe, ye
    
    def display_scan_results(self, devices):
        self.scanned_devices = []  # ล้างข้อมูลอุปกรณ์ที่สแกนก่อนหน้านี้
        scanned_info = ''
        n = 2

        # RSSI_0 values for each anchor
        RSSI_0_values = {
            "P2N_09714": -51,
            "P2N_09725": -54,
            "ZLB_39612": -51
        }
        
        # กำหนด anchors และตำแหน่ง
        anchors = {
            "P2N_09714": (3.506, 2.382),
            "P2N_09725": (0, 11.244),
            "ZLB_39612": (5.725, 9.955)
        }
        
        # สร้างรายการเพื่อเก็บค่า RSSI และระยะทางที่คำนวณได้
        distances = []
        rssi_values = []
        positions = []

        for device in devices:
            name = device.name
            if name in anchors:  # ตรวจสอบว่าอุปกรณ์เป็น anchor ที่กำหนด
                rssi = device.rssi
                RSSI_0 = RSSI_0_values[name]  
                distance = self.calculate_distance(rssi, RSSI_0, n)
                distances.append(distance)
                rssi_values.append(rssi)
                positions.append(anchors[name])

                scanned_info += f"{name}, RSSI: {rssi} dBm, Distance: {distance:.2f} m\n"
                self.scanned_devices.append({"name": name, "rssi": rssi, "distance": distance})

        # ตรวจสอบว่ามีค่าระยะทางครบสามค่าเพื่อคำนวณ trilateration
        if len(distances) >= 3:
            x1, y1 = positions[0]
            x2, y2 = positions[1]
            x3, y3 = positions[2]
            d1, d2, d3 = distances[0], distances[1], distances[2]

            x, y = self.trilateration(d1, d2, d3, x1, y1, x2, y2, x3, y3)
            scanned_info += f"positions: ({x:.3f}, {y:.3f})\n"

            self.scanned_devices.append({"name": "Trilateration Result", "position": (x, y)})
            
        self.root.ids.label.text = scanned_info
        self.root.ids.status.text = "Scan Complete"
        Logger.info('Bluetooth: ' + '\n' + scanned_info)
        
    def calculate_real_to_pixel(self, x_real, y_real):
        origin_x = 131 
        origin_y = 405 
        width = 776 
        height = 990 
        real_width = 14.924 
        real_height = 18.191
        
        scale_x = width / real_width  # อัตราส่วนพิกเซลต่อเมตรในแนวนอน
        scale_y = height / real_height  # อัตราส่วนพิกเซลต่อเมตรในแนวตั้ง

        # แปลงพิกัดจริงเป็นพิกัดพิกเซล
        x_pixel = origin_x + (x_real * (scale_x))
        y_pixel = origin_y + (y_real * (scale_y))

        return x_pixel, y_pixel
    
    def plot_initial_point(self):
        # พิกัดจริงที่ต้องการแปลง
        real_coordinate = (8.75, 16)
        map_coordinate = self.calculate_real_to_pixel(*real_coordinate)    

        # พล็อตจุดที่ตำแหน่ง
        map_widget = self.root.ids.map_widget
        map_widget.plot_point(*map_coordinate, real_coordinate) 
    
    def csi_polygon(self):
        widget = MovingWaveShadowWidget()
        Clock.schedule_interval(widget.update, 1 / 60)  # อัปเดตทุก 1/60 วินาที
        return widget

    def send_data(self):
        self.scanning = False
        self.root.ids.status.text = "Sending data..."
        for device in self.scan_devices: #scanned_devices
            # Check if "rssi" key exists in the device dictionary
            if "rssi" in device:
                rssi = device["rssi"]
            else:
                rssi = None
        
            # Check if "position" key exists in the device dictionary
            if "position" in device:
                x, y = device["position"]
                self.send_data_to_api(device["name"], rssi, device.get("distance", None), x, y)
            else:
                self.send_data_to_api(device["name"], rssi, device.get("distance", None))
                
        self.root.ids.status.text = "Send data Complete"
        Logger.info('Bluetooth: Send data Complete')
        
    def send_data_to_api(self, name, rssi, distance, x=None, y=None):
        url = "http://192.168.100.49:5000/Input"  # Replace with your actual API endpoint
        if distance is not None:
            distance = "%.3f" % distance
        else:
            distance = None
            
        if x is not None and y is not None:
            x = "%.3f" % x
            y = "%.3f" % y
        else:
            x = None
            y = None
            
        data = {
            "anc_name": name,
            "rssi": rssi,
            "distance": distance,
            "x": x,
            "y": y
        }
    
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            Logger.info(f'Successfully sent data to API: {response.json()}')
        except requests.exceptions.HTTPError as http_err:
            Logger.error(f'HTTP error occurred: {http_err}')
        except Exception as err:
            Logger.error(f'Other error occurred: {err}')
            
    def stop_service(self):
        self.scanning = False
        self.root.ids.status.text = "Stop Scanning"
        Logger.info('Bluetooth: Stop Scanning')
            
if __name__ == "__main__":
    MyApp().run()

# รันบนมือถือ Android
# if platform == "android":
#     from able import GATT_SUCCESS, BluetoothDispatcher, require_bluetooth_enabled
#     jnius_config.set_classpath('org/able/BLE.jar')
#     jnius_config.set_classpath('org/able/BLEAdvertiser.jar')
#     jnius_config.set_classpath('org/able/PythonBluetooth.jar')
#     jnius_config.set_classpath('org/able/PythonBluetoothAdvertiser.jar')
#     autoclass('org.able.BLE')
#     autoclass('org.able.BLEAdvertiser')
#     autoclass('org.able.PythonBluetooth')
#     autoclass('org.able.PythonBluetoothAdvertiser')
    
#     class MovingWaveShadowWidget(Widget):
#         def __init__(self, **kwargs):
#             super(MovingWaveShadowWidget, self).__init__(**kwargs)
#             self.x_pos = 500  # ตำแหน่งเริ่มต้นของก้อน
#             self.y_pos = 500
#             self.speed_x = 0.5  # ลดความเร็วในทิศทาง X
#             self.speed_y = 0.25  # ลดความเร็วในทิศทาง Y
#             self.time = 0  # ใช้สำหรับการทำให้เกิดคลื่น

#             with self.canvas:
#                 # พื้นหลังสีเทา
#                 Color(0.5, 0.5, 0.5, 1)  # สีเทา
#                 self.background = Rectangle(size=Window.size)

#                 # กำหนดตำแหน่งของการเลื่อน
#                 self.translation = Translate(self.x_pos, self.y_pos)
                
#                 # ฟังก์ชันสร้าง Mesh สำหรับวงกลม
#                 def create_circle_mesh(radius, num_points=50):
#                     vertices = []
#                     angle_step = 2 * math.pi / num_points
#                     for i in range(num_points):
#                         angle = i * angle_step
#                         x = radius * math.cos(angle)
#                         y = radius * math.sin(angle)
#                         vertices.extend([x, y])
#                     return vertices

#                 # เพิ่มเงาจาง ๆ ด้านนอกสุด
#                 # Color(0, 0, 0, 0.2)
#                 # vertices_blur = create_circle_mesh(70)
#                 # self.outer_shadow_blur = Mesh(
#                 #     vertices=vertices_blur,
#                 #     indices=[i for i in range(len(vertices_blur) // 2)],
#                 #     mode='triangle_fan'
#                 # )

#                 # ชั้นที่ 1: สีด้านนอกสุด
#                 # Color(1, 0, 0, 0.5) #แดง
#                 Color(142 / 255, 174 / 255, 219 / 255) #น้ำเงิน
#                 vertices_outer = create_circle_mesh(60)
#                 self.outer_shadow = Mesh(
#                     vertices=vertices_outer,
#                     indices=[i for i in range(len(vertices_outer) // 2)],
#                     mode='triangle_fan'
#                 )

#                 # ชั้นที่ 2: สีชั้นกลาง
#                 # Color(0, 1, 0, 0.5) #เขียว
#                 Color(114 / 255, 151 / 255, 207 / 255) #น้ำเงิน
#                 vertices_middle = create_circle_mesh(45)
#                 self.middle_shadow = Mesh(
#                     vertices=vertices_middle,
#                     indices=[i for i in range(len(vertices_middle) // 2)],
#                     mode='triangle_fan'
#                 )

#                 # ชั้นที่ 3: สีชั้นในสุด
#                 Color(84 / 255, 125 / 255, 189 / 255) #น้ำเงิน
#                 vertices_inner = create_circle_mesh(30)
#                 self.inner_shadow = Mesh(
#                     vertices=vertices_inner,
#                     indices=[i for i in range(len(vertices_inner) // 2)],
#                     mode='triangle_fan'
#                 )

#             # ตรวจจับการเปลี่ยนแปลงขนาดของหน้าต่าง
#             Window.bind(on_resize=self.update_background)

#         def update(self, dt):
#             # อัปเดตตำแหน่งของก้อนเงา
#             self.x_pos += self.speed_x
#             self.y_pos += self.speed_y

#             # ตรวจสอบการชนกับขอบหน้าต่าง
#             if self.x_pos > Window.width - 60 or self.x_pos < 0:
#                 self.speed_x = -self.speed_x
#             if self.y_pos > Window.height - 60 or self.y_pos < 0:
#                 self.speed_y = -self.speed_y

#             # สร้างคลื่นที่มีการแกว่ง
#             self.time += dt
#             y_offset = 30 * math.sin(self.time)

#             # อัปเดตตำแหน่งการเลื่อน
#             self.translation.x = self.x_pos
#             self.translation.y = self.y_pos + y_offset

#         def update_background(self, *args):
#             # อัปเดตขนาดของพื้นหลังเมื่อขนาดหน้าต่างเปลี่ยน
#             self.background.size = Window.size

#     class MapWidget(Widget):
#         def __init__(self, **kwargs):
#             super(MapWidget, self).__init__(**kwargs)
            
#             # เพิ่มภาพแผนที่
#             self.image = Image(source='imagemap.png', allow_stretch=True, keep_ratio=True)
#             self.image.size_hint = (None, None)  # ให้สามารถกำหนดขนาดได้เอง
#             self.image.size = (self.width, self.height)  # ตั้งขนาดให้เท่ากับขนาดของ MapWidget
#             self.image.pos_hint = {"center_x": .5, "top": 0.5}  
#             self.add_widget(self.image)
            
#             self.labels = []
#             self.grid_drawn = False
#             self.grid_lines = []
            
#             self.angle_drawn_L = False
#             self.angle_lines_L = []
#             self.angle_drawn_R = False
#             self.angle_lines_R = []
            
#             self.start_L_x, self.start_L_y = 131, 405
#             self.start_R_x, self.start_R_y = 907, 405
            
#             # Initialize labels but don't add them to the widget yet
#             self.coord_label_L = Label(text=f"(0, 0)", size_hint=(None, None), color=(0, 0, 0, 1), font_size=24)
#             self.coord_label_R = Label(text=f"(14.924, 0)", size_hint=(None, None), color=(0, 0, 0, 1), font_size=24)
#             self.coord_label_P = Label(text=f"(0, 0)", size_hint=(None, None), color=(1, 0, 0, 1), font_size=24)        

#             # use canvas to draw
#             with self.canvas:
#                 # ตั้งสีของกรอบ
#                 # Color(0, 1, 0, 1)  # สีเขียว
#                 # วาดเส้นกรอบสี่เหลี่ยมรอบจุด
#                 # self.rect = Line(rectangle=(131, 345, 776, 990), width=1.5)  
                
#                 Color(0, 0, 0, 1) # สีดำ
#                 self.point_A1 = Ellipse(pos=(self.start_L_x-5, self.start_L_y-5), size=(15, 15))  
#                 self.point_A2 = Ellipse(pos=(self.start_R_x-5, self.start_R_y-5), size=(15, 15))  
#                 Color(1, 0, 0, 1) # สีแดง
#                 self.point_Estimate = Ellipse(pos=(100, 100), size=(20, 20))  
    
#         def on_size(self, *args):
#             # เมื่อขนาดของ MapWidget เปลี่ยนแปลง จะอัปเดตขนาดของภาพให้เข้ากับ MapWidget
#             self.image.size = (self.width, self.height)  # ตั้งขนาดให้เท่ากับขนาดของ MapWidget
#             self.image.pos_hint = {"center_x": .5, "top": 0.5} 
            
#         def toggle_labels(self):
#             if not self.coord_label_L.parent:  # Check if the label is not displayed
#                 self.coord_label_L.pos = (self.start_L_x - 48, self.start_L_y - 75)
#                 self.coord_label_R.pos = (self.start_R_x - 48, self.start_R_y - 75)
#                 self.add_widget(self.coord_label_L)  # Add labels when toggled on
#                 self.add_widget(self.coord_label_R)
#                 self.add_widget(self.coord_label_P)
#             else:
#                 self.remove_widget(self.coord_label_L)  # Remove when toggled off
#                 self.remove_widget(self.coord_label_R)
#                 self.remove_widget(self.coord_label_P)
        
#         # Draw the grid
#         def display_grid(self):
#             if not self.grid_drawn:
#                 with self.canvas:
#                     Color(0.5, 0.5, 0.5, 1) # สีดำ
#                     num_cells_x = int(14.924 / 0.5)
#                     num_cells_y = int(18.191 / 0.5)
#                     grid_width = int(776 / num_cells_x) * 2
#                     grid_height = int(990 / num_cells_y) * 2
#                     width = 907 #14.924
#                     height = 1395 #18.191
                    
#                     for x in range(self.start_L_x, width + grid_width, grid_width):
#                         line = Line(points=[x, self.start_L_y, x, height + 36], width=1)
#                         self.grid_lines.append(line)
#                     for y in range(self.start_R_y, height + grid_height, grid_height):
#                         line = Line(points=[self.start_L_x, y, width + 4, y], width=1)
#                         self.grid_lines.append(line)
                    
#                 self.grid_drawn = True
                
#             else:
#                 # Clear all grid lines
#                 for line in self.grid_lines:
#                     self.canvas.remove(line)
#                 self.grid_lines.clear()
                
#                 self.grid_drawn = False
                
#         def draw_lines_by_angle_L(self):
#             if not self.angle_drawn_L:
#                 length_line = 1300

#                 with self.canvas:
#                     Color(0, 0, 1, 1)  # สีน้ำเงิน
#                     for angle in range(0, 100, 10):
#                         radians_angle = radians(angle)
#                         end_L_x = self.start_L_x + length_line * cos(radians_angle)  
#                         end_L_y = self.start_L_y + length_line * sin(radians_angle)
#                         line = Line(points=[self.start_L_x, self.start_L_y, end_L_x, end_L_y], width=1)
#                         self.angle_lines_L.append(line)
                
#                 self.angle_drawn_L = True
#             else:
#                 # Clear all angle lines
#                 for line in self.angle_lines_L:
#                     self.canvas.remove(line)
#                 self.angle_lines_L.clear()
#                 self.angle_drawn_L = False
                
#         def draw_lines_by_angle_R(self):
#             if not self.angle_drawn_R:
#                 length_line = 1300
                        
#                 with self.canvas:
#                     Color(1, 0, 1, 1) # สีม่วง
#                     for angle in range(0, 100, 10):
#                         radians_angle = radians(angle)
#                         end_R_x = self.start_R_x - length_line * cos(radians_angle)  
#                         end_R_y = self.start_R_y + length_line * sin(radians_angle)
#                         line = Line(points=[self.start_R_x+4, self.start_R_y, end_R_x+4, end_R_y], width=1)
#                         self.angle_lines_R.append(line)
                
#                 self.angle_drawn_R = True
#             else:
#                 # Clear all angle lines
#                 for line in self.angle_lines_R:
#                     self.canvas.remove(line)
#                 self.angle_lines_R.clear()
#                 self.angle_drawn_R = False
                
#         # ฟังก์ชันสำหรับพล็อตจุดใหม่
#         def plot_point(self, x, y, real_coord):
#             # อัปเดตพิกัดของจุด
#             self.point_Estimate.pos = (x-10, y-15)
            
#              # Update the label estimated coordinates
#             self.coord_label_P.text = f"({real_coord[0]}, {real_coord[1]})"
#             self.coord_label_P.pos = (x-48, y-78)
            
#     class ClientsTable(Screen):
#         def load_table(self):
#             while True:
#                 layout = AnchorLayout()
#                 self.data_tables = MDDataTable(
#                     pos_hint={'center_y': 0.5, 'center_x': 0.5},
#                     size_hint=(0.6, 0.6),
#                     use_pagination=True,
#                     check=True,
#                     column_data=[
#                         ("No.", dp(30)),
#                         ("Name", dp(30)),
#                         ("RSSI", dp(30)), ],
#                     row_data=[
#                         (f"{i + 1}", "{name}", "{rssi}")
#                         for i in range(20)], )
#                 self.add_widget(self.data_tables)
#                 return layout

#         def on_enter(self):
#             self.load_table()

#     sm.add_widget(ClientsTable(name='Clientstable'))

#     class DeviceDispatcher(BluetoothDispatcher):
#         def __init__(self, device, rssi, uuid, major, minor):
#             super().__init__()
#             self._device = device
#             self._address: str = device.getAddress()
#             self._name: str = device.getName() or ""
#             self._rssi: int = rssi
#             self._uuid: str = uuid  # Store the UUID
#             self._major: str = major # Store the Major
#             self._minor: str = minor # Store the Minor

#         @property
#         def title(self) -> str:
#             return f"<{self._address}><{self._name}><{self._uuid}><{self._major}"

#         def on_connection_state_change(self, status: int, state: int):
#             if status == GATT_SUCCESS and state:
#                 Logger.info(f"Device: {self.title} connected")
#             else:
#                 Logger.info(f"Device: {self.title} disconnected. {status=}, {state=}")
#                 # self.close_gatt()
#                 if status == 133:
#                     # Retry connection after delay
#                     Clock.schedule_once(lambda dt: self.reconnect(), 5)
#                 Logger.info(f"Scan <{self._name}> Complete")
#                 # Clock.schedule_once(callback=lambda dt: self.reconnect(), timeout=15)

#         def on_rssi_updated(self, rssi: int, status: int):
#             Logger.info(f"Device: {self.title} RSSI: {rssi}")
#             # self.send_data_to_api(self._name, rssi)
#             # Clock.schedule_once(lambda dt: self.update_ui(self._name, rssi), 0)  # Schedule UI update

#         def periodically_update_rssi(self):
#             """
#             Clock callback to read
#             the signal strength indicator for a connected device.
#             """
#             if self.gatt:  # if device is connected
#                 try:
#                     self.update_rssi()
#                 except Exception as e:
#                     Logger.error(f"Failed to update RSSI: {e}")

#         def reconnect(self):
#             Logger.info(f"Device: {self.title} try to reconnect ...")
#             self.connect_gatt(self._device)

#         def start(self):
#             """Start connection to device."""
            
#             if not self.gatt:
#                 self.connect_gatt(self._device)
#             Clock.schedule_interval(callback=lambda dt: self.periodically_update_rssi(), timeout=5)
            
#         def update_ui(self, name, rssi):
#             scanned_info = f"{name}, RSSI: {rssi} dBm\n, UUID: {self._uuid}, Major: {self._major}, Minor: {self._minor}"
#             app = App.get_running_app()
#             current_text = app.root.ids.label.text
#             # app.root.ids.label.text = current_text + scanned_info  # เพิ่มข้อมูลใหม่

#     class ScannerDispatcher(BluetoothDispatcher):
#         def __init__(self,target_filters=None):
#             super().__init__()
#             # Stores connected devices addresses
#             self._devices = {}
#             self.device = None
#             # self.target_uuids = target_uuids if target_uuids is not None else []
#             self.target_filters = target_filters if target_filters is not None else []

#         def on_scan_started(self, success: bool):
#             Logger.info(f"Scan: started {'successfully' if success else 'unsuccessfully'}")
#             if not success:
#                 App.get_running_app().root.ids.status.text = "Pls restart. Scan unsuccessfully"
            
#         def start_scan(self):
#             # Start Scan Bluetooth Hear
#             super().start_scan()  # Call the scan method from the parent class.
            
#         def stop_scan(self):
#             super().stop_scan()
#             Logger.info("Stop: completed")

#         def on_scan_completed(self):
#             if self.device:
#                 self.connect_gatt(self.device)  # connect to device
#                 Logger.info("Scan: completed")
#                 # self.clear_devices()
                    
#         def on_device(self, device, rssi, advertisement):
#             address = device.getAddress()
#             name = device.getName()
#             data = advertisement.data
#             parsed_data = list(advertisement.parse(data)) 
#             uuid = None
#             major = None
#             minor = None
            
#             for item in parsed_data:
#                 if item.ad_type == 9: #name
#                     name = item.data.decode('utf-8')  # convert to string
#                 elif item.ad_type == 255:  #UUID
#                     data_hex = item.data.hex()  #hex string
#                     uuid_hex = data_hex[8:40]
#                     # uuid = f"{uuid_hex[:8]}-{uuid_hex[8:12]}-{uuid_hex[12:16]}-{uuid_hex[16:20]}-{uuid_hex[20:]}"
#                     uuid = uuid_hex
#                     # if uuid not in self.target_uuids:
#                     #     # Logger.info(f"Skipping device with UUID {uuid} as it doesn't match target UUIDs.")
#                     #     return  # if uuid is not match out of function

#                     major_hex = data_hex[40:44] #2 bytes (4 digit)at 25-28
#                     minor_hex = data_hex[44:48] #2 bytes (4 digit)at 29-32
#                     #convert Major and Minor to base 10 or decimal
#                     if major_hex and minor_hex:
#                         major = int(major_hex, 16)
#                         minor = int(minor_hex, 16)

#                     # tx_power_hex = data_hex[48:50] #1 byte (2 digit)at 33 
#                     #convert TX Power to signed integer
#                     #tx_power = int(tx_power_hex, 16) - 256 if int(tx_power_hex, 16) > 127 else int(tx_power_hex, 16)
            
#             Logger.info(f"Discovered device with UUID: {uuid} and Major: {major}")        
#             # if uuid in self.target_uuids:
#             if any(filter.get("uuid") == uuid and filter.get("major") == major for filter in self.target_filters):
#                 App.get_running_app().update_found_data(uuid, major, rssi)
#             # if uuid and major in self.target_filters:
#                 if major not in self._devices:
#                     # Create dispatcher instance for a new device
#                     dispatcher = DeviceDispatcher(device, rssi, uuid, major, minor)
#                     # Remember address,
#                     # to avoid multiple dispatchers creation for this device
#                     self._devices[address] = dispatcher
#                     Logger.info(f"Scan: device <{name}> address <{address}> added with UUID <{uuid}> and Major <{major}>")
#                     dispatcher.start()
                    
#                 self.device = device
#                 # self.stop_scan()  
                
#             else:
#                 # Logger.info(f"UUID {uuid} does not match target UUIDs.")
#                 return
                    
#             # if name and (name.startswith('P2N') or name.startswith('ZLB')):
#             #     # Clock.schedule_once(lambda dt: self.update_ui(name, rssi, timestamp), 0)  # Schedule UI update
#             #     self.device = device
#             self.stop_scan()
#             return name
        
#         def clear_devices(self):
#             self._devices.clear()  

#     class MyApp(MDApp,BluetoothDispatcher):
#         def build(self):
#             self.theme_cls.theme_style = "Dark"
#             self.theme_cls.primary_palette = "Amber"
#             self.target_device_names = ["P2N_09725", "P2N_09714", "ZLB_39612"]
#             self.scan_results = []  
#             self.target_data_set = [
#                 # {"uuid": "4e543f43cdb34bbe87948a08bb2681db", "major": 888},
#                 # {"uuid": "4e543f43cdb34bbe87948a08bb2681db", "major": 111},
#                 {"uuid": "d8ac484e4fbb4b36bf12c249ab83673b", "major": 888},
#                 {"uuid": "d8ac484e4fbb4b36bf12c249ab83673b", "major": 111},
#                 {"uuid": "ab8190d5d11e4941acc442f30510b408", "major": 10021}
#             ]
#             self.found_data = set()  # To track found data
#             return Builder.load_string(KV)

#         def switch_theme_style(self):
#             self.theme_cls.primary_palette = (
#                 "Orange" if self.theme_cls.primary_palette == "Blue" else "Blue"
#             )
#             self.theme_cls.theme_style = (
#                 "Dark" if self.theme_cls.theme_style == "Light" else "Light"
#             )

#         def close_application(self):
#             App.get_running_app().stop()

#         @property
#         def service(self):
#             return autoclass("test.able.scanservice.ServiceAble")

#         @property
#         def activity(self):
#             return autoclass("org.kivy.android.PythonActivity").mActivity

#         @require_bluetooth_enabled
#         def start_service(self, loop_count=0):
#             # Check if Bluetooth is enabled
#             if not self.is_bluetooth_enabled():
#                 self.request_bluetooth_enable()
#                 return
            
#             Logger.info(f"loop_count: {loop_count}")
                    
#             self.service.start(self.activity, "")
#             Logger.info("Service started.")

#             self.scanner_dispatcher = ScannerDispatcher(target_filters=self.target_data_set)
#             Logger.info("Starting scan...")

#             self.root.ids.status.text = "Scanning..."
#             self.root.ids.label.text = ""  # Clear previous data before new scan
            
#             # Start the scanning process
#             self.scan_for_data()
        
#         def scan_for_data(self):
#             self.scanner_dispatcher.start_scan()
#             Clock.schedule_once(self.check_scan_results, 5)  # Schedule to check results after 20 seconds

#         def check_scan_results(self, dt):
#             # print("found_data:", self.found_data)
#             # print("target_data_set:", self.target_data_set)
            
#             # ดึงแค่ uuid และ major จาก found_data
#             found_data_filtered = {(d[0], d[1]) for d in self.found_data}
#             # ดึงแค่ uuid และ major จาก target_data_set
#             target_data_filtered = {(d['uuid'], d['major']) for d in self.target_data_set}
            
#             # Check if we found all target data
#             if found_data_filtered == target_data_filtered:
#                 Logger.info("All target data found.")
#                 self.root.ids.status.text = "All target data found. Stopping scan."
#                 self.scanner_dispatcher.stop_scan()  # Stop scanning
#                 self.update_scan_results(self.found_data)
#                 # Set a flag to prevent re-scanning
#                 self.scanning = False
#             else:
#                 Logger.info("Not all target data found. Restarting scan...")
#                 # Restart scan
#                 # self.found_data.clear()  # Clear found data for the next scan
#                 self.scan_for_data()  # Scan again

#         def update_found_data(self, uuid, major, rssi):
#             if rssi != 127:
#                 # Update found data based on UUID and Major
#                 # data_tuple = (uuid, major, rssi)
                
#                 # ตรวจสอบเฉพาะ UUID และ Major
#                 data_tuple = (uuid, major)
                
#                 # if data_tuple not in self.found_data:
#                 if data_tuple not in {(d[0], d[1]) for d in self.found_data}:
#                     # self.found_data.add(data_tuple)
#                     self.found_data.add((uuid, major, rssi))
#                     Logger.info(f"Updated found data: {self.found_data}")
#                 # self.found_data.add((uuid, major))
#                 # Logger.info(f"Found data updated: {self.found_data}")

#         def update_scan_results(self, found_data):
#             Logger.info(f"All target data has been successfully collected")
#             # self.scan_results = list(scanner_dispatcher._devices.values())
#             self.scan_results = list(self.found_data)
#             if self.scan_results:
#                 self.display_scan_results()
#                 self.found_data.clear()
#             self.root.ids.status.text = "Scan Complete"
#             self.scanning = False
            
#         def calculate_real_to_pixel(self, x_real, y_real):
#             origin_x = 131 
#             origin_y = 405 
#             width = 776 
#             height = 990 
#             real_width = 14.924 
#             real_height = 18.191
            
#             scale_x = width / real_width  # อัตราส่วนพิกเซลต่อเมตรในแนวนอน
#             scale_y = height / real_height  # อัตราส่วนพิกเซลต่อเมตรในแนวตั้ง

#             # แปลงพิกัดจริงเป็นพิกัดพิกเซล
#             x_pixel = origin_x + (x_real * (scale_x))
#             y_pixel = origin_y + (y_real * (scale_y))

#             return x_pixel, y_pixel
        
#         def plot_initial_point(self):
#             # พิกัดจริงที่ต้องการแปลง
#             real_coordinate = (8.75, 16)
#             map_coordinate = self.calculate_real_to_pixel(*real_coordinate)    

#             # พล็อตจุดที่ตำแหน่ง
#             map_widget = self.root.ids.map_widget
#             map_widget.plot_point(*map_coordinate, real_coordinate) 
#             # return MapWidget()
            
#         def csi_polygon(self):
#             widget = MovingWaveShadowWidget()
#             Clock.schedule_interval(widget.update, 1 / 60)  # อัปเดตทุก 1/60 วินาที
#             return widget

#         def display_scan_results(self):
#             self.scanned_devices = []
#             scanned_info = ''

#             for uuid, major, rssi in self.scan_results:
#                 # Logger.info(f"Result: devices: {device}")
#                 # name = device._name
#                 # uuid = device.uuid
#                 # major = device.major
#                 # minor = device._minor
                
#                 if uuid == None:
#                     scanned_info = f"Don't have any Device is Match"
#                 else:
#                     # rssi = device._rssi
#                     if uuid == "4e543f43cdb34bbe87948a08bb2681db":
#                         name = "1"
#                         uuid1 = "4e543f43cdb34bbe..."
#                         # scanned_info += f"A: {name}, RSSI: {rssi} dBm,\n UUID: {uuid1},\n Major: {major}\n"
#                         scanned_info += f"A: {name}, RSSI: {rssi} dBm,\n Major: {major}\n"
                        
#                     elif uuid == "d8ac484e4fbb4b36bf12c249ab83673b" and major == 888:
#                         name = "202"
#                         uuid2 = "d8ac484e4fbb4b36..."
#                         # scanned_info += f"A: {name}, RSSI: {rssi} dBm,\n UUID: {uuid2},\n Major: {major}\n"
#                         scanned_info += f"A: {name}, RSSI: {rssi} dBm,\n Major: {major}\n"
#                     elif uuid == "d8ac484e4fbb4b36bf12c249ab83673b" and major == 111:
#                         name = "201"
#                         uuid2 = "d8ac484e4fbb4b36..."
#                         # scanned_info += f"A: {name}, RSSI: {rssi} dBm,\n UUID: {uuid2},\n Major: {major}\n"
#                         scanned_info += f"A: {name}, RSSI: {rssi} dBm,\n Major: {major}\n"
                        
#                     else:
#                         name = "3"
#                         # scanned_info += f"A: {name}, RSSI: {rssi} dBm,\n UUID: {uuid},\n Major: {major}\n"
#                         scanned_info += f"A: {name}, RSSI: {rssi} dBm,\n Major: {major}\n"
                
#                 # self.scanned_devices.append({"rssi": rssi, "uuid": uuid, "major": major, "minor": minor})

#             self.root.ids.label.text = scanned_info
#             # self.root.ids.status.text = "Scan Complete"
#             Logger.info('Bluetooth: ' + '\n' + scanned_info)
            
#         def send_data(self):
#             url = "http://192.168.100.183:5000/Input"
#             for device in self.scanned_devices:
#                 data = {
#                     # "anc_name": device['name'],
#                     "rssi": device.get('rssi'),  # ใช้ .get() เพื่อหลีกเลี่ยง KeyError
#                     "uuid": device['uuid'],
#                     "major": device['major'],
#                     "minor": device['minor']
#                 }
                    
#                 try:
#                     response = requests.post(url, json=data)
#                     response.raise_for_status()
#                     Logger.info(f'Successfully sent data to API: {response.json()}')
#                 except requests.exceptions.HTTPError as http_err:
#                     Logger.error(f'HTTP error occurred: {http_err}')
#                 except Exception as err:
#                     Logger.error(f'Other error occurred: {err}')
#             self.root.ids.status.text = "Data Sent"

#         def stop_service(self):
#             self.service.stop(self.activity)
#             Logger.info("Scan: Stop Scanning")
#             self.scanning = False
#             self.stop_scan()

#             # ยกเลิกการตั้งเวลาเพื่อหยุดการเรียก scan_for_devices ซ้ำ
#             # if hasattr(self, 'scan_loop_event'):
#             #     self.scan_loop_event.cancel()
#             self.root.ids.status.text = "Stop Scanning"
        
#         def stop_scan(self):
#             self.scanner_dispatcher.stop_scan()
#             self.is_scanning = False  # ตั้งสถานะกลับไปไม่สแกน
#             Logger.info("Scan stopped. Ready to start new scan.")
            
#         def is_bluetooth_enabled(self):
#             BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
#             adapter = BluetoothAdapter.getDefaultAdapter()
#             return adapter.isEnabled()

#         def request_bluetooth_enable(self):
#             Intent = autoclass('android.content.Intent')
#             Settings = autoclass('android.provider.Settings')
#             activity = autoclass('org.kivy.android.PythonActivity').mActivity
#             intent = Intent(Settings.ACTION_BLUETOOTH_SETTINGS)
#             activity.startActivity(intent)

# if __name__ == "__main__":
#     MyApp().run()