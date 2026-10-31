# -*- coding: utf-8 -*-
"""
הדגמות חיות לשיעור "יצירת טקסט".
כל שלב הוא פונקציה – מריצים אחת-אחת מול הכיתה:
    python demos/generate_demos.py 3      (מריץ רק את שלב 3, מ-1 עד 7)
    python demos/generate_demos.py        (מריץ הכל)
הקובץ לא משתמש בקוד שלכם, כך שהוא עובד גם לפני שהשלמתם את המשימה.
"""
import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EOS = "<EOS>"

# הטקסט של השיעור, אחרי ה-Tokenizer:
# "החתול ישן על הספה. הכלב ישן על הרצפה. החתול אכל דג. הכלב אכל עצם. הילד ראה את החתול. הילד ראה את הכלב."
TOY = ("החתול ישן על הספה <EOS> הכלב ישן על הרצפה <EOS> החתול אכל דג <EOS> "
       "הכלב אכל עצם <EOS> הילד ראה את החתול <EOS> הילד ראה את הכלב <EOS>").split()


def build(tokens, n):
    """בונה מילון N-Gram, כמו build_ngrams מהמשימה הקודמת"""
    d = {}
    for i in range(len(tokens) - n + 1):
        key = " ".join(tokens[i:i + n - 1])
        if key not in d:
            d[key] = []
        d[key].append(tokens[i + n - 1])
    return d


BIGRAMS = build(TOY, 2)
TRIGRAMS = build(TOY, 3)


def predict_2(word):
    """המילה הבאה לפי 2-Gram: מילה אחת אחורה"""
    options = BIGRAMS.get(word, [])
    if len(options) == 0:
        return None
    return random.choice(options)


def predict_3(word1, word2):
    """המילה הבאה לפי 3-Gram: שתי מילים אחורה"""
    options = TRIGRAMS.get(word1 + " " + word2, [])
    if len(options) == 0:
        return None
    return random.choice(options)


def stage1_peek():
    """שלב 1 – מציצים במילונים: כמה מפתחות אקראיים לכל n"""
    for n in [2, 3, 4]:
        d = build(TOY, n)
        print(str(n) + "-Gram:", len(d), "מפתחות")
        for key in random.sample(list(d.keys()), 3):
            print("   ", key, "->", d[key])
    # בבית, על הטקסט שלכם:  random.sample(list(all_ngrams[3].keys()), 3)


def stage2_bigram():
    """שלב 2 – מילה הבאה לפי 2-Gram"""
    for word in ["ישן", "על", "הילד", "פיל"]:
        print(word, "->", BIGRAMS.get(word, []), "  נבחרה:", predict_2(word))
    # "על" -> ['הספה', 'הרצפה']: כל פעם אחרת
    # "פיל" לא הופיע בטקסט: אין המשך -> None


def stage3_trigram():
    """שלב 3 – מילה הבאה לפי 3-Gram: המפתח הוא שתי מילים"""
    for w1, w2 in [("החתול", "ישן"), ("הכלב", "ישן"), ("ראה", "את"), ("הכלב", "ראה")]:
        print(w1, w2, "->", TRIGRAMS.get(w1 + " " + w2, []), "  נבחרה:", predict_3(w1, w2))
    # "הכלב ראה" לא הופיע אף פעם, למרות ש"הכלב" ו"ראה" כן -> None


def sentence_2():
    words = [predict_2(EOS)]
    while words[-1] != EOS and len(words) < 12:
        words.append(predict_2(words[-1]))
    return " ".join(words)


def sentence_3():
    words = [EOS, predict_2(EOS)]                 # מילה ראשונה: אין עדיין שתי מילים אחורה
    while words[-1] not in [EOS, None] and len(words) < 12:
        words.append(predict_3(words[-2], words[-1]))
    return " ".join(w if w is not None else "???" for w in words[1:])


def stage4_compare():
    """שלב 4 – 2-Gram מול 3-Gram: חמישה משפטים מכל אחד"""
    print("2-Gram:")
    for _ in range(5):
        print("   ", sentence_2())
    print("3-Gram:")
    for _ in range(5):
        print("   ", sentence_3())
    # 2-Gram: משפטים חדשים ("הכלב אכל דג"), אבל גם שטויות ("הילד ראה את הכלב ישן על הספה")
    # 3-Gram: נשמע נכון, אבל כמעט רק מעתיק משפטים מהטקסט


def predict_backoff(history):
    """3-Gram אם יש, אחרת 2-Gram, אחרת מילה אקראית"""
    if len(history) >= 2:
        word = predict_3(history[-2], history[-1])
        if word is not None:
            return word, "3-Gram"
    word = predict_2(history[-1])
    if word is not None:
        return word, "2-Gram"
    return random.choice(list(BIGRAMS.keys())), "אקראית"


def stage5_backoff():
    """שלב 5 – Back-off: 3-Gram, אחרת 2-Gram, אחרת מילה אקראית"""
    for history in [["הכלב", "ישן"], ["הכלב", "ראה"], ["פיל"]]:
        word, used = predict_backoff(history)
        print(history, "->", word, "  (" + used + ")")
    # בפרויקט: אותו רעיון, מ-5-Gram ועד 2-Gram


def stage6_first_word():
    """שלב 6 – המילה הראשונה: מה בא אחרי <EOS>?"""
    print("פותחות משפט:", BIGRAMS[EOS])
    history = [EOS]                     # מתחילים כאילו משפט קודם בדיוק נגמר
    while len(history) < 12:
        word, used = predict_backoff(history)
        print("   ", word, "(" + used + ")")
        if word == EOS:
            break
        history.append(word)
    print("המשפט:", " ".join(history[1:]))


def stage7_many_sentences():
    """שלב 7 – יותר ממשפט אחד"""
    print("(א) לולאה: כל משפט מתחיל מחדש אחרי <EOS>")
    for _ in range(3):
        print("   ", sentence_2())
    print("(ב) היסטוריה אחת שממשיכה: <EOS> נשאר בתוכה")
    history = [EOS]
    while history.count(EOS) < 4:
        word, used = predict_backoff(history)
        history.append(word)
    print("   ", " ".join(history))
    # ב-(ב) המפתח "דג <EOS>" קובע איך יתחיל המשפט הבא: המשפטים מחוברים זה לזה


STAGES = [stage1_peek, stage2_bigram, stage3_trigram, stage4_compare,
          stage5_backoff, stage6_first_word, stage7_many_sentences]

if __name__ == "__main__":
    chosen = STAGES
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if not arg.isdigit() or not 1 <= int(arg) <= len(STAGES):
            print("אין שלב כזה:", arg, " בחרו מספר בין 1 ל-" + str(len(STAGES)))
            sys.exit(1)
        chosen = [STAGES[int(arg) - 1]]
    for stage in chosen:
        print("=" * 20, stage.__doc__.strip(), "=" * 20)
        stage()
        print()
