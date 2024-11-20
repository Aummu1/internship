from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Mesh, Translate, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import math

class MovingWaveShadowWidget(Widget):
    def __init__(self, **kwargs):
        super(MovingWaveShadowWidget, self).__init__(**kwargs)
        self.x_pos = 500  # ตำแหน่งเริ่มต้นของก้อน
        self.y_pos = 500
        self.speed_x = 0.5  # ลดความเร็วในทิศทาง X
        self.speed_y = 0.25  # ลดความเร็วในทิศทาง Y
        self.time = 0  # ใช้สำหรับการทำให้เกิดคลื่น

        with self.canvas:
            # พื้นหลังสีเทา
            Color(0.5, 0.5, 0.5, 1)  # สีเทา
            self.background = Rectangle(size=Window.size)

            # กำหนดตำแหน่งของการเลื่อน
            self.translation = Translate(self.x_pos, self.y_pos)
            
            # ฟังก์ชันสร้าง Mesh สำหรับวงกลม
            def create_circle_mesh(radius, num_points=30):
                vertices = []
                angle_step = 2 * math.pi / num_points
                for i in range(num_points):
                    angle = i * angle_step
                    x = radius * math.cos(angle)
                    y = radius * math.sin(angle)
                    vertices.extend([x, y])
                return vertices

            # เพิ่มเงาจาง ๆ ด้านนอกสุด
            # Color(0, 0, 0, 0.2)
            # vertices_blur = create_circle_mesh(70)
            # self.outer_shadow_blur = Mesh(
            #     vertices=vertices_blur,
            #     indices=[i for i in range(len(vertices_blur) // 2)],
            #     mode='triangle_fan'
            # )

            # ชั้นที่ 1: สีด้านนอกสุด
            # Color(1, 0, 0, 0.5)
            Color(142 / 255, 174 / 255, 219 / 255) #น้ำเงิน
            vertices_outer = create_circle_mesh(60)
            self.outer_shadow = Mesh(
                vertices=vertices_outer,
                indices=[i for i in range(len(vertices_outer) // 2)],
                mode='triangle_fan'
            )

            # ชั้นที่ 2: สีชั้นกลาง
            # Color(0, 1, 0, 0.5)
            Color(114 / 255, 151 / 255, 207 / 255) #น้ำเงิน
            vertices_middle = create_circle_mesh(45)
            self.middle_shadow = Mesh(
                vertices=vertices_middle,
                indices=[i for i in range(len(vertices_middle) // 2)],
                mode='triangle_fan'
            )

            # ชั้นที่ 3: สีชั้นในสุด
            # Color(0, 0, 1, 0.7)
            Color(84 / 255, 125 / 255, 189 / 255) #น้ำเงิน
            vertices_inner = create_circle_mesh(30)
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
        # อัปเดตขนาดของพื้นหลังเมื่อขนาดหน้าต่างเปลี่ยน
        self.background.size = Window.size

class MovingWaveShadowApp(App):
    def build(self):
        widget = MovingWaveShadowWidget()
        Clock.schedule_interval(widget.update, 1 / 60)  # อัปเดตทุก 1/60 วินาที
        return widget

if __name__ == '__main__':
    MovingWaveShadowApp().run()
