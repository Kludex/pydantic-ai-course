from pydantic_ai import Agent
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)


agent = Agent("openai:gpt-4.1-nano")

result = agent.run_sync("Ola, tudo bem?")
print(result.output)
