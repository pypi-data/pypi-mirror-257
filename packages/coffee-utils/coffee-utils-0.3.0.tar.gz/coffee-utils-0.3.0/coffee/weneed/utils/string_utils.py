import string


class StringUtils:

    @staticmethod
    def graphic_as_string(texts, width=49):
        if isinstance(texts, str):
            texts = [texts]
        border = '=' * width
        graphic_string = border + "\n"

        for text in texts:
            empty_space = ' ' * ((width - len(text) - 4) // 2)
            graphic_string += '== ' + empty_space + text + empty_space + (
                '==' if len(empty_space) * 2 + len(text) + 4 == width else '===') + "\n"

        graphic_string += border
        return graphic_string

    @staticmethod
    def get_ascii_chars():
        """
        Returns a set of ASCII characters.
        """
        return set(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
