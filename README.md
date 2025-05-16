# Sprite2GIF

A tool to convert sprites into animated GIFs with a user-friendly web interface.

## Installation

1. Make sure you have Python 3.8+ installed
2. Clone this repository
3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development

- Source code is located in the `src/` directory
- Tests are in the `tests/` directory
- Use `pytest` to run tests
- Use `black` for code formatting
- Use `flake8` for code quality checks

## Running the Application

To start the Streamlit web interface:

```bash
streamlit run src/app.py
```

This will launch a local web server where you can:

- Upload sprite sheets
- Configure animation settings
- Preview and download the generated GIFs

## Features

- Convert sprite sheets to animated GIFs
- Interactive web interface using Streamlit
- Customizable animation settings
- Preview functionality
- Direct download of generated GIFs
