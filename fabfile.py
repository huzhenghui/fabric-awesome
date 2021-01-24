import json
import os
import platform
import sys

from fabric import task
from invoke.context import Context
from invoke.runners import Result


@task
def fabric_choose(c):
    context : Context = c
    result : Result = context.run("fab --list --list-format=json | jq '.tasks[].name' | /usr/local/opt/choose-gui/bin/choose")
    print("\nChoose Recipe: ", result.stdout)
    context.run("fab " + result.stdout)

@task
def fabric_fzf(c):
    context: Context = c
    result : Result = context.run('pwsh -c "fab --list --list-format=json | ConvertFrom-Json | Select-Object -ExpandProperty tasks | Select-Object -ExpandProperty name | fzf"', env=os.environ)
    print("\nChoose Recipe: ", result.stdout)
    context.run("fab " + result.stdout)

@task
def unknown_os(c):
    print("Unknown OS : ", platform.system())

@task(default=True)
def default_task(c):
    os_default : dict = {
        'Darwin' : fabric_choose,
        'Windows' : fabric_fzf
    }
    os_default.get(platform.system(), unknown_os)(c)

@task
def fabric_list(c):
    context: Context = c
    context.run("fab --list")

@task
def fabric_list_nested(c):
    context: Context = c
    context.run("fab --list --list-format=nested")

@task
def fabric_list_json(c):
    context: Context = c
    context.run("fab --list --list-format=json | jq")

def get_fabric_draft_dir(c : Context):
    context: Context = c
    result : Result = context.run("jump cd fabric-draft", hide="stdout")
    return result.stdout

@task
def fabric_draft_dir(c):
    print(get_fabric_draft_dir(c))

@task
def code(c):
    cwd = os.getcwd()
    workspace = cwd + "/fabric.code-workspace"
    if os.path.exists(workspace):
        c.run("code " + workspace)
    else:
        c.run("code " + cwd)

@task
def executable(c):
    print(sys.executable)

@task
def vscode_settings(c):
    settings : dict = {
        "python.pythonPath" : sys.executable
    }
    print(json.dumps(settings))
