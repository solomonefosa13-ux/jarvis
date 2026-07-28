# Jarvis

Jarvis is a lightweight local desktop assistant for Linux. It can greet you, answer simple questions, open websites, launch common apps, and open a terminal. It is designed as a foundation for deeper laptop automation and can be extended with voice control and task automation.

## Features

- Text and optional voice interaction
- Opens websites like YouTube, Google, and GitHub
- Launches common apps such as VS Code, Firefox, and the terminal
- Answers simple questions about the time and date

## Quick start

```bash
cd /workspaces/jarvis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 jarvis.py
```

To try voice mode when the required packages are installed:

```bash
python3 jarvis.py --voice
```
