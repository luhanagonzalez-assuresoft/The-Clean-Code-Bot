# core/formatter.py
import re

class Formatter:
    @staticmethod
    def clean_output(text: str) -> str:
        # Remove triple backticks
        return re.sub(r"```.*?\n|```", "", text, flags=re.DOTALL).strip()