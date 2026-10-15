# LLMClass

פרויקט NLP: מטקסט גולמי ועד מודל שפה פשוט. כל שבוע מוסיפים מודול חדש לתיקייה `llmclass/`.

## מבנה הפרויקט

```
LLMClass/
├── main_tokenizer.py        # שלב 1: מריצים את ה-Tokenizer על הקורפוס
├── main_ngrams.py           # שלב 2: בונים מילוני N-Gram (לא תלוי בשלב 1)
├── llmclass/                # הקוד שאתם כותבים
│   ├── __init__.py
│   ├── tokenizer.py         # שבוע 2: פונקציות ה-Tokenizer
│   └── ngrams.py            # שבוע 3: מילוני N-Gram
├── data/
│   ├── raw/                 # קבצי המקור. לא משנים אותם לעולם
│   │   ├── sample_dirty.txt     # טקסט לדוגמה לשלב 1
│   │   ├── sample_dirty_en.txt  # טקסט לדוגמה באנגלית, למי שרוצה לנסות
│   │   └── sample_tokens.txt    # טוקנים מוכנים לשלב 2
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

1. `main_tokenizer.py` רץ כרגע על קובץ הדוגמה `data/raw/sample_dirty.txt`. כשתורידו קורפוס גדול יותר, שימו אותו ב-`data/raw/` ועדכנו את `CORPUS_PATH`.
2. `main_ngrams.py` קורא טוקנים מוכנים מ-`data/raw/sample_tokens.txt`, כך שהוא עובד גם לפני שה-Tokenizer שלכם גמור. אחרי ש-`main_tokenizer.py` שמר את `data/processed/clean_text.txt`, אפשר לעדכן את `TOKENS_PATH` לקובץ הזה.
3. ב-PyCharm: **File > Open**, ובחרו את התיקייה `LLMClass` עצמה (זו שיש בה את `main_tokenizer.py`).

בכל פונקציה בשלד יש שורת `return` זמנית שמחזירה ערך מהסוג הנכון, כדי שהתוכניות ירוצו בלי לקרוס עוד לפני שסיימתם. כשאתם מממשים פונקציה, מחקו את השורה הזמנית.

הוראות ההגשה של כל משימה, כולל הורדה, חילוץ ועבודה מהבית: ב-Google Classroom.

## איך מריצים

כל הפקודות רצות מהתיקייה `LLMClass`:

```
python -m tests.check_tokenizer     # בדיקה עצמית: צריך להגיע ל-11 מתוך 11
python -m tests.check_ngrams        # בדיקה עצמית: צריך להגיע ל-12 מתוך 12
python main_tokenizer.py            # מנקה ושומר ל-data/processed/clean_text.txt
python main_ngrams.py               # בונה מילוני 2,3,4,5-Gram
python demos/tokenizer_demos.py 4    # הדגמה של שלב 4 מהשיעור
python demos/ngram_demos.py 5        # בניית מילון 2-Gram צעד אחר צעד
```

## המשימות

- **שבוע 2:** השלימו את כל ה-TODO בקובץ `llmclass/tokenizer.py`.
- **שבוע 3:** השלימו את כל ה-TODO בקובץ `llmclass/ngrams.py`. מפתח הוא n-1 מילים מחוברות ברווח, והערך הוא רשימת כל המילים שבאו אחריהן, **כולל חזרות**.

בשני הקבצים: אל תשנו שמות של פונקציות או פרמטרים.

