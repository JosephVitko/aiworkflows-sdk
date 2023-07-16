import argparse
import os

from aiworkflows import AiWorkflowsApi, TaskCompiler


def main():
    parser = argparse.ArgumentParser(description='Deploy tasks from JSON files using the AI Workflows API.')

    subparsers = parser.add_subparsers(dest='command')

    deploy_parser = subparsers.add_parser('deploy', help='Deploy tasks from a directory or a single file.')
    deploy_parser.add_argument('path', type=str, help='Path to the directory or JSON file.')
    deploy_parser.add_argument('-r', '--recursive', action='store_true', help='Deploy tasks in subdirectories recursively.')

    args = parser.parse_args()

    api = AiWorkflowsApi()  # Provide necessary arguments
    compiler = TaskCompiler(api)

    if args.command == 'deploy':
        if os.path.isfile(args.path):
            compiler.deploy_task_from_json_file(args.path)
        elif os.path.isdir(args.path):
            compiler.deploy_json_tasks_from_directory(args.path, args.recursive)


if __name__ == "__main__":
    main()
