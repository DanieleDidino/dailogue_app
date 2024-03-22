def create_prompt_clf() -> str:
    """
    Build a prompt to use in OpenAI client.
    This prompt describes how to categorize the text.

    Args: None

    Returns:
        A prompt
    """

    prompt = (
        """
        You are an expert in conflict resolution and effective communication strategies, with a focus on the four communication styles identified by Dr. John Gottman.
        These styles, known as 'The Four Horsemen of the Apocalypse', are crucial in predicting the downfall of relationships.
        Your task is to classify text into one of the following categories based on these communication styles:
        
        1. 'criticism': This style involves ad hominem attacks on a partner's character rather than addressing specific issues, distinguishing it from a complaint, which targets a specific behavior.
        
        2. 'contempt': An extreme form of criticism, characterized by treating a partner with disrespect, sarcasm, and mockery, making them feel despised and worthless.
        
        3. 'defensiveness': A response to criticism where one attempts to excuse their behavior and avoid taking responsibility, often resulting in blame-shifting.
        
        4. 'stonewalling': It occurs when one partner withdraws from the interaction, shutting down communication in response to contempt.
        
        5. 'neutral': This category is used for text that does not exhibit negative communication patterns nor explicitly fits into the categories of criticism, contempt, defensiveness, or stonewalling.
        It includes statements or behaviors that are constructive, positive, or at least not harmful or negative in the context of a relationship.
        Use this category for communication that is understanding, supportive, factual without emotional charge, or otherwise not indicative of conflict.
        
        6. 'unclear': Use this category if the text does not clearly fit into any of the above categories or if it is ambiguous.
        
        Your objective is to generate a label that classifies the provided text according to these categories.
        As answer only provide the predicted label and nothing else.
        Here is the text for classification:
        """
    )
    return prompt


def create_prompt_split_clf(user_text: str) -> str:
    """
    Build a prompt to use in OpenAI client.
    This prompt describes how to split the text into chunks and classify them based on the categories described in the f-string below.

    Args: 
        user_text (str): Text to split and classify.

    Returns:
        A prompt
    """

    prompt = f"""
    Objective: Split the provided text into chunks based on the following categories: 
    'criticism', 'contempt', 'defensiveness', 'stonewalling', 'neutral'.
    If a text chunk does not belong to any specified category, classify it as 'other.'
    
    Categories Defined:
    
        1. 'criticism': This style involves ad hominem attacks on a partner's character rather than addressing specific issues, distinguishing it from a complaint, which targets a specific behavior.
        2. 'contempt': An extreme form of criticism, characterized by treating a partner with disrespect, sarcasm, and mockery, making them feel despised and worthless.
        3. 'defensiveness': A response to criticism where one attempts to excuse their behavior and avoid taking responsibility, often resulting in blame-shifting.
        4. 'stonewalling': It occurs when one partner withdraws from the interaction, shutting down communication in response to contempt.
        5. 'neutral': This category is used for text that does not exhibit negative communication patterns nor explicitly fits into the categories of criticism, contempt, defensiveness, or stonewalling.
            It includes statements or behaviors that are constructive, positive, or at least not harmful or negative in the context of a relationship.
            Use this category for communication that is understanding, supportive, factual without emotional charge, or otherwise not indicative of conflict.
        6. 'unclear': Use this category if the text does not clearly fit into any of the above categories or if it is ambiguous.
    
    Instructions:
    
        1. Read the text thoroughly.
        2. Identify and extract chunks of text that belong to the specified categories.
        3. Label each chunk with the corresponding category name.
        4. If a text chunk does not fit any of the specified categories, label it as "Other."
        5. Present the categorized text chunks in the following format:
    
    Format:
    
        Category: [Category Name]
        Text: [Extracted Text Chunk]
    
    (Repeat this format for each identified chunk.)
    
    Example:
    Given Text: "Why would I do that to you? Are you seriously blaming me for everything? I understand your feelings, and I'm sorry for causing you pain. Maybe you should take a look at your own actions before pointing fingers at me! Let me explain the reasons behind my actions so we can better understand each other."
    
    Expected Output:
    Category: criticism
    Text: Why would I do that to you? Are you seriously blaming me for everything?
    
    Category: neutral
    Text: I understand your feelings, and I'm sorry for causing you pain.
    
    Category: criticism
    Text: Maybe you should take a look at your own actions before pointing fingers at me!
    
    Category: neutral
    Text: Let me explain the reasons behind my actions so we can better understand each other.
    
    Please proceed with categorizing the following text:
    
    {user_text}
    """

    return prompt


def create_prompt_edit_text_output_textchunks(chunked_clf_text: str) -> str:
    """
    Build a prompt to use in OpenAI client.
    This prompt describes how to edit the text to covert it in a more functional version.
    This version returns the text still splitted into chunks and the output has the form:
        Category: [selected_category]
        Functional Text: [transformed_text]

    Args:
        chunked_clf_text (str): Chunks of text already split and classified.

    Returns:
        A prompt
    """

    prompt = f"""
    Objective: Transform the following categorized text chunks into a more functional language, making each chunk actionable or practical.
    The transformation should reflect the core message of each chunk, tailored to its category.

    Instructions:
    
        1. Review the categorized text chunks provided below.
        2. For each text chunk, reformulate the content into a functional, actionable format. Please rewrite the content in everyday language that sounds casual and human.
        3. Maintain the original category label for context.
        4. Present the transformed text in the following format:
    
    Format:
    
        Category: [Category Name]
        Functional Text: [Reformulated Functional Text]
    
    (Repeat this format for each chunk.)
    (Do not reformulate the category 'neutral'.)
    
    Example:
    
    Given Categorized Text Chunks:
        Category: criticism
        Text: Why would I do that to you? Are you seriously blaming me for everything?
        
        Category: neutral
        Text: I understand your feelings, and I'm sorry for causing you pain.
        
        Category: criticism
        Text: Maybe you should take a look at your own actions before pointing fingers at me!
        
        Category: neutral
        Text: Let me explain the reasons behind my actions so we can better understand each other.
    
    Expected Output:
        Category: criticism
        Functional Text: Let's assess the situation together to understand our shared responsibilities.
        
        Category: neutral
        Functional Text: I understand your feelings, and I'm sorry for causing you pain.
        
        Category: criticism
        Functional Text: Reflecting on our actions can lead to mutual understanding.
        
        Category: neutral
        Functional Text: Let me explain the reasons behind my actions so we can better understand each other.
    
    Please proceed with transforming the following text chunks into a functional language:

    {chunked_clf_text}
    """

    return prompt


def create_prompt_edit_text_output_mergedtext(chunked_clf_text: str) -> str:
    """
    Build a prompt to use in OpenAI client.
    This prompt describes how to edit the text to covert it in a more functional version.
    This version returns the text merged into a single paragraph.

    Args:
        chunked_clf_text (str): Chunks of text already split and classified.

    Returns:
        A prompt
    """

    prompt = f"""
    Objective:
        Transform the following categorized text chunks into a single, cohesive paragraph using functional language.
        Make each part of the text actionable or practical, while maintaining a natural, conversational tone.
        The goal is to present the information in a way that is easily understandable and relatable, without 
        separating them by categories or into distinct sentences.
    
    Instructions:
        1. Review the text chunks provided below.
        2. Convert each chunk into functional, everyday language, focusing on making the content actionable or practical.
        3. Merge all converted text into one continuous paragraph, ensuring a smooth flow that naturally transitions from one idea to the next.
        4. Avoid mentioning the original categories and do not separate the text into distinct sections.
        5. Aim for a conversational tone, as if explaining to a friend, to make the paragraph engaging and accessible.

    Example:

    Given Categorized Text Chunks:
        Category: criticism
        Text: Why would I do that to you? Are you seriously blaming me for everything?
        
        Category: neutral
        Text: I understand your feelings, and I'm sorry for causing you pain.
        
        Category: criticism
        Text: Maybe you should take a look at your own actions before pointing fingers at me!
        
        Category: neutral
        Text: Let me explain the reasons behind my actions so we can better understand each other.
    
    Expected Output:
        Let's assess the situation together to understand our shared responsibilities. I understand your 
        feelings, and I'm sorry for causing you pain. Reflecting on our actions can lead to mutual understanding.
        Let me explain the reasons behind my actions so we can better understand each other.
    
    Please proceed with transforming the following text chunks into a functional language:

    {chunked_clf_text}
    """

    return prompt
