import string

class StringUtils:

    @staticmethod
    def graphic_as_string(texts, width=45):
        if isinstance(texts, str):
            texts = [texts]
        border = '>' * (width//2) + ('*' if width % 2 else '') + '<' * (width//2)
        graphic_string = border + "\n"

        for text in texts:
            empty_space = ' ' * ((width - len(text) - 4) // 2)
            graphic_string += '||' + empty_space + text + empty_space + (
                ' ||' if len(empty_space) * 2 + len(text) + 5 == width else '||') + "\n"

        graphic_string += border
        return graphic_string

    @staticmethod
    def get_ascii_chars():
        """
        Returns a set of ASCII characters.
        """
        return set(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
