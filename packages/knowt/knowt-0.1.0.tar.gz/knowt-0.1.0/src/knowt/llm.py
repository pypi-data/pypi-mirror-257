"""
>>> db = VectorDB()
>>> db.search('What is the healthiest fruit?')
>>> context = '\n'.join(list(contextdf['sentence']))
>>> rag('What is the healthiest fruit?', context=context)
>>> q = 'How much exercise is healthiest?'
>>> context = '\n'.join([s for s in df2['sentence']])
>>> rag(q, context=context)
"""
import sys
import dotenv
import logging
from openai import OpenAI
from search_engine import VectorDB
import pdb

try:
    log = logging.getLogger(__name__)
except NameError:
    log = logging.getLogger('llm.__main__')


dotenv.dotenv_values()
env = dotenv.dotenv_values()
OPENROUTER_API_KEY = env['OPENROUTER_API_KEY']
CLIENT = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# globals().update(env)
LLM_MODELS = (
    'meta-llama/llama-2-13b-chat',  # expensive
    "openai/gpt-3.5-turbo",  # free?
    'auto',  # unknown?
    'open-orca/mistral-7b-openorca',  # cheaper/better than Llama-2-13
    "mistralai/mistral-7b-instruct",  # free
)
LLM_MODEL = LLM_MODELS[-1]

PROMPT_EXAMPLES = []
PROMPT_EXAMPLES += [["PUG meetup", "2024-01-27", (
    "You are an elementary school student answering questions on a reading comprehension test. "
    "Your answers must only contain information from the passage of TEXT provided. "
    "Read the following TEXT and answer the QUESTION below the text as succintly as possible. "
    "Do not add any information or embelish your answer. "
    "You will be penalized if you include information not contained in the TEXT passage. \n\n"
    "TEXT: {context}\n\n"
    "QUESTION: {question}\n\n")]]
PROMPT_EXAMPLES += [["for vish", "2024-02-01", (
    "You are an elementary school student answering questions on a reading comprehension test. "
    "Your answers must only contain information from the passage of TEXT provided. "
    "Read the following TEXT and answer the QUESTION below the text as succinctly as possible. "
    "Do not add any information or embelish your answer. "
    "You will be penalized if your ANSWER includes any information not contained in the passage of TEXT provided above the QUESTION. \n\n"
    "TEXT: {context}\n\n"
    "QUESTION: {question}\n\n"
    "ANSWER: ")]]
PROMPT_EXAMPLES += [["", "2024-02-12", (
    "You are an elementary school student answering questions on a reading comprehension exam. \n"
    "To answer the exam QUESTION, first read the TEXT provided to see if it contains enough information to answer the QUESTION. \n"
    "Read the TEXT provided below and answer the QUESTION as succinctly as possible. \n"
    "Your ANSWER should only contain the facts within the TEXT. \n"
    "If the TEXT provided does not contain enough information to answer the QUESTION you should ANSWER with \n "
    "'I do not have enough information to answer your question.'. \n"
    "You will be penalized if your ANSWER includes any information not contained in the TEXT provided. \n\n"
    "TEXT: {context}\n\n"
    "QUESTION: {question}\n\n"
    "ANSWER: ")]]


PROMPT_TEMPLATE = PROMPT_EXAMPLES[-1][-1]

PROMPT_NO_CONTEXT = (
    "You are an AI virtual assistant and search engine."
    "You answer questions truthfully and succinctly as if you are a witness at a legal trial.\n\n"
    "QUESTION: {question}\n\n"
    "ANSWER: "
)


def ask_llm(question='What is Python?',
            context='Python is fast.',
            prompt_template=PROMPT_TEMPLATE,
            client=CLIENT,
            model='meta-llama/llama-2-13b-chat'):
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "https://qary.ai",  # Optional, for including your app on openrouter.ai rankings.
            "X-Title": "https://qary.ai",  # Optional. Shows in rankings on openrouter.ai.
        },
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt_template.format(context=context, question=question)}, ],)
    return [c.message.content for c in completion.choices]


class RAG:

    def __init__(self, prompt_template=PROMPT_TEMPLATE, llm_model=LLM_MODEL, client=None, db=None):
        global CLIENT
        client = client or CLIENT
        self.db = db or VectorDB()
        self.client = client
        self.prompt_template = PROMPT_TEMPLATE
        self.llm_model_name = llm_model
        self.hist = []
        self.search_results = None

    def setattrs(self, *args, **kwargs):
        if len(args) and isinstance(args[0], dict):
            kwargs.update(args[0])
        for k, v in kwargs.items():
            # TODO: try/except better here
            if not hasattr(self, k):
                log.error(f'No such attribute "{k}" in a {self.__class__.__name__} class!')
                raise AttributeError(f'No such attribute in a {self.__class__.__name__} class!')
            setattr(self, k, v)

    def ask(self, question, context=-1, **kwargs):
        self.question = question
        self.setattrs(kwargs)
        if (context or context == 0) and not len(self.hist):
            self.search_results = self.db.search(question, limit=8)
            self.search_results = self.search_results[self.search_results['relevance'] > .45]
            context = '\n'.join(list(self.search_results['sentence']))
        if isinstance(context, int):
            try:
                context = self.hist[context]['context']
            except IndexError:
                context = self.hist[-1]['context']
        self.context = context or 'No information found.'
        self.hist.append(dict(
            question=self.question,
            context=self.context,
            prompt_template=self.prompt_template,
            search_results=self.search_results))
        print(len(self.hist))
        # pdb.set_trace()
        self.prompt = self.prompt_template.format(**self.hist[-1])  # **vars(self))
        self.hist[-1].update(dict(prompt=self.prompt))
        self.completion = self.client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://qary.ai",  # Optional, for including your app on openrouter.ai rankings.
                "X-Title": "https://qary.ai",  # Optional. Shows in rankings on openrouter.ai.
            },
            model=self.llm_model_name,
            messages=[{"role": "user", "content": self.prompt}, ],)
        # TODO: function to flatten an openAI Completion object into a more open-standard interoperable format
        self.answer = self.completion.choices[0].message.content
        self.answer_id = self.completion.id
        self.answer_logprob = self.completion.choices[0].logprobs
        # FIXME: .hist rows should each be temporarily stored in a .turn dict with well-defined schema accepted by all functions
        self.hist[-1].update(dict(prompt=self.prompt, answer=self.answer, answer_id=self.answer_id))  # answer=completion['content']
        return self.answer


if __name__ == '__main__':
    question = ' '.join(sys.argv[1:])
    rag = RAG()
    answers = [rag.ask(question)]
    # answers = ask_llm(
    #     question=question,
    #     model='auto',
    #     context='',
    #     prompt_template=PROMPT_NO_CONTEXT)
    print(answers + '\n')
