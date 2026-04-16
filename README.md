# The-Clean-Code-Bot

🧠 Code Refactoring CLI Tool

This project is a Python-based command-line interface (CLI) tool that takes poorly structured or “dirty” source code and transforms it into clean, maintainable, and well-documented code following SOLID principles.

The tool leverages a large language model to analyze and refactor code while preserving original functionality, and it automatically adds structured documentation such as docstrings.

⚙️ Design Approach

The system was built using a modular pipeline architecture that separates concerns into distinct stages:

Input handling (CLI layer) – manages user input and file paths
Validation & sanitization layer – ensures safe processing of input code and mitigates prompt injection risks
Processing engine – orchestrates transformation of code using an LLM-based refactoring step
Output formatting layer – cleans and standardizes model output for production-ready code

This staged pipeline design ensures maintainability, extensibility, and clear separation of responsibilities.

🔐 Security Considerations

To reduce risks associated with executing or processing untrusted input, the system includes:

Input size validation
Basic prompt injection filtering
Strict separation between code data and model instructions
🤖 AI-Assisted Refactoring

The tool uses an LLM (via API) to:

Refactor code according to SOLID principles
Improve readability and structure
Add comprehensive documentation
Preserve original functionality
📦 Goals
Automate code cleanup for legacy or undocumented projects
Enforce clean architecture principles
Demonstrate secure integration of LLMs in developer tooling
Provide a lightweight extensible CLI framework for future enhancements
🚀 Future Improvements
AST-based code parsing for more precise refactoring
Multi-language support
Batch processing with progress tracking
Plugin system for custom refactoring rules