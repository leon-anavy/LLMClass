# -*- coding: utf-8 -*-
"""
משימה: פונקציות ה-Tokenizer
==========================
הוראות הגשה מלאות: ASSIGNMENT.md
השלימו כל פונקציה במקום שכתוב בו TODO (ומחקו את ה-pass).
אל תשנו את שמות הפונקציות או את הפרמטרים – קובץ הבדיקה מסתמך עליהם.

בדיקה עצמית (מתיקיית LLMClass):   python -m tests.check_tokenizer
הרצה על הקורפוס:                   python main.py
"""

# קבועים. אל תשנו אותם.
EOS = "<EOS>"
SENTENCE_END = [".", "!", "?"]
PUNCTUATION = [",", ";", ":", '"', "'", "(", ")", "[", "]", "״", "׳"]


# ---------- 1. קריאה ----------
def load_text(path):
    """
    קוראת את הקובץ שבנתיב path ומחזירה את כל הטקסט כמחרוזת אחת.
    חובה: encoding="utf-8"
    """
    # TODO
    pass


# ---------- 2. פעולות ניקוי (כל אחת מקבלת מחרוזת ומחזירה מחרוזת) ----------
def mark_sentences(text):
    """
    מחליפה כל סימן מתוך SENTENCE_END ב-" <EOS> " (עם רווח לפני ואחרי!).
    רמז: לולאת for על SENTENCE_END
    """
    # TODO
    pass


def split_hyphens(text):
    """
    מחליפה כל מקף "-" ברווח.  "חתול-ים" -> "חתול ים"
    """
    # TODO
    pass


def remove_punctuation(text):
    """
    מוחקת (מחליפה במחרוזת ריקה) כל תו שנמצא ב-PUNCTUATION
    """
    # TODO
    pass


def normalize_spaces(text):
    """
    מחליפה כל רצף של רווחים / טאבים / ירידות שורה ברווח אחד,
    ומסירה רווחים מההתחלה ומהסוף.
    רמז: split + join
    """
    # TODO
    pass


# ---------- 3. כל הניקוי ביחד ----------
def clean(text):
    """
    מפעילה את ארבע פעולות הניקוי לפי הסדר ומחזירה טקסט נקי:
    mark_sentences -> split_hyphens -> remove_punctuation -> normalize_spaces

    אם הטקסט באנגלית: מוסיפים בהתחלה  text = text.lower()
    (לפני mark_sentences, אחרת <EOS> יהפוך ל-<eos>)

    ליד כל שורה כאן: הערה (#) קצרה במילים שלכם – מה השלב עושה.
    """
    # TODO
    pass


# ---------- 4. טוקניזציה ----------
def tokenize(text):
    """
    מנקה את הטקסט (בעזרת clean) ומחזירה רשימה (list) של טוקנים.
    """
    # TODO
    pass


# ---------- 5. שמירה ----------
def save_tokens(tokens, path):
    """
    שומרת את הטוקנים לקובץ חדש בנתיב path:
    כל הטוקנים מחוברים ברווח אחד, ב-encoding="utf-8".
    """
    # TODO
    pass
