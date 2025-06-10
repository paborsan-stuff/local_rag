import sys
from llama_cpp import Llama # Assuming llama_cpp is installed: pip install llama-cpp-python

class LLMAdapter:
    """
    Handles prompt construction and streaming/buffering interactions with a Llama model.
    """

    def __init__(self,
                 llm: Llama, # The Llama model instance (from llama_cpp)
                 default_max_tokens: int = 800,
                 default_stop_sequences: list[str] = None, # Default stop sequences for generation
                 default_echo: bool = False, # Whether to echo the prompt in the output
                 default_stream: bool = True): # Whether to stream the response
        """
        Initializes the LLMInteractionHandler with a Llama model instance and default generation parameters.

        Args:
            llm (Llama): An initialized instance of the Llama model from llama_cpp.
            default_max_tokens (int): The default maximum number of tokens to generate.
            default_stop_sequences (list[str]): A list of strings that will stop generation.
                                                Defaults to ["Q:", "\n"] if None.
            default_echo (bool): Default setting for echoing the prompt in the output.
            default_stream (bool): Default setting for streaming the response.
        """
        self.llm = llm
        self.default_max_tokens = default_max_tokens
        self.default_stop_sequences = default_stop_sequences if default_stop_sequences is not None else ["Q:", "\n"]
        self.default_echo = default_echo
        self.default_stream = default_stream

    @staticmethod
    def construct_prompt(system_prompt: str, retrieved_docs: str, user_query: str) -> str:
        """
        Constructs a formatted prompt string for the LLM, combining system instructions,
        retrieved context, and the user's query.

        Args:
            system_prompt (str): High-level instructions or persona for the LLM.
            retrieved_docs (str): The relevant context retrieved from a document store.
            user_query (str): The user's specific question or request.

        Returns:
            str: The complete, formatted prompt string.
        """
        prompt = f"""{system_prompt}Here is the retrieved context:{retrieved_docs}Here is the user's query:{user_query}"""
        return prompt

    def stream_and_buffer_response(self,
                                   base_prompt: str,
                                   max_tokens: int = None,
                                   stop: list[str] = None,
                                   echo: bool = None,
                                   stream: bool = None) -> str:
        """
        Streams the response from the LLM, buffering words and printing them to stdout
        as they become complete. This provides a typewriter-like effect.

        Args:
            base_prompt (str): The prompt to send to the LLM (e.g., constructed via construct_prompt).
            max_tokens (int, optional): Max tokens to generate for this specific call.
                                        Defaults to instance's default_max_tokens.
            stop (list[str], optional): Stop sequences for this specific call.
                                       Defaults to instance's default_stop_sequences.
            echo (bool, optional): Echo prompt for this specific call.
                                   Defaults to instance's default_echo.
            stream (bool, optional): Stream response for this specific call.
                                     Defaults to instance's default_stream.

        Returns:
            str: The complete buffered response from the LLM.
        """
        # Use provided parameters or fall back to instance defaults
        actual_max_tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        actual_stop = stop if stop is not None else self.default_stop_sequences
        actual_echo = echo if echo is not None else self.default_echo
        actual_stream = stream if stream is not None else self.default_stream

        # Format the prompt for the Llama model's specific input style (Q: A: )
        # This part is specific to the original `stream_and_buffer`'s intent.
        formatted_llm_prompt = f"Q: {base_prompt} A: "

        # Stream the response from the Llama model
        response_generator = self.llm(
            formatted_llm_prompt,
            max_tokens=actual_max_tokens,
            stop=actual_stop,
            echo=actual_echo,
            stream=actual_stream
        )

        buffer = ""
        full_response_text = ""

        # Iterate over the streamed message chunks
        for message in response_generator:
            chunk = message['choices'][0]['text']
            buffer += chunk
            full_response_text += chunk # Accumulate the full response

            # Split at the last space to get complete words
            words = buffer.split(' ')
            # Process all words except the last one (which might be incomplete)
            for word in words[:-1]:
                sys.stdout.write(word + ' ')  # Write the complete word to stdout
                sys.stdout.flush()  # Ensure immediate display

            # Keep the last part (potentially incomplete word) in the buffer
            buffer = words[-1]

        # After the loop, print any remaining content in the buffer
        if buffer:
            sys.stdout.write(buffer)
            sys.stdout.flush()

        # Add a newline for clean output after the streamed response
        sys.stdout.write('\n')
        sys.stdout.flush()

        return full_response_text.strip() # Return the complete, trimmed response
