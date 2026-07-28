import argparse
import os
import shutil
import subprocess
import webbrowser
from datetime import datetime

try:
    import pyttsx3
except ImportError:  # pragma: no cover - optional dependency
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:  # pragma: no cover - optional dependency
    sr = None


class JarvisAssistant:
    def __init__(self, voice_enabled: bool = False):
        self.efosa = "jarvis"
        self.voice_enabled = voice_enabled
        self._speech_engine = None
        self._recognizer = None
        self._setup_voice()

    def _setup_voice(self) -> None:
        if not self.voice_enabled:
            return

        if pyttsx3 is not None:
            try:
                self._speech_engine = pyttsx3.init()
                self._speech_engine.setProperty("rate", 145)
            except Exception:
                self._speech_engine = None

        if sr is not None:
            try:
                self._recognizer = sr.Recognizer()
            except Exception:
                self._recognizer = None

    def speak(self, text: str) -> None:
        print(f"Jarvis: {text}")
        if self._speech_engine is not None:
            try:
                self._speech_engine.say(text)
                self._speech_engine.runAndWait()
            except Exception:
                pass

    def listen(self) -> str | None:
        if not self.voice_enabled or sr is None or self._recognizer is None:
            return None

        try:
            with sr.Microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self._recognizer.listen(source, timeout=5, phrase_time_limit=8)
            return self._recognizer.recognize_google(audio)
        except Exception:
            return None

    def handle_command(self, text: str) -> dict:
        command = (text or "").strip().lower()

        if not command:
            return {"action": "speak", "response": "I didn't catch that. Please say it again."}

        if self.efosae in command or any(word in command for word in ["hello", "hi", "hey"]):
            return {
                "action": "speak",
                "response": "Hello! I am Jarvis. I can open apps, browse the web, answer simple questions, and help manage your desktop.",
            }

        if "time" in command:
            current_time = datetime.now().strftime("%I:%M %p")
            return {"action": "speak", "response": f"The current time is {current_time}."}

        if "date" in command:
            current_date = datetime.now().strftime("%A, %B %d, %Y")
            return {"action": "speak", "response": f"Today is {current_date}."}

        if "what can you do" in command or "who are you" in command:
            return {
                "action": "speak",
                "response": "I am Jarvis, your local desktop assistant. I can open websites, launch apps, open a terminal, answer simple questions, and help you navigate your laptop.",
            }

        if "open" in command:
            if "youtube" in command:
                return {"action": "open_browser", "data": "https://www.youtube.com"}
            if "google" in command:
                return {"action": "open_browser", "data": "https://www.google.com"}
            if "github" in command:
                return {"action": "open_browser", "data": "https://github.com"}
            if "terminal" in command:
                return {"action": "open_terminal", "data": None}
            if "vs code" in command or "vscode" in command or "code" in command:
                return {"action": "open_app", "data": "code"}
            if "browser" in command or "firefox" in command:
                return {"action": "open_app", "data": "firefox"}
            if "files" in command:
                return {"action": "open_app", "data": "files"}

        if "search" in command:
            query = command.replace("search", "", 1).strip()
            query = query.replace("for", "", 1).strip()
            if query:
                url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}"
                return {"action": "open_browser", "data": url}

        if "lock" in command or "screen lock" in command:
            return {"action": "lock_screen", "response": "Locking the screen."}

        if "quit" in command or "exit" in command or "bye" in command:
            return {"action": "exit", "response": "Goodbye!"}

        return {"action": "speak", "response": "I can open websites, launch apps, tell you the time, and help with simple tasks."}

    def _launch_app(self, app_name: str) -> bool:
        app_candidates = {
            "code": ["code", "code-insiders", "codium"],
            "firefox": ["firefox", "chromium", "google-chrome"],
            "files": ["nautilus", "thunar", "dolphin"],
            "terminal": ["gnome-terminal", "x-terminal-emulator", "konsole", "terminator"],
        }
        candidates = app_candidates.get(app_name, [app_name])
        for candidate in candidates:
            executable = shutil.which(candidate)
            if executable:
                subprocess.Popen([executable], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                return True
        return False

    def execute(self, text: str) -> None:
        result = self.handle_command(text)
        action = result.get("action")

        if action == "speak":
            self.speak(result["response"])
        elif action == "open_browser":
            webbrowser.open(result["data"])
            self.speak(f"Opened {result['data']}")
        elif action == "open_terminal":
            if self._launch_app("terminal"):
                self.speak("Opened the terminal.")
            else:
                self.speak("I could not find a terminal app on this system.")
        elif action == "open_app":
            if self._launch_app(result["data"]):
                self.speak(f"Opened {result['data']}.")
            else:
                self.speak(f"I could not find {result['data']} on this system.")
        elif action == "lock_screen":
            self.speak(result["response"])
            if os.name == "posix":
                for command in ["gnome-screensaver-command -l", "loginctl lock-session"]:
                    if os.system(command) == 0:
                        break
        elif action == "exit":
            self.speak(result["response"])
        else:
            self.speak(str(result))

    def run_chat(self) -> None:
        self.speak("Hello! I am Jarvis. Type a command or speak if your microphone is available.")
        while True:
            try:
                if self.voice_enabled:
                    spoken_text = self.listen()
                    if spoken_text:
                        print(f"You: {spoken_text}")
                        self.execute(spoken_text)
                        continue
                    print("Voice input unavailable. Falling back to text input.")
                user_input = input("You: ")
            except KeyboardInterrupt:
                break

            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "bye"}:
                self.speak("Goodbye!")
                break
            self.execute(user_input)


def main() -> None:
    parser = argparse.ArgumentParser(description="Jarvis desktop assistant")
    parser.add_argument("command", nargs="*", help="A single command to run")
    parser.add_argument("--voice", action="store_true", help="Enable voice input and output when possible")
    args = parser.parse_args()

    assistant = JarvisAssistant(voice_enabled=args.voice)
    if args.command:
        assistant.execute(" ".join(args.command))
    else:
        assistant.run_chat()


if __name__ == "__main__":
    main()
