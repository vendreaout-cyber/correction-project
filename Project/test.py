from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
import os

class CoffeeTycoonGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10
        
        self.money = 0
        self.income = 1
        self.prestige_level = 0
        
        # chemin de l'image
        img_path = os.path.join(os.path.dirname(__file__), 'fonts', 'Coffecup.png')
        
        # === titre ===
        self.add_widget(Label(text='COFFEE TYCOON', font_size='32sp', bold=True))
        
        # === affichage argent ===
        self.money_label = Label(text='0 CAFÉS', font_size='48sp', bold=True)
        self.add_widget(self.money_label)
        
        # === zone tasse + bouton transparent ===
        cup_layout = FloatLayout(size_hint=(1, 0.4))
        
        # image du café
        self.cup_img = Image(
            source=img_path,
            size_hint=(None, None),
            size=(200, 200),   # taille fixe pour éviter la déformation
            pos_hint={'center_x':0.35, 'center_y':0.5},
            allow_stretch=False,
            keep_ratio=True
        )
        cup_layout.add_widget(self.cup_img)
        
        # bouton transparent au-dessus de l'image
        self.cup_btn = Button(
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={'center_x':0.5, 'center_y':0.5},
            background_color=(0,0,0,0),
            border=(0,0,0,0)
        )
        self.cup_btn.bind(on_press=self.collect)
        cup_layout.add_widget(self.cup_btn)
        
        # texte en bas de l'image
        self.cup_text = Label(
            text='+1 CAFÉ',
            font_size='20sp',
            bold=True,
            color=(1,1,1,1),
            pos_hint={'center_x':0.5, 'y':0}
        )
        cup_layout.add_widget(self.cup_text)
        
        self.add_widget(cup_layout)
        
        # === revenu ===
        self.income_label = Label(text=f'Revenu: {self.income} café/sec', font_size='18sp', color=(0.9, 0.9, 0.2, 1))
        self.add_widget(self.income_label)
        
        # === barre de progression ===
        self.progress = ProgressBar(max=100, value=0, size_hint=(1, 0.05))
        self.add_widget(self.progress)
        
        # === bouton upgrade ===
        self.upgrade_btn = Button(text='Améliorer (50 CAFÉS)', font_size='18sp', 
                                  background_color=(0.2, 0.6, 0.2, 1), size_hint=(1, 0.15))
        self.upgrade_btn.bind(on_press=self.upgrade)
        self.add_widget(self.upgrade_btn)
        
        # === bouton prestige ===
        self.prestige_btn = Button(text='Prestige (1000 CAFÉS)', font_size='16sp',
                                    background_color=(0.6, 0.2, 0.6, 0.8), size_hint=(1, 0.12))
        self.prestige_btn.bind(on_press=self.prestige)
        self.add_widget(self.prestige_btn)
        
        # mise à jour chaque seconde
        Clock.schedule_interval(self.update_income, 1)
    
    def collect(self, instance):
        self.money += 1
        self.update_ui()
    
    def update_income(self, dt):
        self.money += self.income
        self.update_ui()
    
    def upgrade(self, instance):
        cost = 50 + (self.income - 1) * 10
        if self.money >= cost:
            self.money -= cost
            self.income += 1
            next_cost = 50 + (self.income - 1) * 10
            instance.text = f'Améliorer (+1/sec)\nCoût: {next_cost} CAFÉS'
            self.progress.value = min(100, (self.income / 10) * 100)
            self.update_ui()
    
    def prestige(self, instance):
        if self.money >= 1000:
            self.prestige_level += 1
            self.money = 0
            self.income = 1
            self.progress.value = 0
            self.upgrade_btn.text = 'Améliorer (50 CAFÉS)'
            instance.text = f'Prestige x{self.prestige_level}\nSuivant: 1000 CAFÉS'
            self.update_ui()
    
    def update_ui(self):
        self.money_label.text = f'{int(self.money)} CAFÉS'
        self.income_label.text = f'Revenu: {self.income} café/sec'

class CoffeeApp(App):
    def build(self):
        return CoffeeTycoonGame()

if __name__ == '__main__':
    CoffeeApp().run()