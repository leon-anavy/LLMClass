# -*- coding: utf-8 -*-
"""
הדגמות חיות לשיעור "ניקוי טקסט וטוקניזציה".
כל שלב הוא פונקציה – מריצים אחת-אחת מול הכיתה:
    python demos/tokenizer_demos.py 3      (מריץ רק את שלב 3, מ-1 עד 8)
    python demos/tokenizer_demos.py        (מריץ הכל)
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO_FILE = os.path.join(ROOT, "data", "processed", "clean_demo.txt")
SAMPLE_FILE = os.path.join(ROOT, "data", "raw", "sample_dirty.txt")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def stage1_load():
    """שלב 1 – קריאת קובץ טקסט (תמיד עם encoding="utf-8")"""
    with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
        text = f.read()
    print(type(text), len(text), "תווים")    # <class 'str'>: כל הקובץ הוא מחרוזת אחת
    print(text[:40])
    print(repr(text[:40]))                    # repr מראה גם את הרווחים ואת ירידות השורה


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

    # באותו סדר כמו clean במשימה:
    # א. סוף משפט
    text = text.replace(".", " <EOS> ")
    # ב. מקפים
    text = text.replace("-", " ")
    # ג. סימני פיסוק – לולאה על רשימה
    for p in [",", ":", '"']:
        text = text.replace(p, "")
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
    """שלב 6 – חזרות: tokens מול types"""
    tokens = "החתול ישן <EOS> החתול אכל <EOS> החתול ישן שוב <EOS>".split()
    print("tokens (מופעים):", len(tokens))         # 10
    print("types (שונים):", len(set(tokens)))      # 5

    # חזרות לא מוחקים. בשבוע הבא נראה שמילוני ה-N-Gram צריכים בדיוק אותן.


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


STAGES = [stage1_load, stage2_split_tokenizer, stage3_what_bothers_us, stage4_eos,
          stage5_cleaning, stage6_repetitions, stage7_hebrew_english, stage8_save]

if __name__ == "__main__":
    chosen = STAGES
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if not arg.isdigit() or not 1 <= int(arg) <= len(STAGES):
            print("אין שלב כזה:", arg, " בחרו מספר בין 1 ל-" + str(len(STAGES)))
            sys.exit(1)
        chosen = [STAGES[int(arg) - 1]]
    for stage in chosen:
        print("\n==========", stage.__doc__.strip(), "==========")
        stage()
