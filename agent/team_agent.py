team = Team(
    name="Smart Router",
    mode=TeamMode.route,
    model=OpenAIResponses(id="gpt-5.2"),
    members=[fast_agent, thinking_agent],
    instructions=[
        "Analyze the user's request complexity.",
        "Simple/direct questions -> Fast Agent",
        "Complex tasks needing planning -> Thinking Agent",
    ],
    show_members_responses=True,
)