import sqlite3 as sql


# создание базы
# не используется
def create_database():
    conn = sql.connect('telegramBotDatabase.db')
    print('Open database successfully')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE TASKS (ID INT NOT NULL, ID_USER INT NOT NULL, "
                 "MESSAGE TEXT, IMAGE TEXT, PRIMARY KEY (ID, ID_USER))")
    conn.commit()
    #print('created')


#create_database()

# добавление задачи
def add_elements(task):
    conn = sql.connect('telegramBotDatabase.db')
    print('Open database successfully')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO TASKS (ID, ID_USER, MESSAGE, IMAGE) VALUES (?,?,?,?)", task)
    conn.commit()


# list1 = ('1','2','something','NULL')
# add_elements(list1)

# удаление задачи
def delete_from_database(taskid):
    conn = sql.connect('telegramBotDatabase.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TASKS WHERE ID = ? AND ID_USER = ?", taskid)

    conn.commit()


# delete_from_database(idtask)


# вывод списка задач
def return_database(user):
    conn = sql.connect('telegramBotDatabase.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ID, MESSAGE, IMAGE FROM TASKS WHERE ID_USER = ?", (user,))
    rows = cursor.fetchall()
    # for row in rows:
    #    print(row)
    return rows

# номер задачи
def number_of_tasks(user):
    conn = sql.connect('telegramBotDatabase.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM TASKS WHERE ID_USER = ?", (user,))
    return str(cursor.fetchone()[0])

def photopath(taskid):
    conn = sql.connect('telegramBotDatabase.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT image FROM tasks WHERE id = ? AND id_user = ?", taskid)
    path = str(cursor.fetchone()[0])
    return path

def clear_database():
    conn = sql.connect('telegramBotDatabase.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TASKS")
    conn.commit()

#clear_database()