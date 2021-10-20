import sqlite3
from datetime import datetime
from sqlite3 import Error
from flask import Flask, redirect, request, render_template, session, jsonify, json
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE = r'mhs.db'

def create_connection(db_file):
    # Create a database connection to a SQLite database
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
        return d

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

 
@app.route('/')
def index():

    sql_create_teams_table = """ CREATE TABLE IF NOT EXISTS teams (
                                    id integer primary key,
                                    team text,
                                    mascot text,
                                    location text
                                ); """

    sql_create_schedule_table = """ CREATE TABLE IF NOT EXISTS schedule (
                                    id integer primary key,
                                    team_home_id integer,
                                    team_home text,
                                    team_away_id integer,
                                    team_away text,
                                    team_home_location text,
                                    completed boolean,
                                    score text
                                ); """

    conn = create_connection(DATABASE)
    if conn is not None:
        # Create tables
        create_table(conn, sql_create_teams_table)
        create_table(conn, sql_create_schedule_table)
        conn.commit()
    else:
        print("Error! Cannot create the database connection.")

    
    con = sqlite3.connect('mhs.db')
    con.row_factory = sqlite3.Row

    get_schedule = con.cursor()
    get_schedule = get_schedule.execute("select * from schedule order by 'game_date' ASC")
    schedule = get_schedule.fetchall()

    return render_template('schedule.html', schedule=schedule)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/roster')
def roster():
    return render_template('roster.html')