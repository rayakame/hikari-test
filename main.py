import asyncio
import os

import hikari
import dotenv
from utils import calculate_waveform
dotenv.load_dotenv()

DEBUG = False
bot = hikari.GatewayBot(os.getenv("TOKEN"), intents=hikari.Intents.ALL, logs="TRACE_HIKARI" if DEBUG else "INFO")

@bot.listen(hikari.StartingEvent)
async def register_commands(event: hikari.StartingEvent) -> None:
    """Register ping and info commands."""
    application = await bot.rest.fetch_application()

    commands = [
        bot.rest.slash_command_builder("audio", "Get the bot's latency."),
        bot.rest.slash_command_builder("test", "Get the bot's latency."),
    ]

    await bot.rest.set_application_commands(application=application.id, commands=commands)

@bot.listen(hikari.InteractionCreateEvent)
async def handle_interactions(event: hikari.InteractionCreateEvent) -> None:
    """Listen for slash commands being executed."""
    if not isinstance(event.interaction, hikari.CommandInteraction):
        # only listen to command interactions, no others!
        return

    if event.interaction.command_name == "audio":
        waveform, length = calculate_waveform("./sample2.wav")
        await event.app.rest.create_interaction_response(
            interaction=event.interaction,
            token=event.interaction.token,
            response_type=hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
            flags=hikari.MessageFlag.EPHEMERAL
        )
        await asyncio.sleep(5)
        await event.app.rest.edit_interaction_voice_message_response(
            application=event.interaction.application_id,
            token=event.interaction.token,
            attachment=hikari.File("./sample2.wav"),
            waveform=waveform,
            duration=length
        )
    if event.interaction.command_name == "test":
        await event.app.rest.create_interaction_response(
            interaction=event.interaction,
            token=event.interaction.token,
            response_type=hikari.ResponseType.DEFERRED_MESSAGE_CREATE,
            flags=hikari.MessageFlag.EPHEMERAL
        )
        await asyncio.sleep(5)
        await event.app.rest.edit_interaction_response(
            application=event.interaction.application_id,
            token=event.interaction.token,
            content="test"
        )

@bot.listen(hikari.events.MessageCreateEvent)
async def on_message(event: hikari.events.MessageCreateEvent):
    if event.message.content is None and len(event.message.attachments) == 1 and event.message.attachments[0].waveform is not None and not event.author.is_bot:
        await event.app.rest.create_voice_message(
            channel = event.channel_id,
            attachment=event.message.attachments[0],
            waveform=event.message.attachments[0].waveform,
            duration=event.message.attachments[0].duration
        )
        return
    if not event.message.content:
        return
    if event.message.content.startswith("!test"):
        component = event.app.rest.build_message_action_row().add_interactive_button(
            hikari.ButtonStyle.PRIMARY,
            "custom_button_id",
            label="test"
        )
        await event.message.respond(
            "Test Button",
            component=component
        )
    if event.message.content.startswith("!audio"):
        waveform, length = calculate_waveform("./sample2.wav")
        await event.message.respond(
            waveform + " " + str(length)
        )
        await event.app.rest.create_voice_message(
            channel=event.channel_id,
            attachment=hikari.File("./sample2.wav"),
            waveform=waveform,
            duration=length
        )
"""@bot.listen(hikari.events.InteractionCreateEvent)
async def test_normal_interaction_event(event: hikari.events.InteractionCreateEvent):
    print(event)

@bot.listen(hikari.events.ComponentInteractionCreateEvent)
async def test_component_interaction_event(event: hikari.events.ComponentInteractionCreateEvent):
    print(event)"""

if __name__ == "__main__":
    bot.run()
