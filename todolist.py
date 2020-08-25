# Write your code here

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from datetime import datetime, timedelta,date
import calendar

engine=create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.string_field

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def add_task(task,deadline):
    new_row = Table(task=task,deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
    session.add(new_row)
    session.commit()

def printTasks():
    today=datetime.today()
    rows = session.query(Table).filter(Table.deadline == today).all()
    day=today.day
    month=today.strftime('%b')
    print(f'Today: {day} {month}:')
    if rows:
        for idx, row in enumerate(rows):
            print(f'{idx}. {row.task}')
    else:
        print('Nothing to do!\n')

def week_tasks():
    today=datetime.today()
    for i in range(7):
        thisday=today+timedelta(days=i)
        weekday=calendar.day_name[thisday.weekday()]
        day=thisday.day
        month=thisday.strftime('%b')
        rows = session.query(Table).filter(Table.deadline == thisday.date()).all()
        print(weekday,day,month)
        if rows:
            for idx,row in enumerate(rows):
                print(f'{idx+1}. {row.task}\n')
        else:
            print('Nothing to do!\n')
def all_tasks():
    rows=session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    for idx,row in enumerate(rows):
        ddate=row.deadline
        day=ddate.day
        month=ddate.strftime('%b')
        print(f'{idx+1}. {row.task}. {day} {month}')

def missed_tasks():
    rows=session.query(Table).filter(Table.deadline<datetime.today().date())\
        .order_by(Table.deadline).all()
    print("Missed tasks:")
    if rows:
        for idx,row in enumerate(rows):
            ddate=row.deadline
            day=ddate.day
            month=ddate.strftime('%b')
            print(f'{idx+1}. {row.task}. {day} {month}')
    else:
        print("Nothing is missed!")
    print("\n")
    return rows

def delete_task():
    rows=session.query(Table).order_by(Table.deadline).all()
    if rows:
        print("Choose the number of the task you want to delete:")
        for idx,row in enumerate(rows):
            ddate=row.deadline
            day=ddate.day
            month=ddate.strftime('%b')
            print(f'{idx+1}. {row.task}. {day} {month}')
    else:
        print("Nothing to delete\n")
        return

    num=int(input())
    spec_row=rows[num-1]
    session.delete(spec_row)
    session.commit()
    print("The task has been deleted!\n")

while True:
    print("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) MIssed tasks"
          "\n5) Add task\n6) Delete task\n0) Exit")
    choice=input()
    if choice=='0':
        print('Bye!')
        break
    if choice=='5':
        newtask=input('Enter task\n')
        newdeadline=input('Enter deadline\n')
        add_task(newtask,newdeadline)
        print('The task has been added!\n')
    if choice=='1':
        printTasks()
    if choice=='2':
        week_tasks()
    if choice=='3':
        all_tasks()
    if choice=="4":
        missed_tasks()
    if choice=='6':
        delete_task()
