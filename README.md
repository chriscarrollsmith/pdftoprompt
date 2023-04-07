# PDFtoPrompt

[![PyPI version](https://badge.fury.io/py/pdftoprompt.svg)](https://badge.fury.io/py/pdftoprompt)

Existing libraries for using GPT-4 to extract information from a PDF fil typically combine GPT-4 with word searching, indexing, and segmentation. Those strategies work reasonably, but they have one significant limitation: they deprive the LLM of "big picture" context.

PDFtoPrompt takes a different strategy. Inspired by Twitter user [@gfodor](https://twitter.com/gfodor)'s experiments with [text compression](https://twitter.com/gfodor/status/1643415357615640577), it uses GPT-4 to compress or distill a PDF file's entire informational content to below the length limit of a single ChatGPT prompt. 

It achieves this by first calculating what compression factor is needed to get the text to the right length, then segmenting the PDF file and asking GPT-4 to compress each segment, and finally stitching the compressed segments back together. You should then be able to fit the full compressed text into a single ChatGPT prompt, with some room left over to ask a question.

The process is, as @gfodor notes, pretty "lossy," especially for longer texts. This tool may be best used in combination with others built on other strategies.

## Installation

1. Install with pip:

```bash
pip install pdftoprompt
```

## Usage

### Setting your API Key

Make sure to first set your GPT-4-approved OpenAI API key with the set_openai_api_key function:


```python
from pdftoprompt import set_openai_api_key

set_openai_api_key()
```

This function either takes your API key as a string argument or looks in the .env file in the current working directory to see if you have an OPENAI_API_KEY variable stored there. I recommend saving your API key in the .env file for your project so you can share your code without worrying about key security. If you're uploading code to GitHub, make sure to add .env to .gitignore.

### Compressing a PDF to an LLM Prompt

Next, import the `compress_pdf` function from the `pdftoprompt` library, and call it with the PDF url or file path:


```python
from pdftoprompt import compress_pdf

file_path = "https://arxiv.org/pdf/2203.06566.pdf"

compressed_text = compress_pdf(file_path)
print(compressed_text)
```


The above code distills an academic paper titled ["PromptChainer: Chaining Large Language Model Prompts through Visual Programming"](https://arxiv.org/pdf/2203.06566.pdf) down to the following GPT-interpretable prompt:

<blockquote>
PromptChainer: Chaining LLM Prompts via Visual Programming by Tongshuang Wu, Ellen Jiang, Aaron Donsbach, Jeff Gray, Alejandra Molina, Michael Terry, and Carrie J.Cai explores LLM chain authoring. Pilot studies show users need support transforming data between steps and debugging chains. PromptChainer is designed to address these needs, providing an interactive interface for visually programming chains. Case studies with four designers and developers demonstrate its ability to support building prototypes for various applications. Open questions remain on scaling chains to more complex tasks and supporting low-fi chain prototyping.3.2 Interface Design
Designing the interface in Figure 1 addresses challenges with Chain View (Figure 1A) for chain structure authoring, Node View (Figure 1B) for single step authoring, and chain debugging support. Chain View is a visual panel for building and viewing chains, with nodes representing steps and edges denoting connections. Node visualization (Figure 4) includes named inputs/outputs, status icons, and data views. Node types (Figure 3) cover diverse user needs, including Generic LLM nodes, LLM Classifier nodes, helper nodes, and communication nodes. Example gallery helps users develop mental models and prompting patterns.

Node View enables node inspection, implementation, testing, and automatic input name parsing based on LLM prompts or JavaScript function signatures. Global chain consistency is ensured by automatically updating input handles when prompt templates change. Interactive debugging functionalities address cascading error challenges and enable unit testing, end-to-end assessments, and breakpoint debugging.

4 USER FEEDBACK SESSIONS
Preliminary study aimed to understand users' desired chains, PromptChainer support, and challenges faced. Users proposed diverse tasks, some with branching logic and others with iterative content. Chaining patterns included parallel logic branches and incremental iterations on content. Chaining rationales included addressing LLM limitations and making prototypes more generalizable. PromptChainer supported various chain construction strategies and multi-level debugging. Participants used predefined helper nodes more than customized JS nodes.Q: Remaining challenges in chain authoring?
A: 1. Ensuring coherence in interdependent sub-tasks; 2. Tracking chains with complex logic.

Challenges include maintaining coherence in chains with interdependent parallel tasks and tracking complex decomposition. P4's story writing chain generated a paragraph for each outline point, resulting in a final essay lacking coherence. One user created an input node to manually track previous outputs. Future work could investigate methods considering inter-dependency between parallel sub-tasks and enhancing PromptChainer's tracing capabilities. Customized chain grouping and execution visualizations may help address these issues.

Study limitations: Participants may have felt invested in their pre-created prompts, making them less inclined to consider other chain structures. Prior prototyping work suggests concurrent consideration of multiple alternatives can lead to better outcomes. Future work could explore low-fi prototyping of multiple chains and task decomposition strategies for larger, more complex tasks. Encouraging users to create "half-baked" chain constructions without investing too much time in prompting upfront may also be beneficial.
</blockquote>

Note that when we ask GPT to compress the text, we specifically instruct it that the text doesn't have to be human-readable. The goal here isn't to get a shortened version that works for humans. It's to get a shortened version that works as a Large Language Model prompt.

### OCR

In theory, you should be able to use OCR by setting the `compress_pdf` function's `use_ocr` argument to True, but that functionality requires that you install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and add it to your system path, and I can't vouch for this functionality because I haven't tested it yet.

## Contributing

If you'd like to contribute to this library, please submit a pull request on GitHub.

## License

This library is released under the [MIT License](https://opensource.org/licenses/MIT).
