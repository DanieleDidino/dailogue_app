<h1 align="center">Dailogy App</h1>

<p align="center">A System for Detecting and Improving Dysfunctional Language</p>

Thank you for your interest in our project. Please note that this is still a prototype and may contain bugs or unfinished features.

This repository is part of Dailogy, a project aimed at developing tools to detect dysfunctional and toxic language in chat conversations and provide suggestions to make the language more respectful and inclusive.

## Table of Contents

- [Objective](#objective)
- [Large Language Models](#large-language-models)
- [App Architecture](#app-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)

## Objective

This repository includes an app developed to transform dysfunctional and toxic language into more respectful and inclusive language.
Currently, our focus is particularly on interactions between couples or ex-couples who need to communicate regularly.
Our goal is to develop tools for detecting and mitigating such language, thereby promoting more respectful and inclusive conversations.

## Large Language Models

To transform text into functional and respectful language, we employ `gpt-3.5-turbo`, a Large Language Model (LLM) accessed through the OpenAI API.

## App Architecture

*COMING SOON*

## Installation

#### Python version: 3.10.12 

#### 1. Clone the repository

```bash
git clone https://github.com/DanieleDidino/dailogue_app.git
```

#### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

#### 3. Activate the virtual environment and install dependencies

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

#### 4. Run the API locally
   
```bash
uvicorn main:app --reload
```

Uvicorn should be running on `http://127.0.0.1:8000`

#### 5. Test the app

```bash
pytest -vvv
```

This runs the tests with a higher verbosity level (`-vvv`).

#### 6. Deactivate the virtual environment

```bash
deactivate
```

## Usage

This code is the backend for an app aimed at detecting and mitigating toxic language, thus improving online communication tools.

## Contributing

We welcome contributions to this project! If you have suggestions for improvements or have found a bug, please feel free to contact us.

## Contact

For questions or further information, please contact [Daniele Didino](https://www.linkedin.com/in/daniele-didino).
