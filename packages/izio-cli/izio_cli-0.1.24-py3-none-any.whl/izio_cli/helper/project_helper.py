import os
import inquirer

from izio_cli.helper.strings_transformers import to_snake_case
from izio_cli.pattern.flutter_pattern import create_directory, create_file
from izio_cli.values.flutter_payloads import (
    flutterCIWorkflowPayload,
    pullRequestPayload,
)


def getPlatforms():
    result = inquirer.prompt(
        [
            inquirer.Checkbox(
                "platforms",
                message="Select the platforms",
                choices=[
                    "android",
                    "ios",
                    "web",
                    "windows",
                    "linux",
                    "macos",
                ],
                default=["android", "ios", "web"],
            )
        ]
    )

    platforms = ",".join(result["platforms"])
    return platforms


def getNetCoreProjects(projectName):
    return [
        f"{projectName}.Api",
        f"{projectName}.Application",
        f"{projectName}.Contracts",
        f"{projectName}.DataAccess",
        f"{projectName}.Domain",
    ]


separator = "/" if os.name == "posix" else "\\"


def getProjectPath(projectName, path=os.getcwd(), type="flutter", solution="IzPay"):
    path = (
        f"{path}{separator}Mb_{solution}.flutter.{projectName}"
        if type == "flutter"
        else f"{path}{separator}Be_{solution}.netCore.{projectName}"
    )
    confirm = inquirer.confirm(
        f"Do you want to create a new project in {path}", default=True
    )
    if not confirm:
        path = inquirer.prompt(
            [inquirer.Path("path", message="Enter the project path", default=path)]
        )["path"]
    return path


def getProjectName() -> tuple[bool, str]:
    projectName = to_snake_case(inquirer.text("Enter the project name"))
    confirm = inquirer.confirm(f"Your project name will be {projectName}", default=True)
    return (confirm, projectName)


def setupWorkflows(path, projectName, console):
    console.print("Creating pull request template")
    create_directory(
        path,
    )
    create_directory(
        f"{path}{separator}.github",
    )
    console.print("Creating continuous integration workflow")
    create_directory(
        f"{path}{separator}.github{separator}workflows",
    )
    create_file(
        f"{path}{separator}.github",
        filename="pull_request_template.md",
        payload=pullRequestPayload(projectName),
    )
    create_file(
        f"{path}{separator}.github{separator}workflows",
        filename="continuous-integration.yml",
        payload=flutterCIWorkflowPayload(projectName),
    )
