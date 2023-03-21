from email.policy import default
import click
from mrfmsim.configuration import MrfmSimLoader, MrfmSimDumper
from mrfmsim.experiment import Job
from mrfmsim.utility import job_execution
import yaml


@click.group()
@click.option("--expt", help="experiment file path")
@click.pass_context
def cli(ctx, expt):
    """Simple program that greets NAME for a total of COUNT times."""
    ctx.ensure_object(dict)
    with open(expt, "r") as f:
        experiment = yaml.load(f, Loader=MrfmSimLoader)
    ctx.obj["experiment"] = experiment


@cli.command()
@click.pass_context
@click.option("--view/--no-view", is_flag=True, default=True)
def show(ctx, view):
    """Draw experiment."""
    dot_graph = ctx.obj["experiment"].draw()
    dot_graph.render(view=view)


@cli.command()
@click.pass_context
def template(ctx):
    """Create a template job file based on the experiment."""
    experiment = ctx.obj["experiment"]
    job_template = [Job("", {k: "" for k in experiment.__signature__.parameters}, [])]
    click.echo(yaml.dump(job_template, Dumper=MrfmSimDumper, sort_keys=False))


@cli.command()
@click.pass_context
@click.option("--job", help="job file path")
def execute(ctx, job):
    """Execute the job."""
    experiment = ctx.obj["experiment"]

    with open(job, "r") as f:
        jobs = yaml.load(f, Loader=MrfmSimLoader)

    for job in jobs:
        # return the result to console
        click.echo(job_execution(experiment, job))
