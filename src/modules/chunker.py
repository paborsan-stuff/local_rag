import re
import os
import uuid
from transformers import AutoTokenizer, AutoModel

TEST_PARAGRAPHS  = """Basement home theater seating in black leather, includes three reclining seats with cup holders and storage compartments.
Designed for ultimate comfort and convenience during movie nights. 

Manufactured by Luxe Seating. Dimensions per seat: 36"W x 40"D x 40"H."""

CHUNK_WORD_SECTION_LIST_FORMATTER = "{word},"

DEFAULT_CHUNK_SIZE_IN_TOKEN = 1024
class Chunker:
    
    PARAGRAPH_SEPARATOR = "\n\n"

    def __init__ (self, tokenizer = None, chunk_delimiter = 1024):
        chunk_delimiter = chunk_delimiter
    
    @staticmethod
    def _paragraph_splitter (paragraph:str, delimiter:str):
    
        words = paragraph.split(delimiter)
        current_chunk = ""
        w = ",".join(words)
        print (w)
        
        return current_chunk

    def process_paragraphs (self):
        
        paragraphs = TEST_PARAGRAPHS.split(self.PARAGRAPH_SEPARATOR)
        for paragraph in paragraphs:
            self._paragraph_splitter (paragraph, ' ')

           
           

