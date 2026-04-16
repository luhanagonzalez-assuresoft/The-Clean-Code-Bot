class Validator:
    MAX_FILE_SIZE = 100_000  # characters

    @staticmethod
    def validate(code: str):
        if not code:
            raise ValueError("Empty input file")

        if len(code) > Validator.MAX_FILE_SIZE:
            raise ValueError("File too large")

        # Optional: restrict binary content
        if "\x00" in code:
            raise ValueError("Binary content detected")