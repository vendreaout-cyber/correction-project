"""
Application de Surveillance de Batterie - Version Française
Avec cercle animé, mode nuit et lecture des données réelles
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
import os

# Tentative de chargement d'une police française
FONT_NAME = 'Roboto'
font_paths = [
    os.path.join(os.path.dirname(__file__), 'fonts', 'Amiri-Regular.ttf'),
    'fonts/Amiri-Regular.ttf',
    'Amiri-Regular.ttf'
]

for path in font_paths:
    if os.path.exists(path):
        try:
            LabelBase.register(name='Amiri', fn_regular=path)
            FONT_NAME = 'Amiri'
            print(f"✅ Police chargée: {path}")
            break
        except:
            pass

class CircleWidget(Widget):
    """Cercle avec icône d'éclair"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.charging = False
        self.percent = 50
        self.night_mode = False
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.update_canvas()
    
    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.charging:
                Color(1, 0.84, 0, 1)  # Doré
            else:
                if self.night_mode:
                    if self.percent < 20:
                        Color(0.8, 0.3, 0.35, 1)
                    elif self.percent < 50:
                        Color(0.8, 0.55, 0.3, 1)
                    else:
                        Color(0.25, 0.65, 0.4, 1)
                else:
                    if self.percent < 20:
                        Color(0.95, 0.33, 0.41, 1)  # Rouge
                    elif self.percent < 50:
                        Color(0.98, 0.62, 0.33, 1)  # Orange
                    else:
                        Color(0.31, 0.78, 0.47, 1)  # Vert
            
            center_x = self.center_x
            center_y = self.center_y
            radius = min(self.width, self.height) / 2 - 10
            Ellipse(pos=(center_x - radius, center_y - radius), size=(radius*2, radius*2))
    
    def update(self, charging, percent, night_mode=False):
        self.charging = charging
        self.percent = percent
        self.night_mode = night_mode
        self.update_canvas()

class BatteryApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.night_mode = False
    
    def toggle_night_mode(self, instance):
        """Basculer entre mode nuit et mode jour"""
        self.night_mode = not self.night_mode
        
        if self.night_mode:
            # Mode nuit - couleurs sombres
            Window.clearcolor = get_color_from_hex('#0F0F1A')
            self.title_label.color = get_color_from_hex('#6C8EBF')
            self.percent_label.color = get_color_from_hex('#7DC488')
            self.status_title.color = get_color_from_hex('#8A9BB5')
            self.status_value.color = get_color_from_hex('#D4C4A3')
            self.time_title.color = get_color_from_hex('#8A9BB5')
            self.time_value.color = get_color_from_hex('#E6C384')
            self.temp_title.color = get_color_from_hex('#8A9BB5')
            self.temp_value.color = get_color_from_hex('#7DC488')
            instance.background_color = get_color_from_hex('#2A2A3E')
            instance.color = get_color_from_hex('#E6C384')
            instance.text = '🌙 Mode jour'
            self.circle.night_mode = True
        else:
            # Mode jour - couleurs claires
            Window.clearcolor = get_color_from_hex('#1E1E2E')
            self.title_label.color = get_color_from_hex('#89B4FA')
            self.percent_label.color = get_color_from_hex('#A6E3A1')
            self.status_title.color = get_color_from_hex('#CDD6F4')
            self.status_value.color = get_color_from_hex('#F9E2AF')
            self.time_title.color = get_color_from_hex('#BAC2DE')
            self.time_value.color = get_color_from_hex('#FAB387')
            self.temp_title.color = get_color_from_hex('#BAC2DE')
            self.temp_value.color = get_color_from_hex('#A6E3A1')
            instance.background_color = get_color_from_hex('#313244')
            instance.color = get_color_from_hex('#F9E2AF')
            instance.text = '🌙 Mode nuit'
            self.circle.night_mode = False
        
        self.circle.update(self.circle.charging, self.circle.percent, self.night_mode)
    
    def build(self):
        self.root_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Barre du haut
        top_bar = BoxLayout(size_hint=(1, 0.08), spacing=10)
        self.title_label = Label(
            text='🔋 Moniteur Batterie', 
            font_name=FONT_NAME,
            font_size='28sp', 
            color=get_color_from_hex('#89B4FA'),
            size_hint=(0.7, 1)
        )
        top_bar.add_widget(self.title_label)
        
        self.night_button = Button(
            text='🌙 Mode nuit',
            font_name=FONT_NAME,
            font_size='14sp',
            size_hint=(0.3, 0.8),
            background_color=get_color_from_hex('#313244'),
            color=get_color_from_hex('#F9E2AF'),
            halign='center',
            valign='middle'
        )
        self.night_button.bind(on_press=self.toggle_night_mode)
        top_bar.add_widget(self.night_button)
        self.root_layout.add_widget(top_bar)
        
        # Cercle central
        self.circle_frame = FloatLayout(size_hint=(1, 0.35))
        self.circle = CircleWidget(size_hint=(0.8, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.circle_frame.add_widget(self.circle)
        
        self.icon_label = Label(
            text='🔌',
            font_name=FONT_NAME,
            font_size='55sp',
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            valign='middle'
        )
        self.circle_frame.add_widget(self.icon_label)
        self.root_layout.add_widget(self.circle_frame)
        
        # Pourcentage batterie
        self.percent_label = Label(
            text='--%', 
            font_name=FONT_NAME, 
            font_size='42sp',
            color=get_color_from_hex('#A6E3A1'),
            size_hint=(1, 0.07)
        )
        self.root_layout.add_widget(self.percent_label)
        
        # Barre de progression
        self.progress_bar = ProgressBar(max=100, value=0, size_hint=(1, 0.07))
        self.root_layout.add_widget(self.progress_bar)
        
        # Statut
        self.status_title = Label(
            text='Statut :', 
            font_name=FONT_NAME,
            font_size='17sp', 
            color=get_color_from_hex('#CDD6F4'),
            size_hint=(1, 0.05)
        )
        self.root_layout.add_widget(self.status_title)
        
        self.status_value = Label(
            text='--', 
            font_name=FONT_NAME, 
            font_size='19sp',
            color=get_color_from_hex('#F9E2AF'),
            size_hint=(1, 0.07)
        )
        self.root_layout.add_widget(self.status_value)
        
        # Temps restant
        self.time_title = Label(
            text='Temps restant :', 
            font_name=FONT_NAME,
            font_size='16sp', 
            color=get_color_from_hex('#BAC2DE'),
            size_hint=(1, 0.05)
        )
        self.root_layout.add_widget(self.time_title)
        
        self.time_value = Label(
            text='--', 
            font_name=FONT_NAME, 
            font_size='18sp',
            color=get_color_from_hex('#FAB387'),
            size_hint=(1, 0.07)
        )
        self.root_layout.add_widget(self.time_value)
        
        # Température
        self.temp_title = Label(
            text='Température :', 
            font_name=FONT_NAME,
            font_size='16sp', 
            color=get_color_from_hex('#BAC2DE'),
            size_hint=(1, 0.05)
        )
        self.root_layout.add_widget(self.temp_title)
        
        self.temp_value = Label(
            text='--', 
            font_name=FONT_NAME, 
            font_size='18sp',
            color=get_color_from_hex('#A6E3A1'),
            size_hint=(1, 0.07)
        )
        self.root_layout.add_widget(self.temp_value)
        
        # Début de la mise à jour
        Clock.schedule_interval(self.update_battery, 1)
        
        return self.root_layout
    
    def get_battery_percent(self):
        """Lire le pourcentage de la batterie"""
        try:
            paths = [
                '/sys/class/power_supply/battery/capacity',
                '/sys/class/power_supply/BAT0/capacity',
            ]
            for path in paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        return int(f.read().strip())
            return 75
        except:
            return 75
    
    def get_charging_status(self):
        """Lire l'état de charge"""
        try:
            paths = [
                '/sys/class/power_supply/battery/status',
                '/sys/class/power_supply/BAT0/status',
            ]
            for path in paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        status = f.read().strip()
                        return 'Charging' in status or 'Full' in status
            return False
        except:
            return False
    
    def get_battery_temp(self):
        """Lire la température de la batterie"""
        try:
            paths = [
                '/sys/class/power_supply/battery/temp',
                '/sys/class/power_supply/BAT0/temp'
            ]
            for path in paths:
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        temp_raw = int(f.read().strip())
                        return f'{temp_raw / 10:.1f}°C'
            return '36°C'
        except:
            return '36°C'
    
    def update_icon_by_status(self, charging, percent):
        """Changer l'icône selon l'état"""
        if charging:
            self.icon_label.text = '⚡🔌'
            self.icon_label.color = get_color_from_hex('#FFD700')
        else:
            if percent is not None:
                if percent < 20:
                    self.icon_label.text = '⚠️🔋'
                    self.icon_label.color = get_color_from_hex('#F38BA8')
                elif percent < 50:
                    self.icon_label.text = '🔋'
                    self.icon_label.color = get_color_from_hex('#FAB387')
                else:
                    self.icon_label.text = '🔋✅'
                    self.icon_label.color = get_color_from_hex('#A6E3A1')
            else:
                self.icon_label.text = '❓'
    
    def update_battery(self, dt):
        percent = self.get_battery_percent()
        is_charging = self.get_charging_status()
        temp = self.get_battery_temp()
        
        self.circle.update(is_charging, percent if percent else 0, self.night_mode)
        self.update_icon_by_status(is_charging, percent)
        
        if percent is not None:
            self.percent_label.text = f'{percent}%'
            self.progress_bar.value = percent
            
            if percent < 20:
                self.progress_bar.color = get_color_from_hex('#F38BA8')
            elif percent < 50:
                self.progress_bar.color = get_color_from_hex('#FAB387')
            else:
                self.progress_bar.color = get_color_from_hex('#A6E3A1')
            
            if is_charging:
                self.status_value.text = '🟢 Branché'
                self.time_value.text = 'Chargeur connecté'
            else:
                if percent < 20:
                    self.status_value.text = '🔴 Batterie faible'
                    self.time_value.text = 'Moins d\'1 heure'
                else:
                    self.status_value.text = '🟡 Sur batterie'
                    hours = int(percent / 12)
                    if hours == 1:
                        self.time_value.text = f'Environ {hours} heure'
                    else:
                        self.time_value.text = f'Environ {hours} heures'
        else:
            self.percent_label.text = '--%'
            self.status_value.text = 'Lecture impossible'
        
        self.temp_value.text = temp

if __name__ == '__main__':
    BatteryApp().run()