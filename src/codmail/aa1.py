from typing import Literal
from pydantic import BaseModel
from pydantic_ai import Agent, ModelSettings
from pydantic_ai.models.groq import GroqModel

model = GroqModel("openai/gpt-oss-120b")

agent = Agent(model)

#class Status(BaseModel):
#    title: str
#    label: Literal['incomplete', 'complete']

#prompt1 = "Current tasks: {'task1': {'title':'USPCodeLab task 1', 'label': 'incomplete'}, 'task2': {'title':'USPCodeLab task 2', 'label': 'complete'}}. What is the info on task2?"

response = agent.run_sync(
    "Write a one-sentence bedtime story about a unicorn",
    #output_type=Status,
    model_settings=ModelSettings(max_tokens=200),
)

print(response.output)
