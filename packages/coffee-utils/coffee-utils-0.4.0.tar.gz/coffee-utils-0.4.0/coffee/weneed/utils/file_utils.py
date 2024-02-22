import os
from coffee.weneed.utils.string_utils import StringUtils


class FileUtils:
    """
    A utility class for working with files.
    """

    @staticmethod
    def strip_non_ascii_filenames(directory, file_extension=None, recursive=False):
        """
        Traverses through the provided directory and renames files in it by
        removing non-ASCII characters, ensuring they don't overwrite an existing file.

        Parameters:
        directory (str): Path to the directory to process.
        file_extension (str, optional): Only files with this extension are processed. If None, all files are processed.
        recursive (bool, optional): If True, subdirectories are processed recursively. Default is False.
        """
        ascii_chars = StringUtils.get_ascii_chars()

        for root, _, filenames in os.walk(directory) if recursive else [(directory, [], os.listdir(directory))]:
            for filename in filenames:
                if file_extension is None or filename.endswith(file_extension):
                    directory, old_filename = os.path.split(os.path.join(root, filename))
                    base, ext = os.path.splitext(old_filename)
                    new_base = ''.join(c for c in base if c in ascii_chars)

                    if base != new_base:
                        new_filename = new_base
                        counter = 1
                        while os.path.exists(os.path.join(directory, new_filename + ext)):
                            new_filename = new_base + "_" + str(counter)
                            counter += 1

                        os.rename(os.path.join(directory, old_filename), os.path.join(directory, new_filename + ext))
