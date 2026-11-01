# -*- coding: utf-8 -*-
"""
בדיקה עצמית ליצירת טקסט.
הריצו משורש הפרויקט:
    python -m tests.check_generate
המילונים לבדיקה כתובים כאן, ולא נבנים בקוד שלכם.
אבל generate.py משתמש ב-make_key וב-next_words מ-ngrams.py, אז קודם ודאו ש-check_ngrams מגיע ל-12 מתוך 12.
"""
import copy
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # כדי שעברית תודפס תקין גם ב-Windows

# מוסיפים את שורש הפרויקט לנתיב החיפוש,
# כדי שגם "python tests/check_generate.py" יעבוד
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llmclass import generate as gen

passed = 0
failed = 0
TRIES = 200

# המילונים של "החתול ישן. החתול אכל. החתול ישן שוב."
CAT = {
    2: {"החתול": ["ישן", "אכל", "ישן"], "ישן": ["<EOS>", "שוב"], "<EOS>": ["החתול", "החתול"],
        "אכל": ["<EOS>"], "שוב": ["<EOS>"]},
    3: {"החתול ישן": ["<EOS>", "שוב"], "ישן <EOS>": ["החתול"], "<EOS> החתול": ["אכל", "ישן"],
        "החתול אכל": ["<EOS>"], "אכל <EOS>": ["החתול"], "ישן שוב": ["<EOS>"]},
    4: {}, 5: {},
}

# לכל n המשך אחר, כדי לראות איזה מילון שימש
LEVELS = {
    2: {"ד": ["שתיים"], "ג": ["שתיים"]},
    3: {"ג ד": ["שלוש"]},
    4: {"ב ג ד": ["ארבע"]},
    5: {"א ב ג ד": ["חמש"]},
}

# מילון שבו כל משפט הוא בדיוק "החתול ישן"
FIXED = {2: {"<EOS>": ["החתול"], "החתול": ["ישן"], "ישן": ["<EOS>"]}, 3: {}, 4: {}, 5: {}}

# מילון שבו המשפט לא נגמר לעולם
ENDLESS = {2: {"<EOS>": ["עוד"], "עוד": ["עוד"]}, 3: {}, 4: {}, 5: {}}


def check(name, func):
    global passed, failed
    try:
        func()
        print("✅", name)
        passed += 1
    except AssertionError as e:
        print("❌", name, "->", e)
        failed += 1
    except Exception as e:
        print("💥", name, "-> שגיאה:", type(e).__name__, e)
        failed += 1


def expect(actual, expected):
    assert actual == expected, "קיבלנו " + repr(actual) + " אבל ציפינו ל- " + repr(expected)


def t_choose_missing():
    expect(gen.choose_next(CAT[2], "כלב"), None)
    expect(gen.choose_next({}, "החתול"), None)


def t_choose_single():
    for _ in range(20):
        expect(gen.choose_next(CAT[2], "אכל"), "<EOS>")


def t_choose_random():
    seen = set()
    for _ in range(TRIES):
        word = gen.choose_next(CAT[2], "החתול")
        assert word in ["ישן", "אכל"], "המילה " + repr(word) + " לא באה אחרי 'החתול'"
        seen.add(word)
    expect(sorted(seen), ["אכל", "ישן"])


def t_choose_unchanged():
    before = copy.deepcopy(CAT)
    for _ in range(20):
        gen.choose_next(CAT[2], "החתול")
    assert CAT == before, "choose_next שינתה את המילון"


def t_next_uses_5():
    expect(gen.next_word(LEVELS, ["א", "ב", "ג", "ד"]), "חמש")


def t_backoff_4_3():
    expect(gen.next_word(LEVELS, ["ז", "ב", "ג", "ד"]), "ארבע")
    expect(gen.next_word(LEVELS, ["ז", "ז", "ג", "ד"]), "שלוש")


def t_backoff_2():
    expect(gen.next_word(LEVELS, ["ז", "ז", "ז", "ד"]), "שתיים")
    expect(gen.next_word(CAT, ["אכל"]), "<EOS>")


def t_random_fallback():
    seen = set()
    for _ in range(TRIES):
        word = gen.next_word(CAT, ["כלב"])
        assert word in CAT[2], "המילה " + repr(word) + " היא לא מפתח במילון ה-2-Gram"
        seen.add(word)
    assert len(seen) > 1, "המילה האקראית תמיד יוצאת אותה מילה: " + repr(seen)


def t_short_history():
    expect(gen.next_word(LEVELS, ["ג", "ד"]), "שלוש")
    expect(gen.next_word(LEVELS, ["ד"]), "שתיים")
    for _ in range(20):
        expect(gen.next_word(CAT, ["<EOS>"]), "החתול")


def t_history_unchanged():
    history = ["<EOS>", "החתול"]
    for _ in range(20):
        gen.next_word(CAT, history)
    expect(history, ["<EOS>", "החתול"])


def t_sentence_fixed():
    expect(gen.generate_sentence(FIXED, 10), ["החתול", "ישן"])


def t_sentence_max():
    expect(gen.generate_sentence(ENDLESS, 5), ["עוד", "עוד", "עוד", "עוד", "עוד"])
    expect(gen.generate_sentence(ENDLESS, 1), ["עוד"])


def t_sentence_cat():
    for _ in range(50):
        words = gen.generate_sentence(CAT, 10)
        assert "<EOS>" not in words, "<EOS> נכנס למשפט: " + repr(words)
        assert len(words) > 0 and words[0] == "החתול", "המשפט לא מתחיל במילה שפותחת משפט: " + repr(words)


def t_text_fixed():
    expect(gen.generate_text(FIXED, 3, 10), "החתול ישן. החתול ישן. החתול ישן.")
    expect(gen.generate_text(FIXED, 1, 10), "החתול ישן.")


def t_text_cat():
    for _ in range(20):
        text = gen.generate_text(CAT, 4, 10)
        expect(type(text), str)
        assert "<EOS>" not in text, "<EOS> נכנס לטקסט: " + repr(text)
        assert text.count(".") == 4 and text.endswith("."), "ציפינו ל-4 משפטים שנגמרים בנקודה: " + repr(text)


tests = [
    ("choose_next מחזירה None על מפתח חסר", t_choose_missing),
    ("choose_next עם אפשרות אחת", t_choose_single),
    ("choose_next בוחרת באקראי", t_choose_random),
    ("choose_next לא משנה את המילון", t_choose_unchanged),
    ("next_word משתמשת קודם ב-5-Gram", t_next_uses_5),
    ("next_word יורדת ל-4-Gram ול-3-Gram", t_backoff_4_3),
    ("next_word יורדת ל-2-Gram", t_backoff_2),
    ("next_word: מילה אקראית כשאין המשך", t_random_fallback),
    ("next_word עם history קצר", t_short_history),
    ("next_word לא משנה את history", t_history_unchanged),
    ("generate_sentence: משפט קבוע", t_sentence_fixed),
    ("generate_sentence עוצרת ב-max_words", t_sentence_max),
    ("generate_sentence: בלי <EOS>, ומתחילה כמו משפט", t_sentence_cat),
    ("generate_text: מספר המשפטים והנקודות", t_text_fixed),
    ("generate_text: מחרוזת, בלי <EOS>", t_text_cat),
]

print("=" * 50)
for name, func in tests:
    check(name, func)
print("=" * 50)
print("עברו:", passed, "/", passed + failed)
if failed == 0:
    print("🎉 כל הכבוד! מחולל הטקסט שלכם עומד בכל הדרישות.")
