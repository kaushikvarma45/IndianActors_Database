# CREATE DATABASE USING THE ACTORS PICTURES AND TEXT FILES

import sqlite3
import os
import pandas as pd

def create_database(name, image, text):
    conn = sqlite3.connect("ActorsData.db")
    cursor = conn.cursor()

    with open(image,'rb') as f:
        data = f.read()
    with open(text, 'rb') as p:
        data2 = p.read()
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS my_table 
       (name TEXT,image BLOP,text BLOP)""")

    cursor.execute(""" INSERT INTO my_table 
       (name, image, text) VALUES (?,?,?)""", (name, data, data2))

    conn.commit()
    cursor.close()
    conn.close()

def fetch_data():

    os.chdir("/Users/kaushikvarma/PycharmProjects/test")
    conn = sqlite3.connect("ActorsData.db")
    cursor = conn.cursor()

    data = cursor.execute("""SELECT * FROM my_table""")
    for x in data.fetchall():

        with open("{}.jpg".format(x[0]),"wb") as f:
            f.write(x[1])
        with open("{}.txt".format(x[0]), "wb") as p:
            p.write(x[2])
    conn.commit()
    cursor.close()
    conn.close()


def main(input):

    if input == 1:
        data = pd.read_csv('actorList.csv')
        names = data.values.tolist() #list of lists
        print(names)
        os.chdir("/Users/kaushikvarma/PycharmProjects/test")
        for i in names:
            create_database(i[0],i[0]+'.jpg',i[0]+'.txt')
    elif input == 2:
        fetch_data()
    else:
        print("WRONG INPUT")


if __name__ == "__main__":
    main(2)  #1 to create database and 2 to fetch data from database Make sure directories are maintained same


