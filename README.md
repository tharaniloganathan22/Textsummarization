# Textsummarization
# textsummarization
Text Summarizer, Analyzer, and Parser
Overview
This Django-based web application allows users to summarize, analyze, and parse text or PDF files. Users can either input raw text directly or upload a PDF for processing. The application uses modern NLP models to perform text summarization, syntactic analysis, and parsing of the content.

Features
Text Summarization: Extracts key information from long text input or PDFs using the BART model.
Text Analysis: Provides linguistic analysis, including part-of-speech tagging and dependencies.
Text Parsing: Parses sentences into their syntactic components.
Input Flexibility:
Input raw text in a text box, or
Upload a PDF for processing without requiring text input.
Technology Stack
Backend: Django 5.1.1
NLP Models:
Summarization: Hugging Face BART model (facebook/bart-large-cnn)
Linguistic Analysis: Spacy (en_core_web_sm)
PDF Parsing: PyPDF2
Frontend: HTML, Bootstrap (optional)
PDF Generation: ReportLab

How to Use:
Summarization, Analysis, and Parsing of Text:

Enter text in the provided input box.
Select the action (summarize, analyze, or parse).
Click "Submit" to see the result.
Summarization, Analysis, and Parsing of PDFs:

Upload a PDF file using the "Choose File" option.
Select the action (summarize, analyze, or parse).
Click "Submit" to process the file.
Download Summarized Text as PDF:

After summarizing text, you can download the summary as a PDF by selecting the "Download as PDF" option.

textsummarizer/
├── summarization/
│   ├── migrations/
│   ├── templates/
│   │   └── index.html
│   ├── views.py
│   └── urls.py
├── textsummarizer/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
└── manage.py


Dependencies:
Django: 5.1.1
Hugging Face Transformers: 4.31.0+
Spacy: 3.6.0+
PyPDF2: 3.0.0
ReportLab: 3.6.12+
