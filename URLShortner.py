from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import base62 as base62
import sqlite3
from fastapi.responses import RedirectResponse

app = FastAPI()

def get_conn():
    conn= sqlite3.connect('urlshortner.db')
    curr = conn.cursor()
    return conn, curr

@app.post("/shorten/{long_url}")
def shorten(long_url:str):
    hash_bytes = hashlib.md5(long_url.encode('utf-8')).digest()
    hash_int= int.from_bytes(hash_bytes, 'big')
    short_hash= base62.encode(hash_int)
    conn,curr=get_conn()
    curr.execute("SELECT id FROM url_list order by id desc limit 1")
    result=curr.fetchone()
    if result:
        id= result[0]+1
    else:
        id=1
    
    print(id, long_url, short_hash[:8])
    curr.execute(
        "INSERT INTO url_list(id, long_url, short_url, analysis) VALUES (?, ?, ?, ?)",
        (id, long_url, short_hash[:8], "abc"),
    )
    conn.commit()
    conn.close()
    return {"short_url": short_hash[:8], "full_hash": short_hash}


@app.get("/{short_hash}")
def redirect(short_hash:str):
    #Convert short hash to base 10 integer
    hash_int = base62.decode(short_hash)
    #Look up ID in the database which is sqlite3 database
    #conn = sqlite3.connect('urlshortner.db')
    conn,curr=get_conn()
    print("Database connected successfully.")
    curr.execute("SELECT long_url FROM url_list WHERE short_url = ?", (short_hash,))
    result = curr.fetchone()
    if result:
        decoded_string = result[0].replace('%3A', ':').replace('%2F', '/')
        return{"url":decoded_string}
    else:
        return{"error":"URL Not found"}