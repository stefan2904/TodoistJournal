from datetime import datetime
from datetime import date
import todoist
import os


API_TOKEN = os.getenv('API_TOKEN')

api = todoist.TodoistAPI(API_TOKEN)
status = api.sync()

if 'error' in status:
    print(status)
    exit()


def main():
    relevant_dates = [date.today()]

    for date_filter in relevant_dates:
        print('# ' + date_filter.strftime('%d. %b %Y'))
        print_for_date(date_filter)


def print_for_date(date_filter):
    for project in api.state['projects']:
        print('### ' + project['name'])

        tasks_by_project(project['id'], date_filter)


def tasks_by_project(project_id, date_filter):
    # open_tasks = api.projects.get_data(project['id'])
        # for task in open_tasks['items']:
        #     print_task(task)

    completed_tasks = api.items.get_completed(project_id)
    for task in completed_tasks:
        print_task(task, date_filter)


def print_task(task, date_filter):
    content = task['content']
    date_completed = task['date_completed']

    if(date_completed is None):
        prefix = " - [ ]"
        suffix = ""
    else:
        date_completed = datetime.strptime(
            date_completed, "%Y-%m-%dT%H:%M:%SZ").date()
        is_relevant = date_completed == date_filter
        prefix = " - [X]"
        suffix = "({})".format(date_completed.strftime('%d. %b %Y'))

    if is_relevant:
        print("{} {} {}".format(prefix, content, suffix))


if __name__ == '__main__':
    main()
