import random
import time
from typing import Callable, Any
from openai import RateLimitError


# Define a retry decorator with exponential backoff
def retry_with_exponential_backoff(
    func: Callable[[Any], Any],  # The function to be decorated
    initial_delay: float = 1,  # Initial delay before the first retry
    exponential_base: float = 2, # Base for the exponential backoff
    jitter: bool = True,  # Whether to add randomness to the delay
    max_retries: int = 10,  # Maximum number of retries
    errors: tuple = (RateLimitError,),  # Errors to retry on
) -> Callable[[Any], Any]:
    """
    This function is from OpenAI Cookbook.

    This decorator retries a function with exponential backoff when specified errors occur.
    The retries are performed with an exponential backoff delay (optionally: with randomized jitter).

    Callable[[Any], Any]:
        Callable: This indicates that the type is a function.
        [Any]: The inner list [Any] indicates that the function can accept any number and any type of arguments.
        Any: The outer Any indicates that the function can return a value of any type.

    Parameters:
    -----------
    func : Callable[[Any], Any]
        The function to be decorated.
    initial_delay : float, optional
        The initial delay before the first retry in seconds (default is 1 second).
    exponential_base : float, optional
        The base for the exponential backoff (default is 2).
    jitter : bool, optional
        Whether to add randomness to the delay (default is True).
    max_retries : int, optional
        The maximum number of retries before giving up (default is 10).
    errors : tuple, optional
        A tuple of exception classes to retry on (default is (openai.RateLimitError,)).

    Returns:
    --------
    Callable[[Any], Any]
        The wrapped function with retry logic applied.

    Raises:
    -------
    Exception
        If the maximum number of retries is exceeded, an exception is raised.
    """

    def wrapper(*args, **kwargs):
        
        num_retries = 0  # Counter for the number of retries
        delay = initial_delay  # Initial delay before retrying

        # Loop until one of these occurs:
        # - a successful response
        # - max_retries is hit
        # - an exception is raised
        while True:
            try:
                # Try to execute the function
                return func(*args, **kwargs)

            # Retry on specified errors
            except errors as e:
                num_retries += 1

                # Check if max retries has been reached
                if num_retries > max_retries:
                    # Raise an exception if the maximum number of retries is exceeded
                    raise Exception(
                        f"Maximum number of retries ({max_retries}) exceeded."
                    )

                # Increment the delay using exponential backoff and jitter
                delay *= exponential_base * (1 + jitter * random.random())

                # Sleep for the current delay duration before the next retry
                time.sleep(delay)

            # Raise exceptions for any errors not specified
            except Exception as e:
                raise e 

    return wrapper
