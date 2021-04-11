import click
from tinydb import TinyDB, Query
db = TinyDB('db.json')
today = TinyDB('today.json')

daily = [   {  'title': 'make the bed',
                'deadline': '10h00'
                },
            {   'title': 'do the dishes',
                'deadline': '18h00'
                }
        ]

class ANSI:
    bold = '\u001b[1m'
    underline = '\u001b[4m'
    back_black = '\u001b[40m'
    back_red = '\u001b[41m'
    back_green = '\u001b[42m'
    back_yellow = '\u001b[43m'
    back_blue = '\u001b[44m'
    back_magenta = '\u001b[45m'
    back_cyan = '\u001b[46m'
    back_white = '\u001b[47m'
    black = '\u001b[30m'
    red = '\u001b[31m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    blue = '\u001b[34m'
    magenta = '\u001b[35m'
    cyan = '\u001b[36m'
    white = '\u001b[37m'
    reset = '\u001b[0m'

@click.group()
def cli() :
    """Todo application"""
    pass

@cli.command()
@click.argument("title", required=True, type=str)
@click.argument("deadline", required=True, type=str)
@click.option("-p", "--path", "path", required = False, type=str, help = "Path to the project")
@click.option("-r", "--reward", "path", required = False, type=str, help = "Reward for completing the task")
@click.option("--parent", "parent", required = False, type=str, help = "Parent project")
@click.option("--repeatable", "repeatable", required = False, type=bool, help = "Flag for task repeatability")
def createTask( title,
                deadline,
                path = None,
                reward = None,
                parent = None,
                repeatable = False
                ) :
    db.insert({  'title': title,
                    'deadline': deadline,
                    'path': '' if path == None else path,
                    'reward': '' if reward == None else reward,
                    'parent': 'master' if parent == None else parent,
                    'completed': False,
                    'repeatable': repeatable})

@cli.command()
def resetDB() :
    db.truncate()

@cli.command()
def initDBwithdaily() :
    Tasks_in_db = Query()
    for daily_task in daily :
        if db.search(Tasks_in_db.title == daily_task['title']) == [] :
            createTask(daily_task['title'], daily_task['deadline'], repeatable = True)

@cli.command()
@click.argument("task_title", required=True, type=str)
def schedule(task_title) :
    Tasks_in_db = Query()
    today.insert(db.search(Tasks_in_db.title == task_title)[0])

@cli.command()
@click.argument("task_title", required=True, type=str)
def unschedule(task_title) :
    Tasks_in_db = Query()
    today.remove(Tasks_in_db.title == task_title)

@cli.command()
@click.argument("task_title", required=True, type=str)
def complete() :
    Tasks_in_db = Query()
    db.update({'completed': True}, (Tasks_in_db.title == task_title)and(Tasks_in_db.repeatable == False))
    task = db.search(Tasks_in_db.title == task_title)
    click.echo("You have successfully completed the task: {}".format(task_title))
    if task['reward'] != '' :
        click.echo("{1.bold}{1.yellow}You earned a reward! :{1.reset}{0[reward]}".format(task, ANSI))

@cli.command()
def ListTasksToday() :
    for i,task in enumerate(today) :
        click.echo(u"{1.bold}#{2}: {0[title]}{1.reset} <{0[deadline]}> {1.yellow}[{0[reward]}]{1.reset}\n{0[parent]}: {1.underline}$PATH = {0[path]}{1.reset}\n".format(task, ANSI, i))

@cli.command()
def ListeUncompleted() :
    Tasks_in_db = Query()
    for i,task in enumerate(db.search(Tasks_in_db.completed == False)) :
        click.echo(u"{1.bold}#{2}: {0[title]}{1.reset} <{0[deadline]}> {1.yellow}[{0[reward]}]{1.reset}\n{0[parent]}: {1.underline}$PATH = {0[path]}{1.reset}\n".format(task, ANSI, i))

@cli.command()
def startday() :
    today.truncate()
    Tasks_in_db = Query()
    for daily_task in daily :
        today.insert(db.search(Tasks_in_db.title == daily_task['title'])[0])
