from datetime import datetime
from datetime import date
import todoist
import os


relevant_dates = [date.today()]
ignore_projects = [2222391662, 2222026062]

API_TOKEN = os.getenv('API_TOKEN')

###############################################################################

api = todoist.TodoistAPI(API_TOKEN)
status = api.sync()

if 'error' in status:
    print(status)
    exit()


def main():

    for date_filter in relevant_dates:
        print('# ' + date_filter.strftime('%d. %b %Y (%a)'), end='\n\n')
        print_tasks_by_date(date_filter)
        print('', end='\n')
        print('---', end='\n\n')


def print_tasks_by_date(date_filter):
    def task_filter(t): return is_task_relevant(t, date_filter)

    for project in api.state['projects']:
        if project['id'] in ignore_projects:
            continue

        tasks = get_tasks_by_project(project['id'])
        tasks = list(filter(task_filter, tasks))

        if tasks is not None and len(tasks) > 0:
            print(
                '### ' +
                append_parent_name(
                    project['parent_id'],
                    project['name']))
            print_tasks(tasks)
            print('', end='\n')


def append_parent_name(parent_id, name):
    if parent_id is not None:
        parent = api.projects.get_by_id(parent_id)
        prefix = "{} -> ".format(parent['name'])
        return append_parent_name(parent['parent_id'], prefix + name)
    else:
        return name


def get_tasks_by_project(project_id):
    return api.items.get_completed(project_id)


def is_task_relevant(task, date_filter):
    date_completed = datetime.strptime(
        task['date_completed'],
        "%Y-%m-%dT%H:%M:%SZ").date()
    return date_filter is None or date_completed == date_filter


def print_tasks(tasks):
    for task in tasks:
        print_task(task)


def print_task(task):
    content = task['content'].strip()
    prefix = " - [X]"
    print("{} {}".format(prefix, content))


if __name__ == '__main__':
    main()
