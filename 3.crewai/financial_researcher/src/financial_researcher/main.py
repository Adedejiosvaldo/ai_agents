#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from financial_researcher.crew import FinancialResearcher

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {"company_name": "Tesla"}

    try:
        results = FinancialResearcher().crew().kickoff(inputs=inputs)
        print(f"Crew execution completed successfully. Result: {results}")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
