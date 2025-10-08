"""
تطبيق بسيط لتحويل العملات باستخدام KivyMD
ميزات:
- إدخال المبلغ
- اختيار العملة المصدر والهدف
- استخدام معدلات تحويل ثابتة (يمكن لاحقاً توصيل API لأسعار حقيقية)

تعليقات الكود باللغة العربية كما طلبت
"""
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

# ضبط حجم النافذة لسطح المكتب لتجربة أسهل (يمكن إزالته عند تشغيله على هاتف)
Window.size = (360, 640)


KV = '''
MDScreen:
    md_bg_color: app.theme_cls.bg_dark

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(12)

        MDLabel:
            text: 'Currency Converter'
            halign: 'center'
            font_style: 'H4'
            size_hint_y: None
            height: self.texture_size[1]

        MDTextField:
            id: amount
            hint_text: 'Enter amount'
            helper_text: 'Numbers only, e.g. 123.45'
            helper_text_mode: 'on_focus'
            icon_right: 'currency-usd'
            input_filter: 'float'

        MDBoxLayout:
            spacing: dp(8)

            MDRaisedButton:
                id: src_btn
                text: app.src_currency
                on_release: app.open_src_menu(self)

            MDRaisedButton:
                id: tgt_btn
                text: app.tgt_currency
                on_release: app.open_tgt_menu(self)

        MDRaisedButton:
            text: 'Convert'
            pos_hint: {'center_x': .5}
            on_release: app.convert_currency()

        MDSeparator:
            height: dp(1)

        MDLabel:
            id: result_label
            text: app.result_text
            halign: 'center'
            theme_text_color: 'Secondary'

        Widget:
'''


class CurrencyConverterApp(MDApp):
    # نص النتيجة الذي يظهر في الواجهة
    result_text = StringProperty('Result will appear here')
    # العملة الافتراضية للمصدر والهدف
    src_currency = StringProperty('USD')
    tgt_currency = StringProperty('EUR')

    # خريطة لمعدلات التحويل الثابتة (كل قيمة هي كم تساوي وحدة من العملة الأساسية USD)
    # لاحقاً يمكن استبدالها باستدعاء API للحصول على أسعار فعلية
    rates = {
        'USD': 1.0,
        'EUR': 0.92,
        'GBP': 0.78,
        'JPY': 149.5,
        'EGP': 30.9,
        'SAR': 3.75,
        'AED': 3.67
    }

    def build(self):
        # إعداد الثيم وألوان التطبيق
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Light'
        screen = Builder.load_string(KV)

        # إعداد قوائم اختيار العملة
        menu_items = [
            {
                'viewclass': 'OneLineListItem',
                'text': code,
                'on_release': lambda x=code: self.set_src_currency(x)
            } for code in sorted(self.rates.keys())
        ]

        self.src_menu = MDDropdownMenu(
            caller=None,
            items=menu_items,
            width_mult=4
        )

        # قائمة الهدف تستخدم نفس العناصر لكن مع callback مختلف
        menu_items_tgt = [
            {
                'viewclass': 'OneLineListItem',
                'text': code,
                'on_release': lambda x=code: self.set_tgt_currency(x)
            } for code in sorted(self.rates.keys())
        ]

        self.tgt_menu = MDDropdownMenu(
            caller=None,
            items=menu_items_tgt,
            width_mult=4
        )

        return screen

    # فتح قائمة المصدر وتعيين caller حتى تعرف أي زر فتحها
    def open_src_menu(self, caller):
        self.src_menu.caller = caller
        self.src_menu.open()

    # فتح قائمة الهدف
    def open_tgt_menu(self, caller):
        self.tgt_menu.caller = caller
        self.tgt_menu.open()

    def set_src_currency(self, code):
        # عند اختيار عملة المصدر نخفي القائمة ونحدث النص
        self.src_currency = code
        self.root.ids.src_btn.text = code
        self.src_menu.dismiss()

    def set_tgt_currency(self, code):
        # عند اختيار عملة الهدف
        self.tgt_currency = code
        self.root.ids.tgt_btn.text = code
        self.tgt_menu.dismiss()

    def convert_currency(self):
        # دالة التحويل - تقرأ المبلغ وتطبق المعادلة
        txt = self.root.ids.amount.text
        if not txt:
            Snackbar(text='Please enter an amount').open()
            return

        try:
            amt = float(txt)
        except ValueError:
            Snackbar(text='Invalid amount').open()
            return

        src_rate = self.rates.get(self.src_currency)
        tgt_rate = self.rates.get(self.tgt_currency)

        if src_rate is None or tgt_rate is None:
            Snackbar(text='Unsupported currency').open()
            return

        # تحويل: أولاً إلى USD (أساس الخريطة)، ثم إلى العملة الهدف
        amount_in_usd = amt / src_rate
        converted = amount_in_usd * tgt_rate

        self.result_text = f"{amt:.2f} {self.src_currency} = {converted:.2f} {self.tgt_currency}"
        # تحديث تسمية النتيجة في الواجهة
        self.root.ids.result_label.text = self.result_text


if __name__ == '__main__':
    CurrencyConverterApp().run()
