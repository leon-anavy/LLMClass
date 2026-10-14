# -*- coding: utf-8 -*-
"""
הדגמות חיות לשיעור "ניקוי טקסט וטוקניזציה".
כל שלב הוא פונקציה – מריצים אחת-אחת מול הכיתה:
    python demos/tokenizer_demos.py 3      (מריץ רק את שלב 3)
    python demos/tokenizer_demos.py        (מריץ הכל)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO_FILE = os.path.join(ROOT, "data", "processed", "clean_demo.txt")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def stage2_split_tokenizer():
    """שלב 2 – ה-tokenizer הבסיסי שכתבנו אתמול"""
    text = "הילד הלך הביתה. הוא אכל ארוחת ערב!"
    tokens = text.split()
    print(tokens)
    # ['הילד', 'הלך', 'הביתה.', 'הוא', 'אכל', 'ארוחת', 'ערב!']
    print("הביתה" in tokens)       # False  <- הבעיה!


def stage3_what_bothers_us():
    """שלב 3 – טקסט 'מלוכלך' לדיון בכיתה"""
    dirty = '   ד"ר כהן אמר: "החתול-ים ישנים"... החתולים ישנים!!!  The Cat sleeps.\n\n'
    print(dirty.split())


def stage4_eos():
    """שלב 4 – הטוקן המיוחד <EOS>"""
    text = "הילד הלך הביתה. הוא אכל."
    print(text.split())
    # ללא <EOS>: הזוג ('הביתה', 'הוא') נראה כמו צירוף אמיתי

    bad = text.replace(".", "<EOS>")
    print(bad.split())          # ['הילד', 'הלך', 'הביתה<EOS>', ...]  <- נדבק!

    good = text.replace(".", " <EOS> ")
    print(good.split())         # ['הילד', 'הלך', 'הביתה', '<EOS>', 'הוא', 'אכל', '<EOS>']

    tricky = "המחיר 3.5 שקלים... וואו!!!"
    print(tricky.replace(".", " <EOS> ").replace("!", " <EOS> ").split())
    # ['המחיר', '3', '<EOS>', '5', 'שקלים', '<EOS>', '<EOS>', '<EOS>', 'וואו', '<EOS>', '<EOS>', '<EOS>']


def stage5_cleaning():
    """שלב 5 – פעולות ניקוי"""
    text = '  שלום,   אמר הילד: "אני אוהב-מאוד פייתון".  '

    # א. מקפים
    text = text.replace("-", " ")
    # ב. סימני פיסוק – לולאה על רשימה
    for p in [",", ":", '"']:
        text = text.replace(p, "")
    # ג. סוף משפט
    text = text.replace(".", " <EOS> ")
    # ד. רווחים – split + join
    text = " ".join(text.split())
    print(text)       # שלום אמר הילד אני אוהב מאוד פייתון <EOS>

    # הסדר חשוב!
    en = "The Cat sat."
    wrong = en.replace(".", " <EOS> ").lower()
    right = en.lower().replace(".", " <EOS> ")
    print(wrong.split())    # [..., '<eos>']  <- הטוקן המיוחד נהרס
    print(right.split())    # [..., '<EOS>']


def stage6_repetitions():
    """שלב 6 – חזרות: tokens מול types (בלי ספירה – זה בשבוע הבא)"""
    tokens = "החתול ישן <EOS> החתול אכל <EOS> החתול ישן שוב <EOS>".split()
    print("tokens (מופעים):", len(tokens))         # 10
    print("types (שונים):", len(set(tokens)))      # 5

    # חזרות לא מוחקים. את הספירה עצמה נלמד בשבוע הבא.


def stage7_hebrew_english():
    """שלב 7 – עברית מול אנגלית"""
    print("Hello".lower(), "HELLO".lower(), "hello" == "Hello")   # hello hello False
    print("שלום".lower() == "שלום")                               # True – אין אותיות גדולות

    for word in ["cat", "חתול"]:
        b = word.encode("utf-8")
        print(word, "תווים:", len(word), "בתים:", len(b), b)
    # cat  תווים: 3 בתים: 3
    # חתול תווים: 4 בתים: 8   <- כל אות עברית = 2 בתים ב-UTF-8

    # מה קורה כשקוראים UTF-8 בקידוד הלא נכון (ברירת מחדל ישנה ב-Windows):
    print("שלום".encode("utf-8").decode("cp1255", errors="replace"))   # ג'יבריש


def stage8_save():
    """שלב 8 – שמירה לקובץ חדש"""
    tokens = ["הילד", "הלך", "הביתה", "<EOS>"]
    with open(DEMO_FILE, "w", encoding="utf-8") as f:
        f.write(" ".join(tokens))
    with open(DEMO_FILE, "r", encoding="utf-8") as f:
        back = f.read().split()
    print(back == tokens)    # True – אפשר לטעון שוב בדיוק את אותם טוקנים


stages = {
    "2": stage2_split_tokenizer, "3": stage3_what_bothers_us, "4": stage4_eos,
    "5": stage5_cleaning, "6": stage6_repetitions, "7": stage7_hebrew_english,
    "8": stage8_save,
}

if __name__ == "__main__":
    chosen = sys.argv[1:] or list(stages)
    for key in chosen:
        print("\n========== שלב", key, "==========")
        stages[key]()
