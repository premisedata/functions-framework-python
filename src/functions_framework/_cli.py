# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

import click

from functions_framework import create_app
from functions_framework._http import create_server


@click.command()
@click.option("--target", envvar="FUNCTION_TARGET", type=click.STRING, required=True)
@click.option("--source", envvar="FUNCTION_SOURCE", type=click.Path(), default=None)
@click.option(
    "--signature-type",
    envvar="FUNCTION_SIGNATURE_TYPE",
    type=click.Choice(["http", "event", "cloudevent"]),
    default="http",
)
@click.option("--host", envvar="HOST", type=click.STRING, default="0.0.0.0")
@click.option("--port", envvar="PORT", type=click.INT, default=8080)
@click.option("--debug", envvar="DEBUG", is_flag=True)
@click.option("--dry-run", envvar="DRY_RUN", is_flag=True)
@click.option("--options", "-o", envvar="OPTIONS", multiple=True, default=[])
def _cli(target, source, signature_type, host, port, debug, dry_run, options):
    app = create_app(target, source, signature_type)
    if dry_run:
        click.echo("Function: {}".format(target))
        click.echo("URL: http://{}:{}/".format(host, port))
        click.echo("Dry run successful, shutting down.")
    else:
        server_options = {
            option.split(":")[0]: option.split(":")[1] for option in options
        }
        create_server(app, debug, **server_options).run(host, port)