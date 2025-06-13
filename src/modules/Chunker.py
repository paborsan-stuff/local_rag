import re
import uuid
from transformers import AutoTokenizer, AutoModel

DEFAULT_CHUNK_SIZE_IN_TOKEN = 1024
class Chunker:

    PARAGRAPH_SEPARATOR = "\n\n"

    def __init__(self, tokenizer=None, chunk_delimiter=256, overlap_tokens=24, paragraph_separator_regex="", chunk_word_delimiter_regex="", input_text = ""):
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

        self.overlap_tokens = overlap_tokens
        self.input = input_text
        self.chunk_delimiter = chunk_delimiter
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)

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

    # def _paragraph_chunker(self, paragraph: str, delimiter: str):
    #     """
    #     Splits a given text into chunks based on a regex delimiter and a maximum token limit.

    #     Args:
    #         text (str): The input text to chunk.
    #         delimiter_regex (re.Pattern): The compiled regex pattern to split the text by.

    #     Returns:
    #         list[str]: A list of text chunks.
    #     """
    #     words = paragraph.split(delimiter)
    #     current_chunk = ""

    #     tokenized = self.tokenizer.tokenize(paragraph)

    #     chunked_tokens = self.slice_array_by_size_loop(tokenized, self.chunk_delimiter)

    #     return self.assign_tokens(chunked_tokens)
    
    def _paragraph_chunker(self, paragraph: str, delimiter: str):
        if not paragraph.strip():
            return {}

        # Fase 1: Primera división basada en palabras (max_tokens)
        words = paragraph.split(delimiter)
        current_text_chunk = "" 
        temp_word_chunks = [] 

        for word in words:
            text_with_new_word = current_text_chunk + (delimiter if current_text_chunk else '') + word

            if self._get_token_count(text_with_new_word) <= self.chunk_delimiter:
                current_text_chunk = text_with_new_word
            else:
                if current_text_chunk: 
                    temp_word_chunks.append(current_text_chunk)
                current_text_chunk = word

        if current_text_chunk:
            temp_word_chunks.append(current_text_chunk)

        # Fase 2: Refinamiento de chunks si son demasiado grandes
        refined_token_chunks = []

        for chunk_text in temp_word_chunks:
            chunk_tokens = self.tokenizer.tokenize(chunk_text)

            if len(chunk_tokens) > self.chunk_delimiter:
                sub_chunks_text = re.split(self.secondary_chunking_regex, chunk_text)
                
                current_sub_chunk_tokens = []
                current_sub_chunk_text = "" 

                for sub_chunk_part in sub_chunks_text:
                    if not sub_chunk_part.strip():
                        continue

                    full_part_text = sub_chunk_part
                    match = re.search(self.secondary_chunking_regex, chunk_text[chunk_text.find(sub_chunk_part) + len(sub_chunk_part):])
                    if match:
                         full_part_text += match.group(0)

                    test_text = current_sub_chunk_text + full_part_text
                    test_tokens = self.tokenizer.tokenize(test_text)

                    if len(test_tokens) <= self.chunk_delimiter:
                        current_sub_chunk_text = test_text
                        current_sub_chunk_tokens = test_tokens
                    else:
                        if current_sub_chunk_tokens:
                            refined_token_chunks.append(current_sub_chunk_tokens)

                        if len(self.tokenizer.tokenize(full_part_text)) > self.chunk_delimiter:
                             oversized_part_tokens = self.tokenizer.tokenize(full_part_text)
                             sliced_oversized = self.slice_array_by_size_loop(oversized_part_tokens, self.chunk_delimiter)
                             refined_token_chunks.extend(sliced_oversized)
                             current_sub_chunk_tokens = [] 
                             current_sub_chunk_text = ""
                        else:
                            current_sub_chunk_text = full_part_text
                            current_sub_chunk_tokens = self.tokenizer.tokenize(full_part_text)

                if current_sub_chunk_tokens:
                    refined_token_chunks.append(current_sub_chunk_tokens)
            else:
                refined_token_chunks.append(chunk_tokens)

        # Fase 3: Aplicar solapamiento (Overlap)
        final_processed_token_chunks = []

        if self.overlap_tokens > 0 and len(refined_token_chunks) > 1:
            for i in range(len(refined_token_chunks)):
                current_chunk = refined_token_chunks[i]
                
                final_processed_token_chunks.append(current_chunk)

                if i < len(refined_token_chunks) - 1:
                    next_chunk = refined_token_chunks[i+1]

                    overlap_from_current = current_chunk[-min(self.overlap_tokens, len(current_chunk)):]

                    overlap_into_next = next_chunk[:min(self.overlap_tokens, len(next_chunk))]
                    combined_overlap_tokens = overlap_from_current + next_chunk
                    
                    if len(combined_overlap_tokens) > self.chunk_delimiter:

                        overlap_tokens_combined = []
                        
                        overlap_tokens_combined.extend(current_chunk[-min(self.overlap_tokens, len(current_chunk)):])

                        remaining_space = self.chunk_delimiter - len(overlap_tokens_combined)
                        if remaining_space > 0:
                            overlap_tokens_combined.extend(next_chunk[:min(remaining_space, len(next_chunk))])

                        if overlap_tokens_combined:
                            final_processed_token_chunks.append(overlap_tokens_combined)

            pass
        else:
            final_processed_token_chunks = refined_token_chunks

        return self.assign_tokens(final_processed_token_chunks)
    
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