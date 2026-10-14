# -*- coding: utf-8 -*-
"""
בדיקה עצמית למילוני ה-N-Gram.
הריצו מתיקיית LLMClass (התיקייה הראשית של הפרויקט):
    python -m tests.check_ngrams
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # כדי שעברית תודפס תקין גם ב-Windows

# מוסיפים את התיקייה הראשית של הפרויקט לנתיב החיפוש,
# כדי שגם "python tests/check_ngrams.py" יעבוד
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llmclass import ngrams as ng

passed = 0
failed = 0

# הטוקנים מהשיעור: "החתול ישן. החתול אכל. החתול ישן שוב."
CAT = ["החתול", "ישן", "<EOS>", "החתול", "אכל", "<EOS>", "החתול", "ישן", "שוב", "<EOS>"]


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


def t_make_key():
    expect(ng.make_key(["החתול", "ישן"]), "החתול ישן")
    expect(ng.make_key(["החתול"]), "החתול")
    expect(ng.make_key(["a", "b", "c", "d"]), "a b c d")


def t_bigrams_type():
    result = ng.build_bigrams(["א", "ב"])
    expect(type(result), dict)
    expect(result, {"א": ["ב"]})


def t_bigrams():
    expect(ng.build_bigrams(CAT), {
        "החתול": ["ישן", "אכל", "ישן"],
        "ישן": ["<EOS>", "שוב"],
        "<EOS>": ["החתול", "החתול"],
        "אכל": ["<EOS>"],
        "שוב": ["<EOS>"],
    })


def t_repeats_kept():
    d = ng.build_bigrams(["א", "ב", "א", "ב", "א", "ב"])
    expect(d["א"], ["ב", "ב", "ב"])


def t_last_word():
    d = ng.build_bigrams(["אחת", "שתיים", "שלוש"])
    assert "שלוש" not in d, "למילה האחרונה אין מילה אחריה, אז היא לא אמורה להיות מפתח"
    expect(len(d), 2)


def t_short():
    expect(ng.build_bigrams(["לבד"]), {})
    expect(ng.build_bigrams([]), {})
    expect(ng.build_bigrams(["שתי", "מילים"]), {"שתי": ["מילים"]})


def t_tokens_unchanged():
    tokens = list(CAT)
    result = ng.build_ngrams(tokens, 3)
    expect(len(result), 6)
    expect(tokens, CAT)


def t_ngrams_2():
    expect(len(ng.build_ngrams(CAT, 2)), 5)
    expect(ng.build_ngrams(CAT, 2), ng.build_bigrams(CAT))


def t_ngrams_3():
    expect(ng.build_ngrams(CAT, 3), {
        "החתול ישן": ["<EOS>", "שוב"],
        "ישן <EOS>": ["החתול"],
        "<EOS> החתול": ["אכל", "ישן"],
        "החתול אכל": ["<EOS>"],
        "אכל <EOS>": ["החתול"],
        "ישן שוב": ["<EOS>"],
    })


def t_ngrams_5():
    d = ng.build_ngrams(CAT, 5)
    expect(len(d), 6)    # 10 טוקנים, 5-Gram: 10 - 5 + 1 = 6 חלונות, כולם שונים
    expect(d["החתול ישן <EOS> החתול"], ["אכל"])
    expect(ng.build_ngrams(["א", "ב", "ג"], 5), {})


def t_all():
    all_ngrams = ng.build_all_ngrams(CAT)
    expect(sorted(all_ngrams.keys()), [2, 3, 4, 5])
    expect(all_ngrams[3], ng.build_ngrams(CAT, 3))
    expect(all_ngrams[4]["<EOS> החתול ישן"], ["שוב"])


def t_next_words():
    d = ng.build_bigrams(CAT)
    expect(ng.next_words(d, "החתול"), ["ישן", "אכל", "ישן"])
    expect(ng.next_words(d, "כלב"), [])


tests = [
    ("make_key מחברת מילים ברווח", t_make_key),
    ("build_bigrams על שתי מילים", t_bigrams_type),
    ("build_bigrams – הדוגמה מהשיעור", t_bigrams),
    ("חזרות נשמרות ברשימה", t_repeats_kept),
    ("המילה האחרונה לא נכנסת כמפתח", t_last_word),
    ("רשימה קצרה: מילון ריק או זוג אחד", t_short),
    ("הפונקציות לא משנות את רשימת הטוקנים", t_tokens_unchanged),
    ("build_ngrams עם n=2 זהה ל-build_bigrams", t_ngrams_2),
    ("build_ngrams עם n=3", t_ngrams_3),
    ("build_ngrams עם n=5", t_ngrams_5),
    ("build_all_ngrams בונה 2,3,4,5", t_all),
    ("next_words לא קורסת על מפתח חסר", t_next_words),
]

print("=" * 50)
for name, func in tests:
    check(name, func)
print("=" * 50)
print("עברו:", passed, "/", passed + failed)
if failed == 0:
    print("🎉 כל הכבוד! מילוני ה-N-Gram שלכם עומדים בכל הדרישות.")
