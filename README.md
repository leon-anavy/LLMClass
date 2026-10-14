# LLMClass

פרויקט NLP: מטקסט גולמי ועד מודל שפה פשוט. כל שבוע מוסיפים מודול חדש לתיקייה `llmclass/`.

## מבנה הפרויקט

```
LLMClass/
├── ASSIGNMENT.docx          # הוראות הגשה (Word)
├── ASSIGNMENT.md            # הוראות הגשה (טקסט)
├── PROJECT_STRUCTURE.docx   # הסבר: מבנה פרויקט, מודולים וייבוא
├── main.py                  # התוכנית הראשית
├── llmclass/                # הקוד שאתם כותבים
│   ├── __init__.py
│   ├── tokenizer.py         # שבוע 2: פונקציות ה-Tokenizer
│   └── ngrams.py            # שבוע 3: מילוני N-Gram
├── data/
│   ├── raw/                 # קבצי המקור. לא משנים אותם לעולם
│   └── processed/           # כאן הקוד שומר את התוצאות
├── tests/
│   ├── check_tokenizer.py   # בדיקה עצמית ל-Tokenizer
│   └── check_ngrams.py      # בדיקה עצמית ל-N-Gram
└── demos/
    ├── tokenizer_demos.py   # ההדגמות משיעור הטוקניזציה
    ├── ngram_demos.py       # ההדגמות משיעור ה-N-Gram
    ├── where_am_i.py        # מדפיס מאיפה פייתון רץ ומחפש
    └── try_import.py        # ניסוי: מתי ייבוא מצליח ומתי לא
```

## לפני שמתחילים

1. `main.py` רץ כרגע על קובץ הדוגמה `data/raw/sample_dirty.txt`. כשתורידו קורפוס גדול יותר, שימו אותו ב-`data/raw/` ועדכנו את `CORPUS_PATH` ב-`main.py`.
2. ב-PyCharm: **File > Open**, ובחרו את התיקייה `LLMClass` עצמה (זו שיש בה את `main.py`).

הסבר מלא, כולל הורדה וחילוץ: ב-ASSIGNMENT.docx.

## איך מריצים

כל הפקודות רצות מהתיקייה `LLMClass`:

```
python -m tests.check_tokenizer     # בדיקה עצמית: צריך להגיע ל-11 מתוך 11
python -m tests.check_ngrams        # בדיקה עצמית: צריך להגיע ל-12 מתוך 12
python main.py                      # מנקה, שומר ל-data/processed/clean_text.txt ובונה מילוני N-Gram
python demos/tokenizer_demos.py 4    # הדגמה של שלב 4 מהשיעור
python demos/ngram_demos.py 5        # בניית מילון 2-Gram צעד אחר צעד
```

## המשימות

- **שבוע 2:** השלימו את כל ה-TODO בקובץ `llmclass/tokenizer.py`.
- **שבוע 3:** השלימו את כל ה-TODO בקובץ `llmclass/ngrams.py`. מפתח הוא n-1 מילים מחוברות ברווח, והערך הוא רשימת כל המילים שבאו אחריהן, **כולל חזרות**.

בשני הקבצים: אל תשנו שמות של פונקציות או פרמטרים.

הגשת ה-Tokenizer ואיך היא נבדקת: **ASSIGNMENT.docx** (אותו תוכן גם ב-[ASSIGNMENT.md](ASSIGNMENT.md))
