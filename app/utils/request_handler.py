from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from app.utils.openai_config import OpenAIModels
from app.utils.rate_limiter import retry_with_exponential_backoff


def count_token_usage(api_response: ChatCompletion) -> tuple:
    """
    Count how many token have been sent to the API.
    This version is specific for OpenAI and Streamlit.

    Parameters:
    -----------
    api_response: ChatCompletion
        Object returned by a synchronous openai client instance

    Returns:
    -----------
    tuple
        the number of tokens used:
        - 'completion_tokens': token generated by the model.
        - 'prompt_tokens': tokens sent to the api.
        - 'total_tokens': total count of used tokens.
    """

    completion_tokens = api_response.usage.completion_tokens
    prompt_tokens = api_response.usage.prompt_tokens
    total_tokens = api_response.usage.total_tokens

    return (completion_tokens, prompt_tokens, total_tokens)


@retry_with_exponential_backoff
def send_request(client: OpenAI, model: OpenAIModels, system_prompt: str, prompt: str, temperature: float) -> tuple[str, tuple]:
    """
    Call the API and get the response.

    Parameters:
    -----------
    client: OpenAI
        Object that manage the call to OpenAI API.
    model: OpenAIModels
        Name of the OpenAI model.
    system_prompt: str
        A prompt used to inform the model how to modify the user text.
    prompt: str
        Prompt including the instructions and the original text provided by the user.
    temperature: float
        Temperature for the OpenAI model.

    Returns:
    -----------
    turple
        response: str
            Response from api.
        token_usage: tuple
            The number of tokens used.
    """

    chat_completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature
    )

    response = chat_completion.choices[0].message.content

    token_usage = count_token_usage(chat_completion)

    return response, token_usage


def handle_request(prompt: str, client: OpenAI, model: OpenAIModels, temperature: float) -> tuple[str, str]:
    """
    This function perform the following steps:
    1) Call a function to create a prompt to split and classify the text.
    2) Call the API with the create prompt to get the text classification.
    3) Call a function to create a prompt to use to edit the text into a more functional version.
    4) Call the API with the second prompt to get the modified functional text.

    Parameters:
    -----------
    prompt: str
        Prompt to pass to the OpenAI model.  
    client: OpenAI
        Object that manage the call to OpenAI API.
    model: OpenAIModels
        Name of the OpenAI model.
    temperature: float
        Temperature for the OpenAI model.

    Returns:
    -----------
    turple
        A tuple with the following objects:
        edited_text: str
            Text converted in a more functional version.
        total_token: str
            Total count of used tokens.
    """

    transformed_text, token_usage = send_request(
        client= client,
        model=model,
        system_prompt="",
        prompt=prompt,
        temperature=temperature)
    
    # Get total token usage
    _, _, total_token = token_usage

    return transformed_text, total_token
