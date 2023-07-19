#!/usr/bin/env python3

import argparse
import os
import logging
from datetime import datetime

import dotenv
from aiworkflows import AiWorkflowsApi, TaskCompiler


def setup_logging(verbose):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=level)


def configure(args):
    api_key = args.api_key or os.getenv('AIWORKFLOWS_API_KEY')
    if not api_key:
        logging.error("You must provide an API key to configure.")
        return

    # check if the .env file exists
    if not os.path.isfile('.env'):
        logging.info(f"No .env file found. Creating one at {os.getcwd()} to store the API key.")
        with open('.env', 'w') as f:
            f.write('')

    try:
        dotenv.set_key('.env', 'AIWORKFLOWS_API_KEY', api_key)
        logging.info("API key successfully configured.")
    except Exception as e:
        logging.error(f"An error occurred while writing the API key to .env file: {str(e)}")


def deploy(args):
    logging.info(f"Deploying tasks from {args.path} at {str(datetime.now())}")
    try:
        api_key = dotenv.get_key('.env', 'AIWORKFLOWS_API_KEY')
        api = AiWorkflowsApi(api_key=api_key)
        compiler = TaskCompiler(api)

        if os.path.isfile(args.path):
            compiler.deploy_task_from_json_file(args.path)
            logging.info(f"Task from {args.path} has been successfully deployed.")
        elif os.path.isdir(args.path):
            compiler.deploy_json_tasks_from_directory(args.path, args.recursive)
            logging.info(f"Tasks from {args.path} have been successfully deployed.")
        else:
            logging.error(f"{args.path} is neither a valid file nor directory.")
    except FileNotFoundError:
        logging.error("No .env file found. Please configure API key first.")
    except Exception as e:
        logging.error(f"An error occurred while deploying tasks: {str(e)}")


def main():
    parser = argparse.ArgumentParser(prog='aiworkflows', description='AI Workflows CLI')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_configure = subparsers.add_parser('configure', help='Configure the API key')
    parser_configure.add_argument('-k', '--api_key', type=str, help='The API key to be used. Can also be set via the AIWORKFLOWS_API_KEY environment variable')
    parser_configure.set_defaults(func=configure)

    parser_deploy = subparsers.add_parser('deploy', help='Deploy AI tasks')
    parser_deploy.add_argument('path', type=str, help='Path to either a directory to deploy tasks from or a JSON file to deploy task from')
    parser_deploy.add_argument('-r', '--recursive', action='store_true', help='Whether to deploy tasks in subdirectories')
    parser_deploy.set_defaults(func=deploy)

    args = parser.parse_args()

    setup_logging(args.verbose)

    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
