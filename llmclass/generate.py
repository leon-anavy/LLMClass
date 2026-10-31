# -*- coding: utf-8 -*-
"""
יצירת טקסט
==========
הוראות הגשה מלאות: ב-Google Classroom
השלימו כל פונקציה במקום שכתוב בו TODO, ומחקו את שורת ה-return הזמנית.
אל תשנו את שמות הפונקציות או את הפרמטרים – קובץ הבדיקה מסתמך עליהם.

הפעם ההסברים קצרים יותר: מה הפונקציה מקבלת ומה היא מחזירה. איך לעשות את זה, אתם מחליטים.
כל מה שצריך כבר למדנו בשיעור: next_words, make_key, random.choice, חיתוך רשימה, לולאות.

בדיקה עצמית (משורש הפרויקט):   python -m tests.check_generate
"""
import random

from llmclass.ngrams import N_VALUES, make_key, next_words

EOS = "<EOS>"


def choose_next(ngrams, key):
    """
    מחזירה מילה אקראית מבין המילים שבאו אחרי key במילון ngrams.
    אם key לא הופיע אף פעם, מחזירה None.
    choose_next({"החתול": ["ישן", "אכל", "ישן"]}, "החתול")  ->  "ישן" או "אכל"
    """
    # TODO
    return None   # זמני


def next_word(all_ngrams, history):
    """
    מקבלת את מילון המילונים (2 עד 5) ואת רשימת המילים שנוצרו עד עכשיו, ומחזירה את המילה הבאה.
    Back-off: מנסים קודם את המילון של ה-n הגדול ביותר, לפי n-1 המילים האחרונות ב-history.
    אין שם המשך? יורדים ל-n הבא, עד 2. גם שם אין? מילה אקראית מתוך המפתחות של מילון ה-2-Gram.
    history לא משתנה.
    """
    # TODO
    return EOS   # זמני


def generate_sentence(all_ngrams, max_words):
    """
    מחזירה משפט אחד, כרשימת מילים בלי <EOS>.
    המשפט מתחיל כמו משפט אמיתי בטקסט: אחרי <EOS>.
    נגמר כשנבחר <EOS>, או כשיש בו max_words מילים.
    """
    # TODO
    return []   # זמני


def generate_text(all_ngrams, num_sentences, max_words):
    """
    מחזירה טקסט (מחרוזת) של num_sentences משפטים בדיוק.
    כל משפט נגמר בנקודה, ובין משפט למשפט יש רווח.
    "החתול ישן. הכלב אכל עצם."
    """
    # TODO
    return ""   # זמני
