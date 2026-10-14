# -*- coding: utf-8 -*-
"""
שלב 2: מילוני N-Gram
קוראת רשימת טוקנים מוכנה מקובץ, ובונה מילוני 2,3,4,5-Gram.
לא תלויה ב-Tokenizer שלכם: אפשר להריץ אותה גם לפני שסיימתם את שלב 1.
הריצו מתיקיית LLMClass:
    python main_ngrams.py
"""
import os
import sys

from llmclass.ngrams import build_all_ngrams, next_words

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # כדי שעברית תודפס תקין גם ב-Windows

EOS = "<EOS>"

# כרגע התוכנית קוראת טוקנים מוכנים של קובץ הדוגמה (טוקנים מופרדים ברווח).
# אחרי שה-Tokenizer שלכם עובד ו-main_tokenizer.py שמר את התוצאה,
# אפשר לעבור לקובץ שלכם:  os.path.join("data", "processed", "clean_text.txt")
TOKENS_PATH = os.path.join("data", "raw", "sample_tokens.txt")


def main():
    if not os.path.exists(TOKENS_PATH):
        print("לא נמצא הקובץ", TOKENS_PATH)
        print("בדקו שהקובץ קיים, ושאתם מריצים מתיקיית LLMClass.")
        return

    with open(TOKENS_PATH, "r", encoding="utf-8") as f:
        tokens = f.read().split()
    print("נקראו", len(tokens), "טוקנים")

    all_ngrams = build_all_ngrams(tokens)
    if len(all_ngrams) == 0:
        print("המילון ריק: עוד לא מימשתם את הפונקציות ב-llmclass/ngrams.py.")
        return

    for n in all_ngrams:
        print(str(n) + "-Gram:", len(all_ngrams[n]), "מפתחות")

    bigrams = all_ngrams.get(2, {})
    print("מילים שפותחות משפט:", next_words(bigrams, EOS)[:10])
    print("מה בא אחרי 'החתול':", next_words(bigrams, "החתול"))


if __name__ == "__main__":
    main()
