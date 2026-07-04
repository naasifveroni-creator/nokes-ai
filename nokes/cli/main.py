"""CLI entry point"""

import asyncio
from typing import Optional
import click
from loguru import logger
from nokes.core.engine import NokesEngine
from nokes.api.config import get_settings


class NokesInteractiveSession:
    """Interactive CLI session"""

    def __init__(self):
        settings = get_settings()
        self.engine = NokesEngine(
            llm_provider=settings.llm_provider,
            model=settings.llm_model,
        )
        self.running = True

    async def run(self):
        """Run interactive session"""
        click.echo("\n🤖 Welcome to Nokes AI")
        click.echo("Type 'help' for commands, 'exit' to quit\n")

        while self.running:
            try:
                user_input = click.prompt("You")

                if user_input.lower() == "exit":
                    self.running = False
                    click.echo("\nGoodbye!")
                    break
                elif user_input.lower() == "help":
                    self._show_help()
                elif user_input.lower() == "clear":
                    self.engine.clear_history()
                    click.echo("Conversation cleared.")
                elif user_input.lower() == "status":
                    self._show_status()
                else:
                    response = await self.engine.chat(user_input)
                    click.echo(f"\nNokes: {response.content}\n")

            except KeyboardInterrupt:
                click.echo("\n\nInterrupted. Type 'exit' to quit.")
            except Exception as e:
                click.echo(f"Error: {e}")
                logger.error(f"CLI error: {e}")

    def _show_help(self):
        """Show help information"""
        click.echo("\nCommands:")
        click.echo("  help    - Show this help message")
        click.echo("  clear   - Clear conversation history")
        click.echo("  status  - Show engine status")
        click.echo("  exit    - Exit the program")
        click.echo()

    def _show_status(self):
        """Show engine status"""
        stats = self.engine.memory.get_stats() if self.engine.memory else {}
        click.echo(f"\nConversation turns: {len(self.engine.conversation_history)}")
        if stats:
            click.echo(f"Memory documents: {stats.get('document_count', 0)}")
            click.echo(f"Memory usage: {stats.get('usage_percent', 0):.1f}%")
        click.echo()


@click.group()
def cli():
    """Nokes AI Command Line Interface"""
    logger.add(lambda msg: click.echo(msg.rstrip()), level="INFO")


@cli.command()
@click.option("--prompt", "-p", help="Prompt to send to Nokes")
def chat(prompt: Optional[str]):
    """Chat with Nokes"""
    if prompt:
        # Single message mode
        engine = NokesEngine()
        response = asyncio.run(engine.chat(prompt))
        click.echo(f"\nNokes: {response.content}\n")
    else:
        # Interactive mode
        session = NokesInteractiveSession()
        asyncio.run(session.run())


@cli.command()
@click.option("--text", "-t", required=True, help="Text to analyze")
@click.option("--type", "-T", default="general", help="Analysis type")
def analyze(text: str, type: str):
    """Analyze text"""
    engine = NokesEngine()
    result = asyncio.run(engine.analyze_text(text, type))
    click.echo(f"\nAnalysis Result:\n{result}\n")


@cli.command()
def info():
    """Show Nokes information"""
    from nokes import __version__

    click.echo(f"\nNokes AI v{__version__}")
    click.echo("Advanced AI Assistant System")
    click.echo("\nFor more info, visit: https://github.com/naasifveroni-creator/nokes-ai")
    click.echo()


if __name__ == "__main__":
    cli()
