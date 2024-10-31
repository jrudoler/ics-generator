# ics-generator
Use structured generation via [outlines](https://dottxt-ai.github.io/outlines/) to create .ics files based on text descriptions / emails.

*Note: Currently only supports CLI, with manual text input (or copy/paste)*

Just a side project for me so not providing multi-OS support. I'm working on an Apple Silicon-based Mac. Requires an OpenAI API key but easily customizable to work with different models.

### Installation
Recommended installation with [poetry](https://python-poetry.org):
1. Clone this repo
2. Install poetry following [these instructions](https://python-poetry.org/docs/#installation).
3. In the repo's root directory, run `poetry install`
4. Add the "event" command to your path: 
```
echo "export PATH=$PATH:<path-to-repo>/cli/" >> ~/.zshrc
```
5. If using an OpenAI model (default) Define your OpenAI API key (OPENAI_API_KEY) as an environment variable: 
```
echo "export OPENAI_API_KEY=<your-key-here>" >> ~/.zshrc
```
6. Run `source ~/.zshrc` 

### Usage
On the command line, run
`event "<text describing event>"`
The program will generate a corresponding .ics file and open it using your default calendar app.

### Example
https://github.com/user-attachments/assets/6ec24fce-5233-4efa-9299-b5720301576a



