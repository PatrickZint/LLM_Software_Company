# This is a stub for the formatting controller. It is responsible for toggling between Markdown and WYSIWYG modes.


class FormattingController:
    def __init__(self):
        pass

    def toggle_formatting(self, content, mode='markdown'):
        # This stub function can later implement conversions between markdown and WYSIWYG formatted content.
        if mode == 'markdown':
            # Return raw markdown
            return content
        else:
            # Convert markdown to a richer formatted text; for now, simply return the original content
            return content
