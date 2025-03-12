#!/usr/bin/env python3

import typer
import json
import subprocess
import os
from pathlib import Path
from InquirerPy import prompt, inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import PathValidator

app = typer.Typer()
PROJECTS_FILE = Path(os.path.expanduser("~/.warpstart/projects.json"))

os.makedirs(PROJECTS_FILE.parent, exist_ok=True)

# Default project storage
if not PROJECTS_FILE.exists():
    PROJECTS_FILE.write_text(json.dumps({}, indent=4))

# Load projects
def load_projects():
    with open(PROJECTS_FILE, "r") as f:
        return json.load(f)

# Save projects
def save_projects(projects):
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f, indent=4)

@app.command()
def launcher():
    action = inquirer.select(
        message="What do you want to do?",
        choices=[
            "Open a project", 
            "Create a project",
            "Remove a project"
            ],
        default=None,
    ).execute()
    
    if action == "Open a project":
        open_project()
    elif action == "Create a project":
        create_project()
    elif action == "Remove a project":
        remove_project()

def open_project():
    projects = load_projects()
    
    if not projects:
        typer.echo("❌ No projects found. Create one first.")
        launcher()
        return

    project_name = inquirer.select(
        message="Select a project to open:",
        choices=[Choice(value=project) for project in projects.keys()],
        default=None,
    ).execute()

    project = projects[project_name]
    
    # Open applications
    for app in project["apps"]:
        print('Opening:', app)
        subprocess.Popen([app], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Run commands
    for cmd in project["commands"]:
        typer.echo(f"Running: {cmd}")
        subprocess.run(cmd, shell=True)

    typer.echo(f"\n✅ Project '{project_name}' launched successfully!\n")

def remove_project():
    projects = load_projects()
    project_name = inquirer.select(
        message="Select a project to remove:",
        choices=[Choice(value=project) for project in projects.keys()],
        default=None,
    ).execute()

    del projects[project_name]
    save_projects(projects)

    typer.echo(f"\n✅ Project '{project_name}' removed successfully!\n")
    launcher()

def create_project():
    commands = []
    # Get project name
    project_name = inquirer.text(message="Enter project name:").execute()

    # Get project path
    project_path = inquirer.filepath(
        message="Enter project path:",
        default="~/" if os.name == "posix" else "C:\\",
        validate=PathValidator(is_dir=True, message="Input is not a file"),
        only_directories=True,
    ).execute()
    project_path = os.path.expanduser(project_path)

    # Select multiple apps to open
    app_list = [
        "firefox",
        "code",
        "code workspace",
        "xfce4-terminal",
        "mongodb-compass",
        "postman",
        "thunar"
    ]
    apps = inquirer.checkbox(
        message="Select applications to open:",
        choices=app_list,
        validate=lambda result: len(result) >= 1,
        default=None,
    ).execute()

    if apps:
        if "code workspace" in apps:
            workspace_path = inquirer.filepath(
                message="Enter code workspace file path:",
                default=project_path,
                validate=PathValidator(is_file=True, message="Input is not a file"),
                only_files=True,
            ).execute()
            workspace_path = os.path.expanduser(workspace_path)
            apps[apps.index("code workspace")] = f"code {workspace_path}"
        if "firefox" in apps:
            firefox_url = inquirer.text(message="Enter URL to open in Firefox (optional):").execute()
            apps[apps.index("firefox")] = f"firefox {firefox_url}".strip()
        if project_path != '':
            if "thunar" in apps:
                apps[apps.index("thunar")] = f"thunar {project_path}"
            if "xfce4-terminal" in apps:
                apps[apps.index("xfce4-terminal")] = f"xfce4-terminal --working-directory={project_path}"
            if "code" in apps:
                apps[apps.index("code")] = f"code {project_path}"

    # Enter multiple commands to execute
    command_prompt = {
        "type": "input",
        "name": "commands",
        "message": "Enter commands to execute (comma-separated):"
    }
    commands.extend(prompt(command_prompt)["commands"].split(","))

    # Save project
    projects = load_projects()
    projects[project_name] = {"apps": apps, "commands": commands}
    save_projects(projects)

    typer.echo(f"\n✅ Project '{project_name}' created successfully!\n")

    launcher()

if __name__ == "__main__":
    app()
