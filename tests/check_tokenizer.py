# -*- coding: utf-8 -*-
"""
בדיקה עצמית לפונקציות ה-Tokenizer.
הריצו מתיקיית LLMClass (התיקייה הראשית של הפרויקט):
    python -m tests.check_tokenizer
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # כדי שעברית תודפס תקין גם ב-Windows

# מוסיפים את התיקייה הראשית של הפרויקט לנתיב החיפוש,
# כדי שגם "python tests/check_tokenizer.py" יעבוד
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llmclass import tokenizer as tk

passed = 0
failed = 0


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


# ---------- הבדיקות ----------
def t_load():
    with open("_test_in.txt", "w", encoding="utf-8") as f:
        f.write("שלום עולם\nשורה שנייה")
    try:
        expect(tk.load_text("_test_in.txt"), "שלום עולם\nשורה שנייה")
    finally:
        os.remove("_test_in.txt")


def t_sentences():
    out = tk.mark_sentences("שלום. מה נשמע? יופי!")
    expect(out.split(), ["שלום", "<EOS>", "מה", "נשמע", "<EOS>", "יופי", "<EOS>"])


def t_eos_spaces():
    out = tk.mark_sentences("סוף.התחלה")
    expect(out.split(), ["סוף", "<EOS>", "התחלה"])


def t_hyphens():
    expect(tk.split_hyphens("חתול-ים"), "חתול ים")


def t_punct():
    expect(tk.remove_punctuation('שלום, אמר: "היי" (בשקט)'), "שלום אמר היי בשקט")


def t_spaces():
    expect(tk.normalize_spaces("   אני \t  אוהב\n\n  פייתון   "), "אני אוהב פייתון")


def t_clean_he():
    expect(tk.clean("  הילד הלך-הביתה.   הוא, אכל!  "),
           "הילד הלך הביתה <EOS> הוא אכל <EOS>")


def t_tokenize_type():
    out = tk.tokenize("שלום עולם.")
    assert isinstance(out, list), "tokenize צריכה להחזיר list, אבל החזירה " + type(out).__name__
    expect(out, ["שלום", "עולם", "<EOS>"])


def t_tokenize():
    expect(tk.tokenize('ד"ר כהן אמר: "חתול-ים יפים".'),
           ["דר", "כהן", "אמר", "חתול", "ים", "יפים", "<EOS>"])


def t_repeats_kept():
    tokens = tk.tokenize("חתול חתול חתול. חתול!")
    expect(tokens.count("חתול"), 4)


def t_save():
    tokens = ["שלום", "עולם", "<EOS>"]
    tk.save_tokens(tokens, "_test_out.txt")
    try:
        with open("_test_out.txt", "r", encoding="utf-8") as f:
            expect(f.read(), "שלום עולם <EOS>")
    finally:
        os.remove("_test_out.txt")


tests = [
    ("load_text קורא עברית ב-UTF-8", t_load),
    ("mark_sentences: נקודה/סימן שאלה/קריאה -> <EOS>", t_sentences),
    ("mark_sentences: <EOS> לא נדבק למילים", t_eos_spaces),
    ("split_hyphens", t_hyphens),
    ("remove_punctuation", t_punct),
    ("normalize_spaces", t_spaces),
    ("clean בעברית", t_clean_he),
    ("tokenize – משפט קצר", t_tokenize_type),
    ("tokenize – דוגמה מלאה", t_tokenize),
    ("חזרות לא נמחקות", t_repeats_kept),
    ("save_tokens כותב קובץ תקין", t_save),
]

print("=" * 50)
for name, func in tests:
    check(name, func)
print("=" * 50)
print("עברו:", passed, "/", passed + failed)
if failed == 0:
    print("🎉 כל הכבוד! ה-Tokenizer שלכם עומד בכל הדרישות.")
