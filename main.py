from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

text_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

markdown_text = """
# Introduction

This is the introduction.

## Python

Python is a programming language.

### Django

Django is a Python web framework.
"""

docs = text_splitter.split_text(markdown_text)

for doc in docs:
    print("TEXT:", doc.page_content)
    print("METADATA:", doc.metadata)
    print("---")