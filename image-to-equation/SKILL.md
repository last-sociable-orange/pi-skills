---
name: image-to-equation
description: "Use this skill whenever the user provides images of mathematical equations or expressions and wants them transcribed into LaTeX and inserted into a markdown file. Triggers include: any mention of 'OCR this equation', 'convert this math image to LaTeX', 'transcribe this formula', 'equation from image', 'math OCR', or requests to process images containing mathematical notation (calculus, algebra, matrices, integrals, sums, fractions, Greek letters, etc.) from a markdown file. Also use when the user says 'extract the equations from these images' or 'put LaTeX after the images in my markdown'. This skill handles one image at a time and only uses the model's built-in vision capability — no external OCR tools or libraries. Do NOT use for general OCR (handwriting to text, document scanning), or for generating LaTeX from text descriptions."
---

# Image to LaTeX Equation

## Overview

This skill converts mathematical equations displayed in images into LaTeX notation and inserts the LaTeX code into a markdown file immediately after the corresponding image reference. It relies entirely on your built-in vision capability — no external OCR tools, third-party libraries, or software packages are used.

## How It Works

The process is entirely visual and manual (one image at a time):

1. You look at each image using the `read` tool (which sends the image to you as an attachment)
2. You visually transcribe the mathematical notation into correct LaTeX
3. You insert the LaTeX code into the markdown file after the image reference

## Workflow

### Step 1: Check Your Capability

Before proceeding, verify that you can receive and process image input. You can do this by checking:
- The `read` tool description — it states it supports image file types (jpg, png, gif, webp) and sends images as attachments
- The model you're running on supports vision/ multimodal inputs

If you cannot receive images, inform the user and abort. No processing can happen without this capability.

### Step 2: Assess the Scope

Look at the markdown file the user provided. Count how many images (e.g., `![](...)` references or `<img>` tags) contain equations that need processing.

**If the count exceeds 50 images**, ask the user to confirm before proceeding. Explain that this is a manual, one-at-a-time process requiring your visual attention for each image.

### Step 3: Process One Image at a Time (No Batch Processing)

**Important: Do not write or run any script to batch-process images.** Each image must be handled individually because you need to visually inspect it with your own vision capability.

For each image:

1. **Read the image** using the `read` tool with its path.
2. **Visually examine the image** to understand the mathematical expression(s) it contains.
3. **Transcribe the equation into LaTeX** using your knowledge of LaTeX math syntax. Be precise:
   - Use `\frac{}{}` for fractions
   - Use `\sum`, `\int`, `\prod` for sums, integrals, products
   - Use `\sqrt{}` or `\sqrt[]{}` for roots
   - Use `\begin{pmatrix}` etc. for matrices
   - Use `\lim`, `\to`, `\infty` for limits
   - Use proper braces `{}` for grouping
   - Preserve exact variable names (Greek letters like \alpha, \beta, \theta, \pi)
   - Preserve superscripts `^` and subscripts `_` correctly
   - Use `\cdot` or `\times` for multiplication as shown
   - Use `\Rightarrow`, `\rightarrow`, `\mapsto` for arrows as shown
   - Wrap inline equations in `$...$` and display equations in `$$...$$` based on how they appear in the image
4. **Insert the LaTeX** into the markdown file:
   - Find the image reference in the markdown file
   - Insert the LaTeX code immediately after it on a new line
   - Use a clear format: a blank line, then the LaTeX, then a blank line before the next content

**Format for insertion:**

```markdown
![equation description](path/to/image.png)

$$
E = mc^2
$$

Next content...
```

### Step 4: Repeat

Move to the next image and repeat Step 3. Do not skip images or process them out of order. Process them in the order they appear in the markdown file.

## Quality Guidelines

- **Accuracy over speed**: Take your time to read each equation carefully. Mathematical notation can be subtle — a misplaced bracket or missing subscript changes the meaning.
- **Preserve structure**: If the image contains multiple equations (e.g., a system of equations), use `\begin{cases}` or multiple `$$...$$` blocks as appropriate.
- **Check for alignment**: If equations have alignment (e.g., `=` signs stacked vertically), use `\begin{aligned}` inside `$$...$$`.
- **Notify the user** if an image is too blurry, low-resolution, or otherwise unreadable. Do not guess incorrectly — state that you cannot reliably read the equation.
- **Verify after insertion**: After inserting LaTeX, quickly re-read the surrounding markdown to ensure the insertion is correct and hasn't broken the file structure.
