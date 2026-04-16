# core/processor.py
from core.sanitizer import Sanitizer
from core.validator import Validator
from core.formatter import Formatter
from services.llm_service import LLMService
from utils.file_handler import FileHandler

class CodeProcessor:
    def __init__(self):
        self.llm = LLMService()

    def process(self, input_path: str, output_path: str):
        code = FileHandler.read_file(input_path)

        Validator.validate(code)
        clean_code = Sanitizer.sanitize(code)

        optimized_code = self.llm.refactor(clean_code)

        optimized_code = Formatter.clean_output(optimized_code)

        FileHandler.write_file(output_path, optimized_code)

        print(f"✅ Optimized code written to {output_path}")