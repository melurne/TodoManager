import click
from tinydb import TinyDB, Query
db = TinyDB('db.json')
today = TinyDB('today.json')

daily = [   {  'title': 'Make the bed',
                'deadline': '10h00'
                },
            {   'title': 'Do the dishes',
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
                    'parent': 'master' if parent == None else parent},
                    'completed': False,
                    'repeatable': repeatable)

def resetDB(data) :
    data.truncate()

def initDB_with_daily() :
    Tasks_in_db = Query()
    for daily_task in daily :
        if db.search(Tasks_in_db.title == daily_task['title']) == [] :
            createTask(daily_task['title'], daily_task['deadline'], repeatable = True)

def schedule(task_title) :
    Tasks_in_db = Query()
    today.insert(db.search(Tasks_in_db.title == task_title))

def unschedule(task_title) :
    Tasks_in_db = Query()
    today.remove(Tasks_in_db.title == task_title)

def complete(task_title) :
    Tasks_in_db = Query()
    db.update({'completed': True}, Tasks_in_db.title == task_title && Tasks_in_db.repeatable == False)
    task = db.search(Tasks_in_db.title == task_title)
    print("You have successfully completed the task: {}".format(task_title))
    if task['reward'] != '' :
        click.echo("{1.bold}{1.yellow}You earned a reward! :{1.reset}{0['reward']}".format(task, ANSI))


def ListTasksToday() :
    for i,task in enumerate(today) :
        click.echo(u"{1.bold}#{2}{0['title']}{1.reset} <{0['deadline']}> {1.yellow}[{0['reward']}{1.reset}]\n
                {0['parent']}: {1.underline}$PATH = {0['path']}{1.reset}\n
                ".format(task, ANSI, i))

def ListeUncompleted() :
    Tasks_in_db = Query()
    for i,task in enumerate(db.search(Tasks_in_db.completed == False)) :
        click.echo(u"{1.bold}#{2}{0['title']}{1.reset} <{0['deadline']}> {1.yellow}[{0['reward']}{1.reset}]\n
                {0['parent']}: {1.underline}$PATH = {0['path']}{1.reset}\n
                ".format(task, ANSI, i))


def log(toLog #<class Task> || <class Goal>
        ) :
    if isinstance(toLog, Task):
        pass
    elif isinstance(toLog, Goal):
        pass


class Task() :
    TasksList = []
    def __init__(   self, 
                    title, 
                    deadline, 
                    path    =   None, 
                    reward  =   None,  
                    parent  =   None
                ) :
        self.title = title #str
        self.deadline = deadline #str 00h00
        self.path = path #str
        self.reward = reward #str
        self.parent = parent #<class Goal>
        TasksList.append(self)
        
    @staticmethod
    def display() :
        for task in Task.TasksList :
            print(task.pretify)

    def pretify(    self, 
                    oneline =   True
                ) :
        if oneline :
            return "{0.title} <{0.deadline}> (parent = {0.parent.pretify()})".format(self)
        else :
            return "{0.title} <{0.deadline}> (parent = {0.parent.pretify()})\n
                    \tpath = {0.path}\n".format(self)

    def complete(   self,
                ) :
        print("The task {0.title} has been completed\n")
        if self.reward != None :
            print("You have achieved the set reward : {0.reward}\n".format(self))
        log(self)
        TasksList.remove(self)

class Goal() :
    GoalsList[]
    def __init__(   self, 
                    title, 
                    path    =   None
                ) :
        self.title = title #str
        self.path = path #str
        GoalsList.append(self)

    @staticmethod
    def display() :
        for goal in GoalsList :
            print(goal.pretify)
    
    def pretify(    self, 
                    oneline =   True
                ) :
        if oneline :
            return "{0.title}".format(self)
        else :
            return "{0.title}\n
                    \tpath = {0.path}".format(self)
    
