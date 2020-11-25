# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# new_row = Table(string_field='This is string field!',
#          date_field=datetime.today())
# session.add(new_row)
# session.commit()



def menu_choice():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")

def day_name(day):
    days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    for key, name_of_day in days.items():
        if key == day:
            return name_of_day

def todays_tasks():
    today = datetime.today()
    # rows = session.query(Table).all()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()
    print("Today {} {}:".format(today.day, today.strftime('%b')))
    if len(rows) == 0:
        print("Nothing to do!")
    else:
        print(rows)


def weeks_tasks():
    today = datetime.today()
    print("")
    # rows = session.query(Table).filter(Table.deadline >= (today + timedelta(days=7))).all()
    # rows = session.query(Table).all()
    for x in range(7):
        print("{} {} {}:".format(day_name((today + timedelta(days=x)).weekday()), (today + timedelta(days=x)).day,
                                 (today + timedelta(days=x)).strftime('%b')))
        # print("check", (today + timedelta(days=x)).date())
        rows = session.query(Table).filter(Table.deadline == (today + timedelta(days=x)).date()).all()
        # print("rows", rows)
        for tasks in rows:
            print(tasks)
            if len(rows) == 0:
                print("Nothing to do!")
        print("")


def print_all_tasks():
    rows = session.query(Table).all()
    for tasks in rows:
        print(tasks.deadline)
        print(tasks)
        if len(rows) == 0:
            print("Nothing to do!")
    print("")


def add_task():
    new_row = []
    print("Enter task")
    new_task = input()
    print("Enter deadline")
    deadline = input()
    deadline = datetime.strptime(deadline, '%Y-%m-%d')
    new_row.append(Table(task=new_task,
                         deadline=deadline))
    session.add(new_row[-1])
    session.commit()
    print("The task has been added!")


def missed_tasks():
    print("Missed tasks:")
    #rows = session.query(Table).filter(Table.deadline < datetime.today()).all().order_by(Table.deadline)
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()

    #rows = session.query(Table).filter(Table.deadline < datetime.today()).all()
    if len(rows) != 0:
        for idx, x in enumerate(rows):
            print("{}. {}. {}".format(idx, x, x.deadline.strftime('%d %b')))
        print("")
    else:
        print("Nothing is missed!")

def delete_task():

    #rows = session.query(Table).filter(Table.deadline < datetime.today()).all()
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()

    print("Chose the number of the task you want to delete:")
    #print(rows)
    if len(rows) != 0:
        for idx, x in enumerate(rows):
            print("{}. {}. {}".format(idx+1, x, x.deadline.strftime('%d %b')))
        index_del = int(input())
        specific_row = rows[index_del-1]  # in case rows is not empty
        session.delete(specific_row)
        print("The task has been deleted!")
        session.commit()
    else:
        print("Nothing is missed!")

def main():

    menu_choice()
    while(True):
        choice = input()
        today = datetime.today()
        if choice == "1":
            todays_tasks()
            menu_choice()
        elif choice == "2":
            weeks_tasks()
            menu_choice()
        elif choice == "3":
            print_all_tasks()
            menu_choice()
        elif choice == "4":
            missed_tasks()
            menu_choice()
        elif choice == "5":
            add_task()
            menu_choice()
        elif choice == "6":
            delete_task()
            menu_choice()
        elif choice == "0":
            print("Bye!")
            break


main()

# 1) Today's tasks
# 2) Week's tasks
# 3) All tasks
# 4) Add task
# 0) Exit

# print("Today:")
# print("1) Do yoga")
# print("2) Make breakfast")
# print("3) Learn basics of SQL")
# print("4) Learn what is ORM")
