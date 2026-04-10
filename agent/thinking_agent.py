thinking_agent = Agent(
    name="Thinking Agent",
    role="Complex tasks requiring planning and reasoning",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[...],  # your tools
    reasoning=True,
)