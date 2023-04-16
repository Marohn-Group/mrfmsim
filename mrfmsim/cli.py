import click
from mrfmsim.configuration import MrfmSimLoader, MrfmSimDumper
from mrfmsim.utils import Job, job_execution
from mrfmsim.plugin import load_plugin, list_plugins, SUBMODULES
import importlib
import yaml
import sys


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--exp-file",
    type=click.Path(exists=True),
    default=None,
    help="Load experiment by file path.",
)
@click.option(
    "--plugin", multiple=True, default=None, required=False, help="Load a plugin."
)
@click.option("--attr", multiple=True, default=SUBMODULES, help="Load a submodule.")
@click.option("--exp", type=str, default=None, help="Load experiment by name.")
def cli(ctx, exp_file, plugin, attr, exp):
    """MRFM simulation tool."""

    if ctx.invoked_subcommand is None:
        if any([exp_file, exp, plugin]):
            raise click.UsageError("No commands are given.")
        click.echo(ctx.get_help())
    else:
        ctx.ensure_object(dict)
        if exp_file and exp:
            raise click.BadOptionUsage(
                "exp-file", "Cannot use both exp-file and exp options."
            )
        elif exp_file:
            with open(exp_file, "r") as f:
                experiment = yaml.load(f, Loader=MrfmSimLoader)
            ctx.obj["experiment"] = experiment
        elif exp:
            load_plugin(plugin, attr)
            experiment_module = sys.modules["mrfmsim.experiment"]
            ctx.obj["experiment"] = getattr(experiment_module, exp)


@cli.command()
@click.pass_context
@click.option("--view/--no-view", is_flag=True, default=True)
def draw(ctx, view):
    """Draw experiment graph."""
    dot_graph = ctx.obj["experiment"].draw()
    dot_graph.render(view=view)


@cli.command()
@click.pass_context
def show(ctx):
    """Show experiment metadata."""
    dot_graph = ctx.obj["experiment"]
    click.echo(dot_graph)


@cli.command()
@click.pass_context
def template(ctx):
    """Create a template job file based on the experiment."""
    experiment = ctx.obj["experiment"]
    job_template = [Job("", {k: "" for k in experiment.__signature__.parameters}, [])]
    click.echo(yaml.dump(job_template, Dumper=MrfmSimDumper, sort_keys=False))


@cli.command()
@click.pass_context
@click.option("--job", help="The job file path.")
def execute(ctx, job):
    """Execute the job file, use --job for the job file path."""
    experiment = ctx.obj["experiment"]

    with open(job, "r") as f:
        jobs = yaml.load(f, Loader=MrfmSimLoader)

    for job in jobs:
        # return the result to the console
        click.echo(job_execution(experiment, job))


@cli.command("list-plugins")
@click.option("--plugin", multiple=True, default=None, help="Load a plugin.")
@click.option("--attr", multiple=True, default=SUBMODULES, help="Load a submodule.")
def show_plugs(plugin, attr):
    """List all available plugins."""

    load_plugin(plugin, attr)
    for att in attr:
        list_plugins(att)


# @click.group()
# @click.option("--plugin", help="load plugins")
# @click.pass_context
# def exp(ctx, exp):
#     """Load experiment."""
#     ctx.obj["experiment"] = importlib.import_module(f"mrfmsim.experiment.{exp}")

# @click.command()
# @click.option("--plugin", help="load plugins")
# def plugin(plugins, attrs=["experiment", "component", "shortcut", "modifier"]):
#     """Load plugins."""
#     load_plugin(plugins, attrs)

# cli = click.CommandCollection(sources=[exp_file, exp])
