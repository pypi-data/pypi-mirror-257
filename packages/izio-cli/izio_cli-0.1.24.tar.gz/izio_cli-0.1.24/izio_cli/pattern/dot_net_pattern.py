import os
from typer import Exit
from izio_cli.helper.console_helper import run_command
from izio_cli.helper.fs_helper import create_directory
from izio_cli.helper.project_helper import getNetCoreProjects, setupWorkflows

separator = "/" if os.name == "posix" else "\\"


def createNetCoreSolution(path, projectName, solution, console):
    with console.status(
        "Creating a new solution", spinner="arc", spinner_style="bold green"
    ) as status:
        """
        Create a new .NET Core solution with a specified structure.

        This function initializes a new .NET Core solution using the 'dotnet new sln' command and sets up various projects within the solution. It also adds cross references, Izio library, and creates submodules as necessary.

        Args:
        - path (str): The file system path where the new .NET Core solution should be created.
        - projectName (str): The name of the project.
        - solution (str): The solution name for the new .NET Core project.
        - console (Console): The Rich console object for displaying the status.

        Note:
        The function assumes a specific structure and naming convention for the .NET Core projects within the solution.
        """

        setupWorkflows(path, projectName, console)
        run_command(
            [
                "dotnet",
                "new",
                "sln",
                "-n",
                f"Be_{solution}.netCore.{projectName}",
            ],
            path=path,
        )
        status.stop()
        projects = getNetCoreProjects(projectName)
        status.start()
        if projects:
            status.update(
                status=f"Creating the following projects: {" ".join(projects)}",
            )
            createNetCoreProjects(path, projectName, projects)

            status.update(status="Adding cross references")
            addReferences(projectName, path)

            status.update(status="Adding BE_Izio.Core.Biblioteca")
            addIzioLib(projectName, path)

            status.update(status="Creating submodules")
            createSubmodules(path, projectName)
        else:
            Exit(code=0)


def createNetCoreProjects(path, projectName, projects):
    """
    Create .NET Core projects within a solution.

    This function iterates over a list of projects and creates each one using the 'dotnet new' command. It also adds each project to the solution file.

    Args:
    - path (str): The file system path where the projects should be created.
    - projectName (str): The name of the project.
    - projects (list): A list of project names to be created.
    """

    for project in projects:
        run_command(
            [
                "dotnet",
                "new",
                "webapi" if project == f"{projectName}.Api" else "classlib",
                "-n",
                f"{project}",
            ],
            path=path,
        )
        run_command(
            [
                "dotnet",
                "sln",
                "add",
                f"{project}" + separator + f"{project}.csproj",
            ],
            path=path,
        )


def addReferences(projectName, path):
    """
    Add project references in a .NET Core solution.

    This function sets up references between different projects in a .NET Core solution based on a predefined structure.

        - Api: ["Application", "Contracts", "Domain"],
        - Application: ["DataAccess", "Domain"],
        - DataAccess: ["Domain"],
        - Domain: ["Contracts"],

    Args:
    - projectName (str): The name of the main project.
    - path (str): The file system path where the projects are located.
    """

    referencies = {
        "Api": ["Application", "Contracts", "Domain"],
        "Application": ["DataAccess", "Domain"],
        "DataAccess": ["Domain"],
        "Domain": ["Contracts"],
    }
    for project, refs in referencies.items():
        for ref in refs:
            run_command(
                [
                    "dotnet",
                    "add",
                    f"{projectName}.{project}{separator}{projectName}.{project}.csproj",
                    "reference",
                    f"{projectName}.{ref}{separator}{projectName}.{ref}.csproj",
                ],
                path=path,
            )


def addIzioLib(projectName, path):
    """
    Add the Izio Library package to the DataAccess project in a .NET Core solution.

    This function adds the 'BE_Izio.Core.Biblioteca' package to the DataAccess project using the 'dotnet add package' command.

    Args:
    - projectName (str): The name of the main project.
    - path (str): The file system path where the DataAccess project is located.
    """
    run_command(
        [
            "dotnet",
            "add",
            f"{projectName}.DataAccess{separator}{projectName}.DataAccess.csproj",
            "package",
            "BE_Izio.Core.Biblioteca",
        ],
        path=path,
    )


def createSubmodules(path, projectName):
    """
    Create submodules for various projects in a .NET Core solution.

    This function creates a set of predefined submodules (directories) for different projects within the solution, such as Extensions, Services, DTOs, Validators, etc.

        ...Application/Extensions",
        ...Application/Services",
        ...Contracts/DTOs",
        ...Contracts/Validators",
        ...DataAccess/Services",
        ...Domain/Entities",
        ...Domain/Interfaces",
        ...Domain/Interfaces{separator}Business",
        ...Domain/Interfaces{separator}DataAccess",

    Args:
    - path (str): The file system path where the submodules should be created.
    - projectName (str): The name of the main project.
    """
    subMobules = [
        projectName + f".Application{separator}Extensions",
        projectName + f".Application{separator}Services",
        projectName + f".Contracts{separator}DTOs",
        projectName + f".Contracts{separator}Validators",
        projectName + f".DataAccess{separator}Services",
        projectName + f".Domain{separator}Entities",
        projectName + f".Domain{separator}Interfaces",
        projectName + f".Domain{separator}Interfaces{separator}Business",
        projectName + f".Domain{separator}Interfaces{separator}DataAccess",
    ]
    for sub in subMobules:
        create_directory(f"{path}{separator}{sub}")
