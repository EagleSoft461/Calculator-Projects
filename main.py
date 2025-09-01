import math
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button 
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle # Renk ve Dikdörtgen çizmek için gerekli

class CalculatorApp(App):

    def on_start(self):
        # Pencereye klavye olaylarını bağlama
        Window.bind(on_key_down=self.on_keyboard)
        Window.size = (600,700)
        os.environ['KIVY_NO_CONSOLELOG'] = '1'  # log penceresini kapatır
        os.environ['KIVY_LOG_LEVEL'] = '0'      # TRACE/INFO/WARNING hepsini kapatır

    def build(self):
        # Operatör listesini tanımlama
        self.operators = ['+', '-', '*', '/']
        # Son girilen operatörü tutacak değişken
        self.last_operator = None
        # Son girilen karakterin bir sayı olup olmadığını kontrol eden değişken
        self.last_was_operator = None

        # Hesaplama ekranı için metin girişi
        self.result = TextInput(
            font_size=32,
            readonly=True,
            halign="right",
            multiline=False,
            background_color=get_color_from_hex("#333333"),
            foreground_color=get_color_from_hex("#ffffff"),
            padding_y=[(40 - 24) / 2.0, 0] # Dikey hizalama için
        )
        
        # Ana düzen (dikey kutu düzeni)
        main_layout = BoxLayout(orientation="vertical", spacing=5, padding=10)
        
        # main_layout için arka plan rengi ekleme
        with main_layout.canvas.before:
            Color(rgb=get_color_from_hex("#222222"))
            self.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)

        # Düzenin boyutu veya konumu değiştiğinde arka planı güncelle
        main_layout.bind(size=self.update_rect, pos=self.update_rect)

        main_layout.add_widget(self.result)
        
        # Butonlar için ızgara düzeni
        buttons_layout = GridLayout(cols=5, spacing=5)
        
        # Buton metinleri listesi, bilimsel işlemler de dahil
        buttons = [
            "sin", "cos", "log", "tan", "sqrt",
            "7", "8", "9", "/", "^",
            "4", "5", "6", "*", "(",
            "1", "2", "3", "-", ")",
            "0", ".", "=", "+", "C"
        ]

        # Butonları oluşturma ve düzene ekleme
        for btn in buttons:
            button = Button(
                text=btn, 
                font_size=24,
                size_hint_y=None, 
                height=60,
                background_normal="",
                background_color=self.get_button_color(btn)
            )
            button.bind(on_press=self.on_button_press)
            buttons_layout.add_widget(button)
        
        main_layout.add_widget(buttons_layout)

        return main_layout

    def update_rect(self, instance, value):
        # Arka plan dikdörtgeninin boyutunu ve konumunu güncelleme
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def get_button_color(self, text):
        # Buton metnine göre renk döndürme
        if text in self.operators or text in ["^", "(", ")","C"]:
            return get_color_from_hex("#FFA500") # Turuncu
        elif text == "=":
            return get_color_from_hex("#008000") # Yeşil
        elif text in ["sqrt", "sin", "cos", "tan","log"]:
            return get_color_from_hex("#808080") # Gri
        else:
            return get_color_from_hex("#555555") # Koyu gri

    # Klavye etkileşim fonksiyonu
    def on_keyboard(self, window, keycode, scancode, codepoint, modifier):
        current_text = self.result.text
        
        # Basılan karakterin sayı olup olmadığını kontrol et
        if codepoint and codepoint.isdigit():
            self.result.text += codepoint
        
        # İşlem tuşlarını kontrol et
        elif codepoint in ['+', '-', '*', '/']:
            if current_text and current_text[-1] not in self.operators:
                self.result.text += codepoint

        # Enter tuşu için '=' işlevi
        elif keycode == 13: # Enter tuşu
            self.calculate()
            
        # Backspace tuşu için silme işlevi
        elif keycode == 8: # Backspace tuşu
            self.result.text = current_text[:-1]

        # Nokta tuşu için
        elif codepoint == '.':
            self.result.text += '.'

        # Bilimsel işlemler için özel kısayollar
        elif codepoint == 's': # 's' harfi sin için
            self.on_sin_press()
        elif codepoint == 'c': # 'c' harfi cos için
            self.on_cos_press()
        elif codepoint == 'r': # 'r' harfi sqrt için
            self.on_sqrt_press()
        elif codepoint == 'l': # 'l' harfi log için
            self.on_log_press()

    # Buton basma olaylarını yönetme
    def on_button_press(self, instance):
        btn_text = instance.text
        current_text = self.result.text
        
        if btn_text == "C":
            self.result.text = ""
        elif btn_text == "=":
            self.calculate()
        elif btn_text in ["+", "-", "*", "/", "."]:
            if current_text and current_text[-1] not in self.operators:
                self.result.text += btn_text
        elif btn_text == "^":
            # Üs alma için ** operatörü kullanılır
            self.result.text += "**"
        elif btn_text == "(":
            self.result.text += "("
        elif btn_text == ")":
            self.result.text += ")"
        elif btn_text == "sin":
            self.on_sin_press()
        elif btn_text == "cos":
            self.on_cos_press()
        elif btn_text == "tan":
            self.on_tan_press()
        elif btn_text == "log":
            self.on_log_press()
        elif btn_text == "sqrt":
            self.on_sqrt_press()
        else:
            self.result.text += btn_text

    def calculate(self):
        try:
            # Python'ın eval() fonksiyonu ile ifadeyi hesaplama
            self.result.text = str(eval(self.result.text))
        except (SyntaxError, ZeroDivisionError):
            self.result.text = "Hata"

    def on_sqrt_press(self):
        try:
            val = float(self.result.text)
            if val >= 0:
                self.result.text = str(math.sqrt(val))
            else:
                self.result.text = "Hata"
        except ValueError:
            self.result.text = "Hata"

    def on_sin_press(self):
        try:
            val = float(self.result.text)
            self.result.text = str(math.sin(math.radians(val))) # Dereceyi radyana çevirme
        except ValueError:
            self.result.text = "Hata"

    def on_cos_press(self):
        try:
            val = float(self.result.text)
            self.result.text = str(math.cos(math.radians(val))) # Dereceyi radyana çevirme
        except ValueError:
            self.result.text = "Hata"
        
    def on_tan_press(self):
        try:
            val = float(self.result.text)
            self.result.text = str(math.tan(math.radians(val))) # Dereceyi radyana çevirme
        except ValueError:
            self.result.text = "Hata"

    def on_log_press(self):
        try:
            val = float(self.result.text)
            if val > 0:
                self.result.text = str(math.log10(val))
            else:
                self.result.text = "Hata"
        except ValueError:
            self.result.text = "Hata"

if __name__ == "__main__":
    CalculatorApp().run()
