# The-Clean-Code-Bot

# 🧠 Code Refactoring CLI Tool

A Python-based command-line interface (CLI) tool that takes poorly structured or "dirty" source code and transforms it into clean, maintainable, and well-documented code following SOLID principles.

The tool uses a large language model to refactor code while preserving functionality and automatically adds structured documentation such as docstrings.

---

## ⚙️ Design Approach

The system is built using a modular pipeline architecture with clear separation of concerns:

- **CLI Layer**
  - Handles user input and file paths

- **Validation & Sanitization Layer**
  - Ensures safe processing of input code
  - Reduces risks from malformed or malicious input

- **Processing Engine**
  - Orchestrates LLM-based code refactoring
  - Applies structured transformation instructions

- **Output Formatting Layer**
  - Cleans and standardizes model output
  - Ensures production-ready formatting

This pipeline-based structure improves maintainability, extensibility, and clarity of the system.

---

## 🔐 Security Considerations

The tool includes basic safeguards for handling untrusted input:

- File size validation
- Simple prompt injection filtering
- Strict separation between code content and model instructions

---

## 🤖 AI-Assisted Refactoring

The system uses a large language model to:

- Refactor code using SOLID principles
- Improve readability and structure
- Add comprehensive documentation (docstrings)
- Preserve original functionality

---

## 🎯 Project Goals

- Automate cleanup of legacy or undocumented code
- Improve code quality and maintainability
- Demonstrate secure integration of LLMs into developer tools
- Provide a lightweight and extensible CLI framework

---

## 🚀 Future Improvements

- AST-based parsing for deeper code understanding
- Multi-language support (Python, JavaScript, etc.)
- Batch processing with progress tracking
- Plugin system for custom refactoring rules
- Diff output view (before vs after)

---