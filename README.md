# PDFtoPrompt

[![PyPI version](https://badge.fury.io/py/pdftoprompt.svg)](https://badge.fury.io/py/pdftoprompt)

Existing libraries for using GPT-4 to extract information from a PDF fil typically combine GPT-4 with word searching, indexing, and segmentation. Those strategies work reasonably, but they have one significant limitation: they deprive the LLM of "big picture" context.

PDFtoPrompt takes a different strategy. Inspired by Twitter user [@gfodor](https://twitter.com/gfodor)'s experiments with [text compression](https://twitter.com/gfodor/status/1643415357615640577), it uses GPT-4 to compress or distill a PDF file's entire informational content to below the length limit of a single ChatGPT prompt. 

It achieves this by first calculating what compression factor is needed to get the text to the right length, then segmenting the PDF file and asking GPT-4 to compress each segment, and finally stitching the compressed segments back together. You should then be able to fit the full compressed text into a single ChatGPT prompt, with some room left over to ask a question.

The process is, as Twitter user @gfodor notes, pretty "lossy." especially for longer texts. This tool may be best used in combination with others that use other strategies.

## Installation

1. Install with pip:

```bash
pip install pdftoprompt
```

## Usage

Make sure to first set your GPT-4-approved OpenAI API key with the set_openai_api_key function:


```python
from pdftoprompt import set_openai_api_key

set_openai_api_key()
```

This function either takes your API key as a string argument or looks in the .env file in the current working directory to see if you have an OPENAI_API_KEY variable stored there. I recommend saving your API key in the .env file for your project so you can share your code without worrying about key security. If you're uploading code to GitHub, make sure to add .env to .gitignore.

Next, import the `compress_pdf` function from the `pdf_compressor` library, and call it with the PDF url or file path:


```python
from pdf_compressor import compress_pdf

file_path = "path/to/your/pdf/file.pdf"
use_ocr = True  # Set to True if you want to use OCR

compressed_text = compress_pdf(file_path, use_ocr)
print(compressed_text)
```


In theory you should be able to use OCR and an optional `use_ocr` argument (default is `False`)

2. 

Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and add it to your system path.

3. Set an environment variable `GPT_API_KEY` with your OpenAI API key.

## Usage

## Contributing

If you'd like to contribute to this library, please submit a pull request on GitHub. We welcome any improvements, bug fixes, or new features.

## License

This library is released under the [MIT License](https://opensource.org/licenses/MIT).
