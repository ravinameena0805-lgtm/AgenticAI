from agents.base_agent import BaseAgent
from models.prompt import Prompt


class TemplateAgent(BaseAgent):

    def __init__(self):

        super().__init__("TemplateAgent")

        self.current_id = 1

    def run(self, template: str):

        prompt = Prompt(

            id=self.current_id,

            template=template,

            text=template,

            strategy="Template",

            generation=0

        )

        self.current_id += 1

        return prompt