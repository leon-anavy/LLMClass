# -*- coding: utf-8 -*-
"""
התוכנית הראשית: קוראת את הקורפוס, מנקה, מפרקת לטוקנים, שומרת ובונה מילוני N-Gram.
הריצו מתיקיית LLMClass:
    python main.py
"""
import os
import sys

from llmclass.ngrams import build_all_ngrams, next_words
from llmclass.tokenizer import EOS, load_text, save_tokens, tokenize

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # כדי שעברית תודפס תקין גם ב-Windows

# כרגע התוכנית רצה על קובץ הדוגמה הקטן בעברית.
# אחרי שתורידו קורפוס גדול יותר ותשימו אותו בתיקייה data/raw,
# עדכנו כאן את שם הקובץ, למשל: "corpus_ngram_1000_words.txt"
CORPUS_PATH = os.path.join("data", "raw", "sample_dirty.txt")
OUTPUT_PATH = os.path.join("data", "processed", "clean_text.txt")


def main():
    if not os.path.exists(CORPUS_PATH):
        print("לא נמצא הקובץ", CORPUS_PATH)
        print("בדקו שהקובץ נמצא בתיקייה data/raw, ושאתם מריצים מתיקיית LLMClass.")
        return

    raw = load_text(CORPUS_PATH)
    tokens = tokenize(raw)

    print("20 הטוקנים הראשונים:", tokens[:20])
    print("מספר טוקנים:", len(tokens))
    print("מספר משפטים:", tokens.count(EOS))

    save_tokens(tokens, OUTPUT_PATH)
    print("נשמר ל-" + OUTPUT_PATH)

    # ---------- מילוני N-Gram ----------
    all_ngrams = build_all_ngrams(tokens)
    for n in all_ngrams:
        print(str(n) + "-Gram:", len(all_ngrams[n]), "מפתחות")
    print("מילים שפותחות משפט:", next_words(all_ngrams[2], EOS)[:10])


if __name__ == "__main__":
    main()
