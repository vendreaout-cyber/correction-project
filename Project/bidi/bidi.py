# Project/bidi/bidi.py

def get_base_level_inner(text):
    # يرجع المستوى الأساسي للنص (LTR=0, RTL=1)
    # هنا مجرد تبسيط، النص العربي يرجع 1
    if any('\u0600' <= ch <= '\u06FF' for ch in text):
        return 1
    return 0

def get_display_inner(text):
    # يعيد النص كما هو (ممكن تضيف reshaping لاحقًا)
    return text