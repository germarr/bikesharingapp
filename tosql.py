import psycopg2
import psycopg2.extras
import csv
import pandas as pd
from datetime import datetime, timedelta
import json

def mainsql():
    dateforfile = get_date()
    #dateforfile="df_9_2_2021"
    new_youtube_table(date=dateforfile)
    arrange_file(datefile=dateforfile)
    push_data_to_table(datefile=dateforfile)
    print("ALL CREATED!")

def get_date():
    today = datetime.today()

    todayasstring = f"df_{today.month}_{today.day}_{today.year}"
    print(todayasstring)
    return todayasstring

def new_youtube_table(date):
    conn = psycopg2.connect("host=34.220.116.144 port=5432 dbname=apidata user=gmarr password=MTia100%s2021!!")
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE {date}(
            video_id text PRIMARY KEY,
            channel_id text,
            channel_thumbnail text,
            publishedAT date,
            title text,
            viewCount NUMERIC,
            likeCount NUMERIC,
            dislikeCount NUMERIC,
            commentCount NUMERIC,
            thumbnail text,
            link text,
            video_lang text,
            categoryId NUMERIC,
            channel_title text,
            published_videos NUMERIC,
            channel_subs NUMERIC,
            birth_of_channel date,
            country_of_the_channel text,
            category_title text,
            country text,
            AR NUMERIC, 
            AU NUMERIC, 
            BO NUMERIC, 
            BR NUMERIC,
            CA NUMERIC, 
            CL NUMERIC, 
            CO NUMERIC, 
            CR NUMERIC, 
            DE NUMERIC, 
            EC NUMERIC, 
            ES NUMERIC, 
            FR NUMERIC, 
            GB NUMERIC,
            INDIA NUMERIC, 
            IT NUMERIC, 
            JP NUMERIC,
            KR NUMERIC, 
            MX NUMERIC, 
            PE NUMERIC,
            PT NUMERIC, 
            US NUMERIC, 
            UY NUMERIC, 
            sum_of_countries NUMERIC
        )
        """)

    conn.commit()
    print("Table Created!")

def arrange_file(datefile):
    testfile = pd.read_csv(f"./db/{datefile}.csv")
    v3 = testfile[["video_id","channel_id","channel_thumbnail","publishedAt","title","viewCount","likeCount","dislikeCount","commentCount","thumbnail","link","video_lang","categoryId","channel_title","published_videos","channel_subs","birth_of_channel","country_of_the_channel","category_title","country","AR","AU","BO","BR","CA","CL","CO","CR","DE","EC","ES","FR","GB","IN","IT","JP","KR","MX","PE","PT","US","UY","sum_of_countries"]].set_index("video_id").fillna(0)
    v3["title"] = [i.replace(",","") for i in v3["title"].to_list()]
    v3["channel_title"] = [i.replace(",","") for i in v3["channel_title"].to_list()]
    v3.to_csv(f"./db/{datefile}.csv",sep=',')
    print("Arrangement Finished!")

def push_data_to_table(datefile):
    conn = psycopg2.connect("host=34.220.116.144 port=5432 dbname=apidata user=gmarr password=MTia100%s2021!!")
    cur = conn.cursor()
    with open(f'./db/{datefile}.csv', 'r', encoding="utf8") as f:
        # Notice that we don't need the `csv` module.
        next(f) # Skip the header row.
        cur.copy_from(f, f'{datefile}', sep=',')

    conn.commit()
    print("Data Added to Table!")


if __name__ == "__main__":
   mainsql()