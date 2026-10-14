# -*- coding: utf-8 -*-
"""
ניסוי ייבוא: האם הקובץ הזה מוצא את החבילה llmclass?
    python demos/try_import.py     -> ModuleNotFoundError  (למה?)
    python -m demos.try_import     -> עובד                 (למה?)
"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

print("פייתון מחפש מודולים קודם כל ב:", sys.path[0] or "(התיקייה הנוכחית)")

from llmclass.tokenizer import EOS

print("הייבוא הצליח! EOS =", EOS)
