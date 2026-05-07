from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.clock import Clock
import json, os, random
from datetime import datetime

try:
    from plyer import battery
    HAS_PLYER = True
except ImportError:
    HAS_PLYER = False

Window.clearcolor = (0.05, 0.05, 0.08, 1)


class AIBatteryOptimizer:
    def __init__(self):
        self.user_profile = self.load_profile()
        self.history = []
        self.power_modes = {
            "performance": {"name": "Performance", "factor": 1.0},
            "balanced": {"name": "Balanced", "factor": 0.7},
            "eco": {"name": "Eco", "factor": 0.4}
        }

    def load_profile(self):
        if os.path.exists("ai_profile.json"):
            try:
                with open("ai_profile.json", "r") as f:
                    return json.load(f)
            except:
                return {"mode": "balanced"}
        return {"mode": "balanced"}

    def save_profile(self):
        try:
            with open("ai_profile.json", "w") as f:
                json.dump(self.user_profile, f)
        except:
            pass

    def record(self, level, is_charging):
        self.history.append({
            "level": level,
            "charging": is_charging,
            "time": datetime.now().strftime("%H:%M:%S")
        })
        if len(self.history) > 100:
            self.history = self.history[-100:]

    def ai_predict_mode(self):
        if not self.history:
            return self.user_profile['mode']

        avg_level = sum(h["level"] for h in self.history) / len(self.history)
        charging_ratio = sum(1 for h in self.history if h["charging"]) / len(self.history)

        if avg_level < 30 and charging_ratio < 0.3:
            return "eco"
        elif avg_level < 60:
            return "balanced"
        else:
            return "performance"

    def ai_solutions(self, level, is_charging):
        solutions = []
        mode = self.ai_predict_mode()

        if not is_charging:
            if level < 20:
                solutions.append("Enable Eco mode automatically")
                solutions.append("Close high consumption apps")
            elif level < 50:
                solutions.append("Reduce background updates")
                solutions.append("Adjust screen brightness dynamically")
            else:
                solutions.append("Battery stable")

        if mode == "performance":
            solutions.append("Priority: Performance")
        elif mode == "balanced":
            solutions.append("Balanced mode recommended")
        elif mode == "eco":
            solutions.append("Maximum energy saving")

        return solutions, mode


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        self.ai = AIBatteryOptimizer()
        self.fake_level = 80
        self.fake_charging = False

        self.title = Label(text="🔋 AI BATTERY GUARDIAN",
                           font_size='24sp',
                           color=(0.3, 0.9, 0.5, 1))
        self.add_widget(self.title)

        self.battery_label = Label(text="--%",
                                   font_size='40sp',
                                   color=(0.3, 0.9, 0.5, 1))
        self.add_widget(self.battery_label)

        self.progress = ProgressBar(max=100, value=50)
        self.add_widget(self.progress)

        self.ai_text = Label(text="Analysis in progress...",
                             color=(0.9, 0.9, 0.9, 1))
        self.add_widget(self.ai_text)

        btn_refresh = Button(text="🔄 REFRESH",
                             size_hint_y=0.1,
                             background_color=(0.2, 0.6, 0.4, 1))
        btn_refresh.bind(on_press=self.refresh)
        self.add_widget(btn_refresh)

        btn_tips = Button(text="💡 AI SOLUTIONS",
                          size_hint_y=0.1,
                          background_color=(0.3, 0.4, 0.5, 1))
        btn_tips.bind(on_press=self.show_solutions)
        self.add_widget(btn_tips)

        Clock.schedule_interval(self.auto_update, 5)
        self.update_display()

    def get_battery_info(self):
        if HAS_PLYER:
            info = battery.status
            if info:
                return info.get('percentage', 50), info.get('isCharging', False)
        if not self.fake_charging and self.fake_level > 0:
            self.fake_level -= random.randint(0, 2)
        return self.fake_level, self.fake_charging

    def update_display(self):
        level, is_charging = self.get_battery_info()
        self.ai.record(level, is_charging)

        self.battery_label.text = f"{level}%"
        self.progress.value = level

        if level < 20:
            self.battery_label.color = (0.9, 0.2, 0.2, 1)
        elif level < 40:
            self.battery_label.color = (0.9, 0.6, 0.2, 1)
        else:
            self.battery_label.color = (0.3, 0.9, 0.5, 1)

        _, mode = self.ai.ai_solutions(level, is_charging)
        self.ai_text.text = f"AI recommended mode: {self.ai.power_modes[mode]['name']}"

    def auto_update(self, dt):
        self.update_display()

    def refresh(self, instance):
        self.update_display()

    def show_solutions(self, instance):
        level, is_charging = self.get_battery_info()
        solutions, mode = self.ai.ai_solutions(level, is_charging)
        self.ai_text.text = f"AI recommended mode: {self.ai.power_modes[mode]['name']}\n" + "\n".join(solutions)


class BatteryGuardianApp(App):
    def build(self):
        return MainScreen()


if __name__ == "__main__":
    BatteryGuardianApp().run()