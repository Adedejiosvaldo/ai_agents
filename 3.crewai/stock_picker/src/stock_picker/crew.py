from pydantic import BaseModel, Field
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


class TrendingCompany(BaseModel):
    """Trending company model"""

    name: str = Field(description="Company name")
    ticker: str = Field(description="Company ticker symbol")
    reasons: str = Field(description="Reasons for trending")
    url: str = Field(description="URL to the company's website")


class TrendingCompanies(BaseModel):
    """Trending companies model"""

    companies: List[TrendingCompany] = Field(
        description="List of trending companies based on latest news"
    )


class TrendingCompanyResearch(BaseModel):
    """Trending company research model"""

    company: TrendingCompany = Field(description="Trending company")
    market_position: str = Field(description="Market position of the trending company")
    future_outlook: str = Field(description="Future outlook of the trending company")
    investment_potential: str = Field(
        description="Investment potential of the trending company"
    )


class TrendingCompaniesResearchList(BaseModel):
    """Trending companies research list model"""

    research: List[TrendingCompanyResearch] = Field(
        description="List of research on trending companies"
    )


@CrewBase
class StockPicker:
    """StockPicker crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trending_agent(self) -> Agent:
        """Trending agent"""
        return Agent(
            config=self.agents_config["trending_company_finder"],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def financial_researcher(self) -> Agent:
        """Financial researcher agent"""
        return Agent(
            config=self.agents_config["financial_researcher"],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def stock_picker(self) -> Agent:
        """Stock picker agent"""
        return Agent(
            config=self.agents_config["stock_picker"],
            verbose=True,
        )

    @task
    def find_trending_companies_task(self) -> Task:
        """Trending companies task"""
        return Task(
            config=self.tasks_config["find_trending_companies"],
            output_pydantic=TrendingCompanies,
        )

    @task
    def research_trending_companies_task(self) -> Task:
        """Research trending companies task"""
        return Task(
            config=self.tasks_config["research_trending_companies"],
            output_pydantic=TrendingCompaniesResearchList,
        )

    @task
    def pick_best_company_task(self) -> Task:
        """Pick best company task"""
        return Task(
            config=self.tasks_config["pick_best_company"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        manager_agent = Agent(
            config=self.agents_config["manager"], allow_delegation=True, verbose=True
        )
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager_agent,
        )
