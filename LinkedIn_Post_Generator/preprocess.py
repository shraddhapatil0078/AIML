import json

from future.backports.http.client import responses
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import  OutputParserException
from llm_helper import llm


def process_posts(raw_file, processed_file="data/processed_posts.json"):
    enriched_post = []
    with open(raw_file, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_post.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_post)

    for post in enriched_post:
        current_tags = post['tags']
        new_tags = {unified_tags[tag] for tag in current_tags}
        post['tags']=list(new_tags)

    with open(processed_file, encoding='utf-8', mode='w') as outfile:
        json.dump(enriched_post, outfile, indent=4)

def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    for post in posts_with_metadata:
        unique_tags.update(post['tags'])

    unique_tags_list = ', '.join(unique_tags)

    template = '''I will give you a list of tags. You need to unify tags with following requirements,
    1. Tags are unified and merged to create shorter list
    2. Each tag should follow title case convention.
    3. Output should be a JSON object, No preamble
    4. Output should have mapping of original tag and the unified tag.
    
    Here is the list of tags:
    {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'tags': str(unique_tags_list)})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context is too big, Unable to parse jobs.")
    return res


def extract_metadata(post):
    template = '''
    You are given a LinkedIn post, You need to extract number of lines, langauge of the post and tags.
    1. Return a Valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, langauge and tags.
    3. tags is an array of text tags. Extract maximum two tags if any are present.
    4. Langauge should be English.
    
    Here is the actual post on which you need to perform this task:
    {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post})

    try:
        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Context is too big, Unable to parse jobs.")
    return res


if __name__ == "__main__":
    process_posts("data/raw_posts.json", "data/processed_posts.json")
