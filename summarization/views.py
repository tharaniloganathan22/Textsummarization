from django.shortcuts import render
from transformers import pipeline
import spacy
import PyPDF2
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Load models
summarizer_en = pipeline("summarization", model="facebook/bart-large-cnn")
nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_file):
    """Extract text from the uploaded PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text.strip()  # Remove leading/trailing whitespace


def create_pdf(summary):
    """Create a PDF containing only the summary."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.drawString(100, height - 50, "Summarized Text")

    # Function to draw wrapped text
    def draw_wrapped_text(text, x, y, max_width):
        for line in text.splitlines():
            words = line.split(' ')
            current_line = ''
            for word in words:
                # Check if adding this word would exceed the max width
                if p.stringWidth(current_line + word, 'Helvetica', 12) < max_width:
                    current_line += word + ' '
                else:
                    p.drawString(x, y, current_line)
                    y -= 15  # Move down for the next line
                    current_line = word + ' '
            # Draw any remaining text
            if current_line:
                p.drawString(x, y, current_line)
                y -= 15  # Move down for the next line
        return y  # Return the new y position

    # Summary
    y = height - 100
    p.drawString(100, y, "Summary:")
    y -= 20
    draw_wrapped_text(summary, 100, y, width - 200)

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def parse_sentence(text):
    """Parse the input sentence and return parse trees."""
    doc = nlp(text)
    parse_trees = []
    for sentence in doc.sents:
        parse_tree = f"Sentence: {sentence.text}"
        for token in sentence:
            parse_tree += f"\n - {token.text} ({token.dep_})"
        parse_trees.append(parse_tree)
    return parse_trees

def home(request):
    summary = ""
    analysis = []
    parse_trees = []

    if request.method == "POST":
        text = request.POST.get('text')
        action = request.POST.get('action')
        pdf_file = request.FILES.get('pdf_file')

        if pdf_file:
            text = extract_text_from_pdf(pdf_file)

        if action == "summarize" and text:
            summary = summarizer_en(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

            # Check if user wants to download the summary as a PDF
            if request.POST.get('download_pdf') == 'on':
                pdf_buffer = create_pdf(summary)  # Only pass the summary
                response = HttpResponse(pdf_buffer, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="summary.pdf"'
                return response

        elif action == "analyze" and text:
            doc = nlp(text)
            analysis = [(token.text, token.lemma_, token.pos_, token.dep_) for token in doc]

        elif action == "parse" and text:
            parse_trees = parse_sentence(text)  # Ensure this function is defined

    return render(request, 'index.html', {'summary': summary, 'analysis': analysis, 'parse_trees': parse_trees})
