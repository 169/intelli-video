from string import Template

translate_prompt = """Translate to $other_language language strictly line by line. return json data

Input: Hello, my name is John.
I'm from the United States.
Output: {"Hello, my name is John.": "你好，我的名字叫约翰.", "I'm from the United States.": "我来自美国."}
Input: ${content}
Output: 
"""


def render_translate_prompt(content: str, other_language: str) -> str:
    return Template(translate_prompt).substitute(
        content=content, other_language=other_language
    )
