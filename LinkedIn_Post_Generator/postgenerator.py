from llm_helper import llm
from few_shots import FewShotPosts

few_shots = FewShotPosts()

def get_length_generator(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def get_prompt(length, langauge, tag):
    len_str = get_length_generator(length)
    prompt = f'''
        Generate a LinkedIn post using below information. No preamble
        1) Topic: {tag}
        2) Length: {len_str}
        3) Langauge: {langauge}

        The script for the generated post should be always English
        Each Bullet points should be on new line.
    '''
    examples = few_shots.get_filtered_posts(length, langauge, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following example."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i + 1}: \n\n {post_text}'

        if i == 1:  # Use max two samples
            break
    return prompt

def generate_post(length, langauge, tag):

    prompt = get_prompt(length, langauge,tag)
    response = llm.invoke(prompt)
    return response.content