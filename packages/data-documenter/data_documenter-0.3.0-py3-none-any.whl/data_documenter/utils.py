import re

def replace_urls_with_markdown_links(text):
    # Regular expression pattern for matching URLs
    url_pattern = r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)'
    
    # Function to replace each URL with markdown link
    def replace_with_markdown(match):
        url = match.group(0)
        return f'[{url}]({url})'
    
    # Use re.sub() to replace all URLs in the text with markdown links
    markdown_text = re.sub(url_pattern, replace_with_markdown, text)
    
    return markdown_text

def escape_markdown(text):
    # List of markdown special characters
    # ! removed ()
    markdown_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '#', '+', '-', '.', '!']
    # Escape each special character with a backslash
    for char in markdown_chars:
        text = text.replace(char, '\\' + char)
    return text

def as_raw(text):
    return replace_urls_with_markdown_links(escape_markdown(str(text)))

def as_code(text):
    return f'`{text}`'

def as_is(text):
    return text
