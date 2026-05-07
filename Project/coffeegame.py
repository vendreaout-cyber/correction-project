# main.py - الكود الأصلي ولكن معدل ليعمل بدون مشاكل
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock

class CoffeeTycoonGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        self.money = 0.0
        self.income_per_second = 1.0
        
        # عنوان اللعبة
        title = Label(text="☕ Coffee Tycoon ☕", 
                      font_size='24sp',
                      size_hint=(1, 0.1))
        self.add_widget(title)
        
        # عرض النقود
        self.money_label = Label(text="☕ 0", 
                                 font_size='36sp',
                                 bold=True)
        self.add_widget(self.money_label)
        
        # زر جمع الأرباح اليدوي
        self.collect_btn = Button(text="☕ Pour Coffee +1 ☕", 
                                  size_hint=(1, 0.25),
                                  font_size='18sp',
                                  background_color=(0.6, 0.4, 0.2, 1))
        self.collect_btn.bind(on_press=self.collect_money)
        self.add_widget(self.collect_btn)
        
        # عرض الدخل في الثانية
        self.income_label = Label(text=f"Income: {self.income_per_second} ☕/sec",
                                  font_size='16sp',
                                  color=(0.8, 0.8, 0.2, 1))
        self.add_widget(self.income_label)
        
        # شريط التطور
        self.progress = ProgressBar(max=100, value=0, size_hint=(1, 0.05))
        self.add_widget(self.progress)
        
        # زر شراء تحسين
        self.upgrade_btn = Button(text="🆙 Buy Espresso Machine (50 ☕)",
                                  font_size='16sp',
                                  background_color=(0.2, 0.5, 0.2, 1),
                                  size_hint=(1, 0.15))
        self.upgrade_btn.bind(on_press=self.buy_upgrade)
        self.add_widget(self.upgrade_btn)
        
        # زر تطور متقدم
        self.prestige_btn = Button(text="🌟 Prestige (1000 ☕) 🌟",
                                   font_size='14sp',
                                   background_color=(0.5, 0.2, 0.5, 0.8),
                                   size_hint=(1, 0.1))
        self.prestige_btn.bind(on_press=self.prestige)
        self.add_widget(self.prestige_btn)
        
        self.prestige_count = 0
        
        # تحديث الدخل كل ثانية
        Clock.schedule_interval(self.update_income, 1)
    
    def collect_money(self, instance):
        self.money += 1
        self.update_ui()
    
    def update_income(self, dt):
        self.money += self.income_per_second
        self.update_ui()
    
    def buy_upgrade(self, instance):
        cost = 50 + (self.income_per_second - 1) * 10
        if self.money >= cost:
            self.money -= cost
            self.income_per_second += 1
            self.progress.value = min(100, (self.income_per_second / 10) * 100)
            instance.text = f"🆙 Next Upgrade ({int(self.income_per_second)} ☕/sec)\nCost: {int(cost + 10)} ☕"
        self.update_ui()
    
    def prestige(self, instance):
        if self.money >= 1000:
            self.prestige_count += 1
            self.money = 0
            self.income_per_second = 1.0
            self.progress.value = 0
            self.upgrade_btn.text = "🆙 Buy Espresso Machine (50 ☕)"
            instance.text = f"🌟 Prestige x{self.prestige_count} (Next: 1000 ☕) 🌟"
            self.update_ui()
    
    def update_ui(self):
        self.money_label.text = f"☕ {int(self.money)}"
        self.income_label.text = f"Income: {self.income_per_second} ☕/sec"

class TycoonApp(App):
    def build(self):
        return CoffeeTycoonGame()

if __name__ == '__main__':
    TycoonApp().run()