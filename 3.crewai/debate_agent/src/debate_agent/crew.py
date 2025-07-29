from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

llm_judge = LLM(model=os.getenv("GROQ_GEMMA_MODEL", "gemini/gemini-2.0-flash-lite-001")) 


@CrewBase
class DebateAgent:
    """Debate Agent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def debater(self) -> Agent:
        return Agent(
            config=self.agents_config["debater"], verbose=True  # type: ignore[index]
        )

    @agent
    def judge(self) -> Agent:
        return Agent(
            config=self.agents_config["judge"], verbose=True, llm=llm_judge  # type: ignore[index]
        )

    @task
    def propose_task(self) -> Task:
        return Task(
            config=self.tasks_config["propose"],
        )

    @task
    def oppose_task(self) -> Task:
        return Task(
            config=self.tasks_config["oppose"],
        )

    @task
    def decide_task(self) -> Task:
        return Task(
            config=self.tasks_config["decide"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debate Agent crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
