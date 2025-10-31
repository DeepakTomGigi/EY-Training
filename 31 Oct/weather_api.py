from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import requests
import os
import litellm

load_dotenv()
os.environ["OPENROUTER_CREWAI_KEY"] = os.getenv("OPENROUTER_CREWAI_KEY")


litellm.api_key = os.getenv("OPENROUTER_CREWAI_KEY")
litellm.api_base = "https://openrouter.ai/api/v1"
model_name = "openrouter/meta-llama/llama-3.3-8b-instruct:free"

# Define the input schema for your tool
class FetchWeatherInput(BaseModel):
    city: str = Field(..., description="Name of the city to fetch the weather report for")


# Create a custom tool by subclassing BaseTool
class FetchWeatherTool(BaseTool):
    name: str = "fetch_weather"
    description: str = "Fetches the current weather report for a given city using OpenWeatherMap API"
    args_schema: type[BaseModel] = FetchWeatherInput  # ✅ type annotation required

    def _run(self, city: str) -> str:
        """Fetch weather data from OpenWeatherMap API"""
        try:
            API_KEY = "your_openweather_api_key_here"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                return f"Failed to fetch weather data: {data.get('message', 'Unknown error')}"

            weather = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]

            return f"Weather in {city}: {weather}, Temperature: {temperature}°C, Humidity: {humidity}%"
        except Exception as e:
            return f"Error fetching weather: {e}"


# Initialize your LLM (you can change model name as needed)
# llm = LLM(model="gpt-4-turbo")


# Create an agent that uses the weather tool
weather_agent = Agent(
    role="Weather Analyst",
    goal="Provide the current weather details of any given city",
    backstory="You are an expert meteorologist who fetches accurate weather reports from APIs.",
    tools=[FetchWeatherTool()],
    llm=model_name
)


# Define the task that uses the agent
weather_task = Task(
    description="Fetch the current weather details for the requested city.",
    agent=weather_agent,
    expected_output="A detailed weather report with temperature, humidity, and sky conditions."
)


# Create the crew
crew = Crew(
    agents=[weather_agent],
    tasks=[weather_task],
    process=Process.sequential
)


if __name__ == "__main__":
    city = input("Enter a city name: ")
    result = crew.kickoff(inputs={"city": city})
    print("\n=== Weather Report ===")
    print(result)
