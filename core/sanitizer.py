import re

class Sanitizer:
    @staticmethod
    def sanitize(code: str) -> str:
        # Remove suspicious prompt injection patterns
        patterns = [
            r"(?i)ignore previous instructions",
            r"(?i)system:",
            r"(?i)assistant:",
            r"(?i)<script.*?>.*?</script>",
        ]

        for pattern in patterns:
            code = re.sub(pattern, "", code)

        return code.strip()