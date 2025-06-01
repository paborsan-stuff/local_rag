import re
import os
import uuid
from transformers import AutoTokenizer, AutoModel

TEST_PARAGRAPH  = """Basement home theater seating in black leather, includes three reclining seats with cup holders and storage compartments.
Designed for ultimate comfort and convenience during movie nights. 
Manufactured by Luxe Seating. Dimensions per seat: 36"W x 40"D x 40"H."""

CHUNK_WORD_SECTION_LIST_FORMATTER = "{word},"

DEFAULT_CHUNK_SIZE_IN_TOKEN = 1024
class Chunker:
    
    def __init__ (self, tokenizer = None, chunk_delimiter = 1024):
       chunk_delimiter = chunk_delimiter
       
    def paragraph_splitter (self, paragraph:str, delimiter:str):
    
      words = paragraph.split(delimiter)
      current_chunk = ""
      for word in words:
          current_chunk += (delimiter if current_chunk else '') + word
      
      return current_chunk

test_chunker = Chunker ()

test_chunker.paragraph_splitter(TEST_PARAGRAPH, ".")