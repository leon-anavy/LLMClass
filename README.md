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
│   └── tokenizer.py         # שבוע 2: פונקציות ה-Tokenizer
├── data/
│   ├── raw/                 # קבצי המקור. לא משנים אותם לעולם
│   └── processed/           # כאן הקוד שומר את התוצאות
├── tests/
│   └── check_tokenizer.py   # בדיקה עצמית
└── demos/
    ├── tokenizer_demos.py    # ההדגמות מהשיעור
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
python main.py                      # מריץ על הקורפוס ושומר ל-data/processed/clean_text.txt
python demos/tokenizer_demos.py 4    # הדגמה של שלב 4 מהשיעור
```

## המשימה של השבוע

השלימו את כל ה-TODO בקובץ `llmclass/tokenizer.py`. אל תשנו שמות של פונקציות או פרמטרים.

מה מגישים ואיך זה נבדק: **ASSIGNMENT.docx** (אותו תוכן גם ב-[ASSIGNMENT.md](ASSIGNMENT.md))
