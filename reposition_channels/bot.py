import hikari
import os
import dotenv

dotenv.load_dotenv()

DEBUG = False
bot = hikari.GatewayBot(os.getenv("TOKEN"), intents=hikari.Intents.ALL, logs="TRACE_HIKARI" if DEBUG else "INFO")


@bot.listen(hikari.StartingEvent)
async def register_commands(event: hikari.StartingEvent) -> None:
    """Register ping and info commands."""
    application = await bot.rest.fetch_application()

    commands = [
        bot.rest.slash_command_builder("test", "Test something"),
    ]

    await bot.rest.set_application_commands(application=application.id, commands=commands)

GUILD = 1366423901953069116
CATEGORY_1 = 1366423903198642187
CATEGORY_2 = 1368155982282096702
CHANNEL = 1368155748349247539

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
    print("started event running")
    builder = event.app.rest.reposition_channels(GUILD)
    await builder.add_reposition_channel(
        position=0,
        channel=CHANNEL,
        lock_permissions=False,
        parent=CATEGORY_1
    ).add_reposition_channel(
        position=0,
        channel=CHANNEL,
        lock_permissions=False,
        parent=CATEGORY_2
    )


if __name__ == "__main__":
    bot.run()
