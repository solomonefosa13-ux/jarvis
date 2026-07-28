from jarvis import JarvisAssistant


def test_greeting_response():
    assistant = JarvisAssistant()
    result = assistant.handle_command("hello jarvis")

    assert result["action"] == "speak"
    assert "hello" in result["response"].lower()


def test_time_response_contains_time():
    assistant = JarvisAssistant()
    result = assistant.handle_command("what time is it")

    assert result["action"] == "speak"
    assert "time" in result["response"].lower()


def test_open_browser_command_builds_url():
    assistant = JarvisAssistant()
    result = assistant.handle_command("open youtube")

    assert result["action"] == "open_browser"
    assert result["data"] == "https://www.youtube.com"
