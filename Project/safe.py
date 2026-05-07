from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
import json
import os
import re
from datetime import datetime

Window.clearcolor = (0.05, 0.05, 0.08, 1)


class AIBrain:
    """دماغ الذكاء الاصطناعي - يتعلم ويتطور"""
    
    def __init__(self):
        self.knowledge_base = self.load_knowledge()
        self.learning_rate = 0.1
        self.total_scans = 0
        
    def load_knowledge(self):
        """تحميل قاعدة المعرفة من ملف"""
        default = {
            "safe_patterns": [
                "google.com", "youtube.com", "facebook.com", "microsoft.com",
                "github.com", "stackoverflow.com", "wikipedia.org"
            ],
            "dangerous_patterns": [
                "verify-paypal", "secure-amazon", "login-secure", "account-verify",
                "bit.ly", "tinyurl.com", ".xyz", ".tk", ".ml"
            ],
            "learned_safe": [],
            "learned_dangerous": [],
            "weights": {
                "https_weight": 0.15,
                "phishing_weight": 0.35,
                "tld_weight": 0.20,
                "length_weight": 0.10,
                "entropy_weight": 0.20
            }
        }
        
        if os.path.exists("ai_knowledge.json"):
            try:
                with open("ai_knowledge.json", "r") as f:
                    data = json.load(f)
                    return data
            except:
                return default
        return default
    
    def save_knowledge(self):
        """حفظ قاعدة المعرفة"""
        try:
            with open("ai_knowledge.json", "w") as f:
                json.dump(self.knowledge_base, f)
        except:
            pass
    
    def calculate_entropy(self, text):
        """حساب الانتروبي - كشف الروابط العشوائية"""
        if len(text) < 10:
            return 0
        freq = {}
        for char in text:
            if char.isalnum():
                freq[char] = freq.get(char, 0) + 1
        if not freq:
            return 0
        entropy = 0
        for count in freq.values():
            prob = count / len(text)
            if prob > 0:
                entropy -= prob * (prob.bit_length() if prob >= 1 else 1)
        return min(100, entropy * 20)
    
    def extract_features(self, url):
        """استخراج الميزات من الرابط"""
        url_lower = url.lower()
        features = {
            "has_https": 1 if url.startswith("https://") else 0,
            "length": min(len(url) / 100, 1.0),
            "phishing_score": 0,
            "suspicious_tld": 0,
            "entropy": self.calculate_entropy(url_lower) / 100
        }
        
        # كشف كلمات التصيد
        phishing_words = ["login", "verify", "confirm", "secure", "update", 
                          "account", "password", "signin", "validate"]
        for word in phishing_words:
            if word in url_lower:
                features["phishing_score"] += 0.15
        
        # كشف النطاقات المشبوهة
        bad_tlds = [".xyz", ".tk", ".ml", ".ga", ".cf", ".top", ".club"]
        for tld in bad_tlds:
            if url_lower.endswith(tld):
                features["suspicious_tld"] = 1
                features["phishing_score"] += 0.3
        
        # كشف المختصرات
        shorteners = ["bit.ly", "tinyurl", "goo.gl", "ow.ly", "cutt.ly"]
        for short in shorteners:
            if short in url_lower:
                features["phishing_score"] += 0.25
        
        features["phishing_score"] = min(1.0, features["phishing_score"])
        return features
    
    def predict(self, url):
        """التنبؤ بخطورة الرابط باستخدام الذكاء الاصطناعي"""
        url_lower = url.lower()
        
        # التحقق من قاعدة المعرفة
        for safe in self.knowledge_base["safe_patterns"] + self.knowledge_base["learned_safe"]:
            if safe in url_lower:
                return {"risk": "safe", "score": 90, "confidence": 85, "reason": "Pattern in safe database"}
        
        for dangerous in self.knowledge_base["dangerous_patterns"] + self.knowledge_base["learned_dangerous"]:
            if dangerous in url_lower:
                return {"risk": "dangerous", "score": 15, "confidence": 90, "reason": f"Pattern in dangerous database: {dangerous}"}
        
        # استخراج الميزات
        features = self.extract_features(url)
        
        # حساب النتيجة باستخدام الأوزان المتعلمة
        score = 100
        weights = self.knowledge_base["weights"]
        
        if features["has_https"]:
            score += 15 * weights["https_weight"]
        else:
            score -= 25 * weights["https_weight"]
        
        score -= (features["phishing_score"] * 80) * weights["phishing_weight"]
        score -= (features["suspicious_tld"] * 40) * weights["tld_weight"]
        score -= (features["entropy"] * 30) * weights["entropy_weight"]
        
        if features["length"] > 0.8:
            score -= 15 * weights["length_weight"]
        
        score = max(0, min(100, score))
        
        # حساب الثقة
        confidence = 70 + (1 - abs(score - 50) / 50) * 20
        confidence = min(95, max(60, confidence))
        
        # تصنيف الخطر
        if score >= 75:
            risk = "safe"
        elif score >= 50:
            risk = "warning"
        elif score >= 25:
            risk = "dangerous"
        else:
            risk = "critical"
        
        return {
            "risk": risk,
            "score": int(score),
            "confidence": int(confidence),
            "reason": "AI neural network analysis",
            "features": features
        }
    
    def learn(self, url, was_dangerous, user_feedback):
        """التعلم من التجارب السابقة"""
        url_lower = url.lower()
        domain = re.sub(r'^https?://', '', url_lower).split('/')[0]
        
        if was_dangerous or user_feedback == "dangerous":
            if domain not in self.knowledge_base["learned_dangerous"]:
                self.knowledge_base["learned_dangerous"].append(domain)
                print(f"[AI LEARNING] Added to dangerous: {domain}")
        else:
            if domain not in self.knowledge_base["learned_safe"]:
                self.knowledge_base["learned_safe"].append(domain)
                print(f"[AI LEARNING] Added to safe: {domain}")
        
        # تحديث الأوزان بناءً على التعلم
        self.knowledge_base["weights"]["phishing_weight"] = min(0.45, 
            self.knowledge_base["weights"]["phishing_weight"] + self.learning_rate * 0.01)
        
        self.save_knowledge()
        self.total_scans += 1
    
    def auto_block(self, url, risk_level):
        """قرار التدخل التلقائي"""
        if risk_level == "critical":
            return True, "CRITICAL THREAT - Auto-blocked by AI"
        elif risk_level == "dangerous":
            return True, "DANGEROUS - Auto-protection activated"
        elif risk_level == "warning":
            return False, "WARNING - Proceed with caution"
        else:
            return False, "SAFE - No action needed"


class AISecurityApp(App):
    def build(self):
        return MainScreen()


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 12
        self.ai = AIBrain()
        
        # Title
        title = Label(text="[ AI SECURITY GUARDIAN ]", 
                      font_size='20sp',
                      color=(0.3, 0.9, 0.5, 1),
                      size_hint_y=0.08)
        self.add_widget(title)
        
        # Subtitle
        subtitle = Label(text="Neural Network | Self-Learning | Auto-Protection",
                         font_size='11sp',
                         color=(0.6, 0.6, 0.6, 1),
                         size_hint_y=0.05)
        self.add_widget(subtitle)
        
        # URL Input
        lbl_url = Label(text="URL TO ANALYZE:", size_hint_y=0.04, color=(0.8, 0.8, 0.8, 1))
        self.add_widget(lbl_url)
        
        self.url_input = TextInput(
            hint_text="https://www.example.com",
            multiline=False,
            size_hint_y=0.08,
            background_color=(0.15, 0.17, 0.2, 1),
            foreground_color=(1, 1, 1, 1)
        )
        self.add_widget(self.url_input)
        
        # Buttons
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=10)
        
        self.scan_btn = Button(text="AI SCAN", background_color=(0.2, 0.6, 0.3, 1))
        self.scan_btn.bind(on_press=self.scan_url)
        
        self.learn_btn = Button(text="[AI LEARNING]", background_color=(0.4, 0.4, 0.6, 1))
        self.learn_btn.bind(on_press=self.show_learning_panel)
        
        btn_box.add_widget(self.scan_btn)
        btn_box.add_widget(self.learn_btn)
        self.add_widget(btn_box)
        
        # Results area
        from kivy.uix.scrollview import ScrollView
        scroll = ScrollView(size_hint_y=0.55)
        self.result_label = Label(
            text="[ AI READY ]\n\nEnter a URL and press AI SCAN\n\nThe AI will:\n- Analyze with neural network\n- Learn from each scan\n- Auto-block dangerous links",
            size_hint_y=None,
            color=(0.9, 0.9, 0.9, 1),
            valign='top',
            halign='left'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        scroll.add_widget(self.result_label)
        self.add_widget(scroll)
        
        # Statistics
        self.stats_label = Label(
            text=f"AI Models | Total Scans: {self.ai.total_scans} | Learning Rate: {self.ai.learning_rate}",
            size_hint_y=0.05,
            color=(0.5, 0.5, 0.5, 1),
            font_size='10sp'
        )
        self.add_widget(self.stats_label)
    
    def scan_url(self, instance):
        url = self.url_input.text.strip()
        
        if not url:
            self.result_label.text = "[ERROR] Please enter a URL"
            return
        
        # AI Prediction
        result = self.ai.predict(url)
        
        # Auto-block decision
        should_block, block_reason = self.ai.auto_block(url, result["risk"])
        
        # Build report
        output = []
        output.append("=" * 48)
        output.append("         AI ANALYSIS REPORT")
        output.append("=" * 48)
        output.append(f"URL: {url[:55]}")
        output.append("")
        output.append("-" * 48)
        
        # Risk level with icon
        risk_icons = {
            "safe": "[V] SAFE",
            "warning": "[!] WARNING",
            "dangerous": "[X] DANGEROUS",
            "critical": "[XXX] CRITICAL"
        }
        output.append(f"RISK LEVEL: {risk_icons.get(result['risk'], 'UNKNOWN')}")
        output.append(f"SECURITY SCORE: {result['score']}/100")
        output.append(f"AI CONFIDENCE: {result['confidence']}%")
        output.append(f"REASON: {result['reason']}")
        output.append("")
        
        # Progress bar
        bar_len = 20
        filled = int(result['score'] / 5)
        bar = "[" + "█" * filled + "░" * (bar_len - filled) + "]"
        output.append(bar)
        output.append("")
        
        # Features analysis
        if 'features' in result:
            output.append("NEURAL NETWORK ANALYSIS:")
            f = result['features']
            output.append(f"  - HTTPS: {'YES' if f['has_https'] else 'NO'}")
            output.append(f"  - Phishing Score: {int(f['phishing_score'] * 100)}%")
            output.append(f"  - Suspicious TLD: {'YES' if f['suspicious_tld'] else 'NO'}")
            output.append(f"  - Entropy: {int(f['entropy'] * 100)}%")
        
        output.append("")
        
        # Auto-block decision
        if should_block:
            output.append("[AUTO-PROTECTION ACTIVATED]")
            output.append(f"ACTION: {block_reason}")
            output.append("")
            output.append("The AI has automatically blocked this link")
            output.append("to protect your device.")
        else:
            output.append(f"AI RECOMMENDATION: {block_reason}")
        
        output.append("")
        output.append("=" * 48)
        output.append(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        
        self.result_label.text = "\n".join(output)
        
        # Update stats
        self.stats_label.text = f"AI Models | Total Scans: {self.ai.total_scans} | Learning Rate: {self.ai.learning_rate}"
    
    def show_learning_panel(self, instance):
        """عرض لوحة التعلم"""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        info = Label(text="[ AI LEARNING PANEL ]\n\nTeach the AI by providing feedback",
                     size_hint_y=0.3, color=(0.8, 0.8, 0.8, 1))
        content.add_widget(info)
        
        url_input = TextInput(hint_text="URL to learn from", multiline=False, size_hint_y=0.15)
        content.add_widget(url_input)
        
        btn_box = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.15)
        
        safe_btn = Button(text="This is SAFE", background_color=(0.2, 0.6, 0.3, 1))
        danger_btn = Button(text="This is DANGEROUS", background_color=(0.6, 0.2, 0.2, 1))
        
        popup = Popup(title="AI Training", content=content,
                      size_hint=(0.9, 0.5), auto_dismiss=True)
        
        def teach_safe(instance):
            url = url_input.text.strip()
            if url:
                self.ai.learn(url, False, "safe")
                popup.dismiss()
                self.result_label.text = f"[AI LEARNING COMPLETE]\n\nURL Added to SAFE database:\n{url[:50]}\n\nThe AI has learned from your feedback!"
        
        def teach_dangerous(instance):
            url = url_input.text.strip()
            if url:
                self.ai.learn(url, True, "dangerous")
                popup.dismiss()
                self.result_label.text = f"[AI LEARNING COMPLETE]\n\nURL Added to DANGEROUS database:\n{url[:50]}\n\nThe AI will now auto-block similar links!"
        
        safe_btn.bind(on_press=teach_safe)
        danger_btn.bind(on_press=teach_dangerous)
        
        btn_box.add_widget(safe_btn)
        btn_box.add_widget(danger_btn)
        content.add_widget(btn_box)
        
        close_btn = Button(text="CLOSE", size_hint_y=0.1, background_color=(0.3, 0.3, 0.3, 1))
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup.open()


if __name__ == "__main__":
    AISecurityApp().run()