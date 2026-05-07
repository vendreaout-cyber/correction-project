import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window
from math import cos, sin, pi
from datetime import datetime
import os

# جعل النافذة شفافة
Window.clearcolor = (0, 0, 0, 0)  # شفاف تماماً
Window.fullscreen = True

class HorlogeAnalogique(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # تحميل الصورة
        chemins_possibles = [
            "/storage/emulated/0/ru.iiec.pydroid3/files/assets/clock_bg.png",
            "assets/clock_bg.png", 
            "clock_bg.png",
        ]
        
        self.bg_texture = None
        for chemin in chemins_possibles:
            if os.path.exists(chemin):
                try:
                    from kivy.core.image import Image as CoreImage
                    self.bg_texture = CoreImage(chemin).texture
                    print(f"✅ تم تحميل الصورة")
                    break
                except:
                    pass
        
        Clock.schedule_interval(self.mettre_a_jour, 0.2)

    def mettre_a_jour(self, *args):
        self.canvas.clear()
        self.dessiner_samae()
        self.dessiner_aiguilles()

    def dessiner_samae(self):
        centre_x = self.width / 2
        centre_y = self.height / 2
        rayon = min(centre_x, centre_y) * 0.85
        
        with self.canvas:
            if self.bg_texture:
                Rectangle(texture=self.bg_texture,
                         pos=(centre_x - rayon, centre_y - rayon),
                         size=(rayon * 2, rayon * 2))

    def dessiner_aiguilles(self):
        maintenant = datetime.now()
        seconde = maintenant.second + maintenant.microsecond / 1e6
        minute = maintenant.minute + seconde / 60.0
        heure = maintenant.hour % 12 + minute / 60.0

        centre_x = self.width / 2
        centre_y = self.height / 2
        rayon = min(centre_x, centre_y) * 0.85

        with self.canvas:
            # عقرب الساعات (أقصر - يصل إلى 0.45 بدلاً من 0.5)
            angle_h = -(heure * 30) * (pi / 180)
            Color(0, 0, 0, 0.9)
            Line(points=[centre_x, centre_y, 
                        centre_x + rayon * 0.42 * cos(angle_h), 
                        centre_y + rayon * 0.42 * sin(angle_h)], 
                 width=12, cap='round')

            # عقرب الدقائق (أقصر - يصل إلى 0.65 بدلاً من 0.7)
            angle_m = -(minute * 6) * (pi / 180)
            Color(0.1, 0.1, 0.6, 0.85)
            Line(points=[centre_x, centre_y, 
                        centre_x + rayon * 0.62 * cos(angle_m), 
                        centre_y + rayon * 0.62 * sin(angle_m)], 
                 width=8, cap='round')

            # عقرب الثواني (أقصر - يصل إلى 0.75 بدلاً من 0.8)
            angle_s = -(seconde * 6) * (pi / 180)
            Color(0.9, 0.2, 0.2, 0.9)
            Line(points=[centre_x, centre_y, 
                        centre_x + rayon * 0.72 * cos(angle_s), 
                        centre_y + rayon * 0.72 * sin(angle_s)], 
                 width=4, cap='round')
            
            # نقطة المركز
            Color(0, 0, 0, 0.9)
            Line(circle=(centre_x, centre_y, rayon * 0.06), width=4)

class ApplicationHorloge(App):
    def build(self):
        return HorlogeAnalogique()

if __name__ == '__main__':
    ApplicationHorloge().run()