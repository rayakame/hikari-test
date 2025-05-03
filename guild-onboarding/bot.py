import os
import hikari
import hikari.guilds
import hikari.impl.special_endpoints
import dotenv

dotenv.load_dotenv()

DEBUG = False
bot = hikari.GatewayBot(os.getenv("TOKEN"), intents=hikari.Intents.ALL, logs="TRACE_HIKARI" if DEBUG else "INFO")
GUILD_ID = int(os.getenv("GUILD_ID"))

@bot.listen(hikari.StartingEvent)
async def register_commands(event: hikari.StartingEvent) -> None:
    """Register ping and info commands."""
    application = await bot.rest.fetch_application()

    commands = [
        bot.rest.slash_command_builder("test", "Test something"),
    ]

    await bot.rest.set_application_commands(application=application.id, commands=commands)

DEFAULT_CHANNELS = [
1368194536043446374,
1368194556025241610,
1368194575696400477,
1368194597573890188,
1368194617077403688,
1368194704859992157,
1368194725110087701
]

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
    print("started event running")
    guild_onboarding = await event.app.rest.fetch_guild_onboarding(GUILD_ID)
    print(guild_onboarding)
    await event.app.rest.edit_guild_onboarding(
        GUILD_ID,
        default_channel_ids=DEFAULT_CHANNELS,
        mode=hikari.guilds.GuildOnboardingMode.ONBOARDING_DEFAULT,
        enabled=False,
        prompts=[
            hikari.impl.special_endpoints.GuildOnboardingPromptBuilder("Test Prompt", single_select=True,required=True,in_onboarding=True).add_option(
                "Test Option",
                role_ids=[1368200174077214720],
                description="Test Description",
            ).add_option(
                "Test Option 2",
                role_ids=[1368200174077214720],
                description="Test Description 2",
            )
        ]
    )


if __name__ == "__main__":
    bot.run()
