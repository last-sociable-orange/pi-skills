---
name: pymupdf
description: "Use this skill for PDF manipulation tasks using PyMuPDF (fitz). Handles opening/saving documents, text extraction (txt only, no markdown), merging/splitting PDFs, adding watermarks/images, rotating/cropping pages, encryption, redaction, and converting pages to images."
---

# PyMuPDF Skill

PyMuPDF (also known as `fitz`) is a Python library for PDF manipulation, text extraction (txt only, no markdown), and document processing. It provides fast and comprehensive functionality for working with PDF and other document formats.

**DO NOT**: use it to translate pdf to MarkDown.

## Installation

```bash
pip install pymupdf
```

## Basic Usage

### Importing

```python
import pymupdf
# or the legacy alias
import fitz  # still works for backward compatibility
```

### Opening a Document

```python
# Open from file
doc = pymupdf.open("document.pdf")

# Open from memory data
with open("document.pdf", "rb") as f:
    data = f.read()
doc = pymupdf.open(stream=data, filetype="pdf")

# Create new empty PDF
doc = pymupdf.open()
```

### Document Properties

```python
# Page count
page_count = doc.page_count  # or len(doc)

# Metadata
metadata = doc.metadata  # dict with keys: producer, format, encryption, author, 
                         # modDate, keywords, title, creationDate, creator, subject

# Table of contents (bookmarks)
toc = doc.get_toc()  # returns [[level, title, page], ...]
```

## Working with Pages

### Accessing Pages

```python
# By index (0-based)
page = doc[0]  # or doc.load_page(0)

# Negative indices work too
last_page = doc[-1]

# Iterate over pages
for page in doc:
    # process page

# Iterate with range
for page in doc.pages(start=0, stop=10, step=2):
    # process pages 0, 2, 4, 6, 8
```

### Page Dimensions

```python
# Get page rectangle
rect = page.rect  # full page size
rect = page.bound()  # same as page.rect

# Get crop box
rect = page.cropbox

# Set crop box (crop page)
page.set_cropbox(pymupdf.Rect(100, 100, 400, 400))
```

## Text Extraction

### Extract Text from Page

```python
# Plain text
text = page.get_text("text")

# Text blocks (paragraphs)
blocks = page.get_text("blocks")  # returns list of (x0, y0, x1, y1, text, block_no, block_type)

# Words
words = page.get_text("words")  # returns list of (x0, y0, x1, y1, word, block_no, line_no, word_no)

# HTML with formatting
html = page.get_text("html")

# Dictionary format
dict_data = page.get_text("dict")

# JSON format
json_data = page.get_text("json")

# XHTML
xhtml = page.get_text("xhtml")

# XML with detailed positioning
xml = page.get_text("xml")
```

### Search Text

```python
# Find all occurrences of text
areas = page.search_for("search term")  # returns list of Rect objects

# Search with options
areas = page.search_for("term", hit_max=10)  # limit results
```

### Extract Text from Entire Document

```python
full_text = ""
for page in doc:
    full_text += page.get_text()
```

## Converting Pages to Images

### Basic Page Rendering

```python
# Render page to pixmap (image)
pix = page.get_pixmap()

# Save as PNG
pix.save("page.png")

# Save as other formats
pix.save("page.jpg")
pix.save("page.ppm")
pix.save("page.pam")
```

### Rendering Options

```python
# Higher resolution (DPI)
pix = page.get_pixmap(dpi=300)

# Specific zoom matrix
mat = pymupdf.Matrix(2.0, 2.0)  # 2x zoom
pix = page.get_pixmap(matrix=mat)

# Grayscale
pix = page.get_pixmap(colorspace=pymupdf.csGRAY)

# With transparency (alpha channel)
pix = page.get_pixmap(alpha=True)

# Specific clip region
clip_rect = pymupdf.Rect(100, 100, 400, 400)
pix = page.get_pixmap(clip=clip_rect)

# Rotation
pix = page.get_pixmap(rotation=90)
```

### Matrix Transformations

```python
# Create transformation matrix
mat = pymupdf.Matrix(a, b, c, d, e, f)  # standard matrix notation

# Or use convenience methods
mat = pymupdf.Matrix(2.0, 2.0)  # zoom x and y
mat = pymupdf.Matrix(0)  # identity

# Pre-translate (shift)
mat = pymupdf.Matrix(2, 2).pretranslate(-rect.x0, -rect.y0)

# Pre-rotate
mat = pymupdf.Matrix(2, 2).prerotate(45)
```

## Merging and Combining PDFs

### Merge PDF Files

```python
# Open source documents
doc_a = pymupdf.open("a.pdf")
doc_b = pymupdf.open("b.pdf")

# Merge doc_b into doc_a
doc_a.insert_pdf(doc_b)

# Save result
doc_a.save("merged.pdf")
```

### Merge with Page Range

```python
# Insert specific pages from doc_b into doc_a
doc_a.insert_pdf(doc_b, 
                 from_page=0,      # start page in doc_b (0-based)
                 to_page=5,        # end page in doc_b (inclusive)
                 start_at=-1,      # insert position in doc_a (-1 = end)
                 rotate=-1,        # rotation for inserted pages
                 links=True,       # copy links
                 annots=True,      # copy annotations
                 widgets=True)     # copy form fields
```

### Merge with Other File Types

```python
# Insert non-PDF files (XPS, EPUB, CBZ, etc.)
doc_a = pymupdf.open("a.pdf")
doc_b = pymupdf.open("b.xps")  # or .epub, .cbz, etc.
doc_a.insert_file(doc_b)
doc_a.save("merged.pdf")
```

## Page Manipulation

### Rotate Pages

```python
# Rotate single page
page.set_rotation(90)  # 0, 90, 180, or 270 degrees
```

### Crop Pages

```python
# Set crop box (visible area)
page.set_cropbox(pymupdf.Rect(100, 100, 400, 400))

# Remove crop (restore full page)
page.set_cropbox(page.rect)
```

### Delete Pages

```python
# Delete single page
doc.delete_page(0)  # delete first page

# Delete page range
doc.delete_pages(from_page=9, to_page=14)  # delete pages 10-15
```

### Move Pages

```python
# Move page (source index, destination index)
doc.move_page(1, 0)  # move page 2 to position 1
```

### Copy Pages

```python
# Copy page to end of document
doc.copy_page(0)  # copy first page to end
```

### Select/Reorder Pages

```python
# Keep only specific pages
doc.select([0, 2, 4])  # keep only pages 1, 3, 5

# Reorder pages
doc.select([2, 1, 0])  # reverse first 3 pages

# Duplicate pages
doc.select([0, 0, 0, 1, 1])  # page 1 x3, page 2 x2
```

### Add Blank Pages

```python
# Add blank page at end
page = doc.new_page(-1, width=595, height=842)  # A4 size

# Add at specific position
page = doc.new_page(0, width=612, height=792)  # Letter size at beginning

# Using paper size helper
w, h = pymupdf.paper_size("a4")
page = doc.new_page(width=w, height=h)

# Landscape
w, h = pymupdf.paper_size("letter-l")  # letter landscape
```

### Insert Pages with Text

```python
# Insert page with text
n = doc.insert_page(-1,  # position (-1 = end)
                    text="Hello World",
                    fontsize=12,
                    width=595,
                    height=842,
                    fontname="Helvetica",
                    color=(0, 0, 0))  # RGB
```

## Adding Content to PDFs

### Add Images

```python
# Insert image on page
page.insert_image(rect, filename="image.png")

# Or from pixmap
pix = pymupdf.Pixmap("image.png")
page.insert_image(rect, pixmap=pix)

# Or from bytes
with open("image.png", "rb") as f:
    img_data = f.read()
page.insert_image(rect, stream=img_data)

# Image with transparency (overlay)
page.insert_image(rect, filename="image.png", overlay=True)

# Image behind content
page.insert_image(rect, filename="watermark.png", overlay=False)
```

### Add Watermarks

```python
# Add watermark to all pages
doc = pymupdf.open("document.pdf")
for page in doc:
    page.insert_image(page.bound(), filename="watermark.png", overlay=False)
doc.save("watermarked.pdf")
```

### Add Text

```python
# Simple text insertion
page.insert_text((100, 100),  # point (x, y)
                 "Hello World",
                 fontsize=11,
                 fontname="Helvetica",
                 color=(0, 0, 0))

# With text box
rect = pymupdf.Rect(100, 100, 400, 200)
page.insert_textbox(rect,
                    "Long text that will wrap within the box",
                    fontsize=12,
                    align=pymupdf.TEXT_ALIGN_LEFT)
```

### Add Links

```python
# Add URI link
page.insert_link({
    "from": pymupdf.Rect(100, 100, 200, 150),
    "uri": "https://example.com"
})

# Add internal link (to page)
page.insert_link({
    "from": pymupdf.Rect(100, 100, 200, 150),
    "page": 5,  # target page number
    "to": (100, 100)  # target point on page
})
```

### Add Annotations

```python
# Add text annotation
annot = page.add_text_annot((100, 100), "Comment text")

# Add highlight
annot = page.add_highlight_annot(pymupdf.Rect(100, 100, 200, 120))

# Add underline
annot = page.add_underline_annot(rect)

# Add strikeout
annot = page.add_strikeout_annot(rect)

# Add rectangle
annot = page.add_rect_annot(rect)

# Add circle
annot = page.add_circle_annot(rect)

# Set annotation colors
annot.set_colors(stroke=(1, 0, 0))  # red
annot.update()
```

## Redaction (Secure Content Removal)

### Redact Text

```python
# Search and redact all occurrences
for page in doc:
    instances = page.search_for("sensitive text")
    for inst in instances:
        page.add_redact_annot(inst)
    page.apply_redactions()
doc.save("redacted.pdf")
```

### Redact Area with Options

```python
# Redact with fill color
page.add_redact_annot(rect, fill=(1, 0, 0))  # red fill

# Apply with options
page.apply_redactions(
    images=pymupdf.PDF_REDACT_IMAGE_PIXELS,  # how to handle images
    graphics=1,  # 0=ignore, 1=remove
    text=1       # 0=ignore, 1=remove
)
```

## Encryption and Security

### Check Encryption

```python
# Check if document needs password
if doc.needs_pass:
    # Try to authenticate
    auth_result = doc.authenticate("password")
    # Returns: 0=failed, 1=owner access, 2=user access
```

### Encrypt PDF

```python
# Create encrypted PDF
perm = int(
    pymupdf.PDF_PERM_ACCESSIBILITY |
    pymupdf.PDF_PERM_PRINT |
    pymupdf.PDF_PERM_COPY |
    pymupdf.PDF_PERM_ANNOTATE
)

doc.save("encrypted.pdf",
         encryption=pymupdf.PDF_ENCRYPT_AES_256,
         owner_pw="owner_password",
         user_pw="user_password",
         permissions=perm)
```

### Permission Flags

- `PDF_PERM_PRINT` - print document
- `PDF_PERM_MODIFY` - modify content
- `PDF_PERM_COPY` - copy text/graphics
- `PDF_PERM_ANNOTATE` - add annotations
- `PDF_PERM_ACCESSIBILITY` - accessibility (always use this)

## Saving Documents

### Save Options

```python
# Basic save
doc.save("output.pdf")

# With garbage collection and compression
doc.save("output.pdf", garbage=3, deflate=True)

# Incremental save (faster for small changes)
doc.save("output.pdf", incremental=True)

# Save to memory
pdf_bytes = doc.tobytes(garbage=3, deflate=True)

# Save with linearization (fast web view)
doc.save("output.pdf", linear=True)
```

## Working with Metadata

### Set Metadata

```python
doc.set_metadata({
    "title": "Document Title",
    "author": "Author Name",
    "subject": "Subject",
    "keywords": "keyword1, keyword2",
    "creator": "Application",
    "producer": "PyMuPDF",
    "creationDate": "D:20240101120000",
    "modDate": "D:20240101120000"
})
```

## Extracting Images

### Get Images from Page

```python
# Get list of images on page
image_list = page.get_images(full=True)

# Extract each image
for img_index, img in enumerate(image_list):
    xref = img[0]  # xref number
    base_image = doc.extract_image(xref)
    image_bytes = base_image["image"]
    image_ext = base_image["ext"]  # png, jpeg, etc.
    
    # Save to file
    with open(f"image_{img_index}.{image_ext}", "wb") as f:
        f.write(image_bytes)
```

## Table of Contents (Bookmarks)

### Get TOC

```python
toc = doc.get_toc()
# Returns: [[level, title, page], ...]
```

### Set TOC

```python
toc = [
    [1, "Chapter 1", 1],
    [2, "Section 1.1", 2],
    [2, "Section 1.2", 5],
    [1, "Chapter 2", 10],
]
doc.set_toc(toc)
```

## Advanced: Splitting Pages (Posterize)

```python
# Split each page into 4 parts (2x2)
src = pymupdf.open("test.pdf")
doc = pymupdf.open()

for spage in src:
    r = spage.rect
    d = pymupdf.Rect(spage.cropbox_position, spage.cropbox_position)
    
    # Define 4 rectangles
    r1 = r / 2  # top left
    r2 = r1 + (r1.width, 0, r1.width, 0)  # top right
    r3 = r1 + (0, r1.height, 0, r1.height)  # bottom left
    r4 = pymupdf.Rect(r1.br, r.br)  # bottom right
    
    for rx in [r1, r2, r3, r4]:
        rx += d
        page = doc.new_page(-1, width=rx.width, height=rx.height)
        page.show_pdf_page(page.rect, src, spage.number, clip=rx)

doc.save("poster.pdf", garbage=3, deflate=True)
```

## Advanced: N-up Pages

```python
# Combine 4 pages into 1 (4-up)
src = pymupdf.open("test.pdf")
doc = pymupdf.open()

width, height = pymupdf.paper_size("a4")
r = pymupdf.Rect(0, 0, width, height)

# Define 4 rectangles per page
r1 = r / 2
r2 = r1 + (r1.width, 0, r1.width, 0)
r3 = r1 + (0, r1.height, 0, r1.height)
r4 = pymupdf.Rect(r1.br, r.br)
r_tab = [r1, r2, r3, r4]

for spage in src:
    if spage.number % 4 == 0:
        page = doc.new_page(-1, width=width, height=height)
    page.show_pdf_page(r_tab[spage.number % 4], src, spage.number)

doc.save("4up.pdf", garbage=3, deflate=True)
```

## Common Patterns

### Convert PDF to Images

```python
doc = pymupdf.open("input.pdf")
for page_num in range(len(doc)):
    page = doc[page_num]
    pix = page.get_pixmap(dpi=200)
    pix.save(f"page_{page_num + 1:03d}.png")
doc.close()
```

### Extract All Text to File

```python
doc = pymupdf.open("input.pdf")
with open("output.txt", "w", encoding="utf-8") as f:
    for page in doc:
        f.write(page.get_text())
doc.close()
```

### Add Page Numbers

```python
doc = pymupdf.open("input.pdf")
for page in doc:
    page.insert_text(
        (page.rect.width / 2, page.rect.height - 30),
        str(page.number + 1),
        fontsize=10,
        color=(0, 0, 0)
    )
doc.save("numbered.pdf")
```

### Merge Multiple PDFs

```python
import os

result = pymupdf.open()
for file in sorted(os.listdir("pdfs")):
    if file.endswith(".pdf"):
        with pymupdf.open(os.path.join("pdfs", file)) as doc:
            result.insert_pdf(doc)
result.save("combined.pdf")
```

## Key Classes and Objects

- **Document** - The PDF document object
- **Page** - Individual page within a document
- **Rect** - Rectangle (x0, y0, x1, y1) for positioning
- **Point** - Point (x, y) for positioning
- **Matrix** - Transformation matrix for scaling/rotation
- **Pixmap** - Raster image representation
- **Annot** - Annotation object
- **Link** - Hyperlink object

## Best Practices

1. **Always close documents** when done to free resources
2. **Use context managers** when possible: `with pymupdf.open("file.pdf") as doc:`
3. **Reuse image data** for watermarks to save memory
4. **Use incremental saves** for small changes to large files
5. **Enable garbage collection** (`garbage=3`) when saving to optimize file size
6. **Use deflate compression** to reduce file size
7. **Render at 2x resolution** and downscale for better image quality

## Resources

- Documentation: https://pymupdf.readthedocs.io/
- GitHub: https://github.com/pymupdf/PyMuPDF
- Examples: https://github.com/pymupdf/PyMuPDF-Utilities
