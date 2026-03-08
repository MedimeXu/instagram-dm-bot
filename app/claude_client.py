import subprocess

class ClaudeClient:
    def __init__(self, mode="cli", api_key=None):
        self.mode = mode
        self.api_key = api_key

    def generate_response(self, system_prompt, user_message):
        if self.mode == "cli":
            return self._call_cli(system_prompt, user_message)
        else:
            return self._call_api(system_prompt, user_message)

    def _call_cli(self, system_prompt, user_message):
        full_prompt = f"{system_prompt}\n\n{user_message}"
        result = subprocess.run(
            ["claude", "-p", full_prompt, "--no-input"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode != 0:
            raise RuntimeError(f"Claude CLI error: {result.stderr}")
        return result.stdout.strip()

    def _call_api(self, system_prompt, user_message):
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        return message.content[0].text.strip()

    def parse_bubbles(self, response):
        bubbles = [b.strip() for b in response.split("---") if b.strip()]
        return bubbles
