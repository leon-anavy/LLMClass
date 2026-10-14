# -*- coding: utf-8 -*-
"""
התוכנית הראשית: קוראת את הקורפוס, מנקה, מפרקת לטוקנים ושומרת.
הריצו מתיקיית LLMClass:
    python main.py
"""
import os
import sys

from llmclass.tokenizer import EOS, load_text, save_tokens, tokenize

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # כדי שעברית תודפס תקין גם ב-Windows

CORPUS_PATH = os.path.join("data", "raw", "corpus_ngram_1000_words.txt")
OUTPUT_PATH = os.path.join("data", "processed", "clean_text.txt")


def main():
    if not os.path.exists(CORPUS_PATH):
        print("לא נמצא הקובץ", CORPUS_PATH)
        print("שימו את הקורפוס בתיקייה data/raw, והריצו מתיקיית LLMClass.")
        return

    raw = load_text(CORPUS_PATH)
    tokens = tokenize(raw)

    print("20 הטוקנים הראשונים:", tokens[:20])
    print("מספר טוקנים:", len(tokens))
    print("מספר משפטים:", tokens.count(EOS))

    save_tokens(tokens, OUTPUT_PATH)
    print("נשמר ל-" + OUTPUT_PATH)


if __name__ == "__main__":
    main()
