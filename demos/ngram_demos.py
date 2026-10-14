# -*- coding: utf-8 -*-
"""
הדגמות חיות לשיעור "מבוא ל-N-Gram".
כל שלב הוא פונקציה – מריצים אחת-אחת מול הכיתה:
    python demos/ngram_demos.py 3      (מריץ רק את שלב 3)
    python demos/ngram_demos.py        (מריץ הכל)
הקובץ לא משתמש בקוד שלכם, כך שהוא עובד גם לפני שהשלמתם את המשימה.
"""
import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# "החתול ישן. החתול אכל. החתול ישן שוב." אחרי ה-Tokenizer
CAT = ["החתול", "ישן", "<EOS>", "החתול", "אכל", "<EOS>", "החתול", "ישן", "שוב", "<EOS>"]


def stage1_windows():
    """שלב 1 – חלון שזז: כל ה-2-Gram וה-3-Gram במשפט"""
    tokens = ["הילד", "הלך", "<EOS>", "הוא", "אכל"]     # "הילד הלך. הוא אכל"
    print("2-Gram:")
    for i in range(len(tokens) - 1):
        print("  ", tokens[i:i + 2])
    print("3-Gram:")
    for i in range(len(tokens) - 2):
        print("  ", tokens[i:i + 3])
    # 5 טוקנים: 4 זוגות, 3 שלשות.  בכלל: len - n + 1
    # ['הלך', '<EOS>']  -> המשפט נגמר אחרי "הלך"
    # ['<EOS>', 'הוא']  -> "הוא" פותח משפט


def stage2_dict_basics():
    """שלב 2 – מילון: מפתח וערך"""
    ages = {}                      # מילון ריק
    ages["דנה"] = 16               # שומרים ערך תחת המפתח "דנה"
    ages["יואב"] = 17
    print(ages)                    # {'דנה': 16, 'יואב': 17}
    print(ages["דנה"])             # קוראים את הערך  ->  16
    ages["דנה"] = 17               # מפתח קיים: הערך מתחלף, לא מתווסף
    print(ages)
    print(len(ages))               # כמה מפתחות  ->  2
    print("נועה" in ages)          # האם המפתח קיים?  ->  False
    for name in ages:              # לולאה על כל המפתחות
        print(name, "->", ages[name])


def stage3_missing_key():
    """שלב 3 – מפתח שלא קיים"""
    ages = {"דנה": 16}
    print(ages.get("נועה"))        # None  (בלי קריסה)
    print(ages.get("נועה", 0))     # 0     (ערך ברירת מחדל)
    print(ages["נועה"])            # KeyError: 'נועה'  <- קריסה!


def stage4_list_values():
    """שלב 4 – ערך שהוא רשימה: הדפוס של 'צור אם חסר, ואז הוסף'"""
    after = {}
    for word, nxt in [("החתול", "ישן"), ("החתול", "אכל"), ("החתול", "ישן")]:
        if word not in after:
            after[word] = []       # פעם ראשונה: רשימה ריקה
        after[word].append(nxt)    # תמיד: מוסיפים לסוף
        print(after)
    # {'החתול': ['ישן', 'אכל', 'ישן']}   <- "ישן" פעמיים. לא מוחקים חזרות!


def stage5_build_bigrams():
    """שלב 5 – בונים מילון 2-Gram, צעד אחר צעד"""
    bigrams = {}
    for i in range(len(CAT) - 1):
        key = CAT[i]
        next_word = CAT[i + 1]
        if key not in bigrams:
            bigrams[key] = []
        bigrams[key].append(next_word)
        print(i, key, "->", next_word, "   ", bigrams)
    print()
    for key in bigrams:
        print(key, "->", bigrams[key])


def stage6_why_repeats():
    """שלב 6 – למה שומרים חזרות: בחירה אקראית מהרשימה"""
    options = ["ישן", "אכל", "ישן"]        # מה שבא אחרי "החתול"
    for _ in range(10):
        print(random.choice(options), end="  ")
    print()
    # "ישן" יוצא בערך פי 2 מ"אכל", בלי שספרנו כלום.
    # מה שבא אחרי <EOS> = המילים שפותחות משפט:
    print("פותחות משפט:", ["החתול", "החתול"])


def stage7_trigrams():
    """שלב 7 – 3-Gram: המפתח הוא שתי מילים"""
    trigrams = {}
    for i in range(len(CAT) - 2):
        key = " ".join(CAT[i:i + 2])           # "החתול ישן"
        next_word = CAT[i + 2]
        if key not in trigrams:
            trigrams[key] = []
        trigrams[key].append(next_word)
    for key in trigrams:
        print(key, "->", trigrams[key])
    # "החתול" לבד:      ['ישן', 'אכל', 'ישן']
    # "החתול ישן":      ['<EOS>', 'שוב']      <- יותר הקשר, פחות אפשרויות


def stage8_bigger_n():
    """שלב 8 – ככל ש-n גדל, הרשימות מתקצרות"""
    for n in [2, 3, 4, 5]:
        d = {}
        for i in range(len(CAT) - n + 1):
            key = " ".join(CAT[i:i + n - 1])
            if key not in d:
                d[key] = []
            d[key].append(CAT[i + n - 1])
        longest = max(len(v) for v in d.values())
        print(str(n) + "-Gram:", len(d), "מפתחות, הרשימה הארוכה ביותר:", longest)
    # ב-4-Gram כבר לכל מפתח יש רק המשך אחד: המודל רק "מעתיק" את הטקסט


STAGES = [stage1_windows, stage2_dict_basics, stage3_missing_key, stage4_list_values,
          stage5_build_bigrams, stage6_why_repeats, stage7_trigrams, stage8_bigger_n]

if __name__ == "__main__":
    chosen = STAGES
    if len(sys.argv) > 1:
        chosen = [STAGES[int(sys.argv[1]) - 1]]
    for stage in chosen:
        print("=" * 20, stage.__doc__.strip(), "=" * 20)
        try:
            stage()
        except KeyError as e:
            print("KeyError:", e, " <- זו בדיוק הקריסה שרצינו לראות")
        print()
