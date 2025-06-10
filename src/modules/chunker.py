import re
import os
import uuid
from transformers import AutoTokenizer, AutoModel

DEFAULT_CHUNK_SIZE_IN_TOKEN = 1024
class Chunker:

    PARAGRAPH_SEPARATOR = "\n\n"

    def __init__(self, tokenizer=None, chunk_delimiter=3, paragraph_separator_regex="", chunk_word_delimiter_regex="", input_text = ""):
        """
        Initializes the Chunker with a Hugging Face tokenizer, a target chunk size,
        and configurable regex delimiters for text splitting.

        Args:
            model_name (str): The name of the Hugging Face model to load the tokenizer from.
                              (e.g., 'BAAI/bge-small-en-v1.5').
            chunk_size_in_token (int): The target maximum number of tokens per chunk.
            paragraph_separator_regex (str, optional): A regex pattern to split the main text into paragraphs.
                                                      If None, uses DEFAULT_PARAGRAPH_SEPARATOR_REGEX.
            chunk_word_delimiter_regex (str, optional): A regex pattern to split paragraphs into smaller sections (e.g., words).
                                                        If None, uses DEFAULT_WORD_DELIMITER_REGEX.
        """
        if input_text == None:
            raise TypeError  ("Bad init, input text is empty")

        self.input = input_text
        self.chunk_delimiter = chunk_delimiter
        self.tokenizer = tokenizer

    def _get_token_count(self, text: str) -> int:
        """
        Calculates the number of tokens in a given text using the loaded tokenizer.

        Args:
            text (str): The input text.

        Returns:
            int: The number of tokens.
        """
        # The `encode` method returns a list of token IDs
        return len(self.tokenizer.tokenize(text))
    
    @staticmethod
    def slice_array_by_size_loop(arr, chunk_size):
        sliced_arrays = []

        #
        # TODO: Check this...
        #
        if  len(arr) < chunk_size:
            return arr

        # Iterate from 0 up to the length of the array, stepping by chunk_size
        for i in range(0, len(arr), chunk_size):
            # Slice the array from the current index 'i' up to 'i + chunk_size'
            sliced_arrays.append(arr[i : i + chunk_size])
        
        return sliced_arrays

    def _refine_chunk (self):
        """
        Implement if we have too
        """
        pass
    
    def assign_tokens (self, chunked_tokens):

        final_chunks = {}

        for chunk in chunked_tokens:
            chunk_id = str(uuid.uuid4())
            #
            #  TODO: Do we need more keys?
            #
            final_chunks[chunk_id] = {"text": " ".join(chunk)}  # Initialize metadata as dict

        return final_chunks

    def _paragraph_chunker(self, paragraph: str, delimiter: str):
        """
        Splits a given text into chunks based on a regex delimiter and a maximum token limit.

        Args:
            text (str): The input text to chunk.
            delimiter_regex (re.Pattern): The compiled regex pattern to split the text by.

        Returns:
            list[str]: A list of text chunks.
        """
        words = paragraph.split(delimiter)
        current_chunk = ""

        tokenized = self.tokenizer.tokenize(paragraph)

        chunked_tokens = self.slice_array_by_size_loop(tokenized, self.chunk_delimiter)

        return self.assign_tokens (chunked_tokens)
    
    def process_paragraphs(self):
        """
        Processes the input text, splitting it into paragraphs and then into smaller chunks
        based on token limits using the configured regex delimiters.

        Args:
            text_to_chunk (str): The full text string to be chunked. Defaults to TEST_PARAGRAPHS.

        Returns:
            list[str]: A list of processed text chunks.
        """
        final_chunks = {}

        paragraphs = self.input.split(self.PARAGRAPH_SEPARATOR)
        for paragraph in paragraphs:
            final_chunks.update(self._paragraph_chunker(paragraph, " "))

        return final_chunks