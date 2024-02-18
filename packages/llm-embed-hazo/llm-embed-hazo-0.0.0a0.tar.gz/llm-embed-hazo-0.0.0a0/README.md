# llm-embed-hazo

[![PyPI](https://img.shields.io/pypi/v/llm-embed-hazo.svg)](https://pypi.org/project/llm-embed-hazo/)
[![Changelog](https://img.shields.io/github/v/release/Florents-Tselai/llm-embed-hazo?include_prereleases&label=changelog)](https://github.com/Florents-Tselai/llm-embed-hazo/releases)
[![Tests](https://github.com/Florents-Tselai/llm-embed-hazo/workflows/Test/badge.svg)](https://github.com/Florents-Tselai/llm-embed-hazo/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/Florents-Tselai/llm-embed-hazo/blob/main/LICENSE)

Dummy `llm` model for demonstration purposes

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

    llm install llm-embed-hazo

## Usage

The models will be downloaded the first time you try to use them.

See [the LLM documentation](https://llm.datasette.io/en/stable/embeddings/index.html) for everything you can do.

To get started embedding a single string, run the following:

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-embed-hazo
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
pytest
```
