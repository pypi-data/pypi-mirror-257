import subprocess

import click
from loguru import logger


def check_node_installed():
    try:
        result = subprocess.run(
            ["node", "--version"], check=True, stdout=subprocess.PIPE, text=True
        )
        version = result.stdout.strip().replace("v", "")
        if int(version.split(".")[0]) < 18:
            raise click.ClickException(
                f"Node.js version {version} is not supported. Please install Node.js 18 or later."
            )
    except FileNotFoundError:
        raise click.ClickException(
            "Node.js is not installed. Please install Node.js 18 or later."
        )


def run_sca(
    project_root: str,
    emitter_file_path: str,
    emitter_function: str,
    emitter_payload_parameter: str,
    event_name_key: str,
):
    try:
        cmd = [
            "npx",
            "-y",
            "-q",
            "@gable-eng/sca",
            "python",
            project_root,
            "--emitter-file-path",
            emitter_file_path,
            "--emitter-function",
            emitter_function,
            "--emitter-payload-parameter",
            emitter_payload_parameter,
            "--event-name-key",
            event_name_key,
        ]
        logger.debug(" ".join(cmd))
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            logger.debug(result.stderr)
            raise click.ClickException(f"Error running Gable SCA: {result.stderr}")
        logger.debug(result.stdout)
        logger.debug(result.stderr)
        # The sca CLI prints the results to stdout,and everything else to trace/warn/debug/error
        return result.stdout
    except Exception as e:
        logger.opt(exception=e).debug("Error running Gable SCA")
        raise click.ClickException(
            "Error running Gable SCA: Please ensure you have the @gable-eng/sca package installed."
        )
