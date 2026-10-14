# -*- coding: utf-8 -*-
"""
איפה אני? מדפיס את ארבעת הדברים שקובעים איך פייתון מוצא קבצים ומודולים.
נסו להריץ אותו מכמה מקומות שונים ולהשוות:
    python demos/where_am_i.py          (מתיקיית LLMClass)
    python -m demos.where_am_i          (מתיקיית LLMClass)
    cd demos  ואז  python where_am_i.py
"""
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("1. הקובץ שרץ עכשיו  (__file__):  ", __file__)
print("2. שם המודול       (__name__):  ", __name__)
print("3. תיקיית העבודה   (os.getcwd()):", os.getcwd())
print("4. פייתון מחפש מודולים קודם כל ב- (sys.path[0]):", sys.path[0] or "(התיקייה הנוכחית)")
