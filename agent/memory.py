import json, sqlite3, time

class Memory:
    def __init__(self, path="agent.db"):
        self.db=sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, ts REAL, state TEXT, type TEXT, message TEXT, data TEXT)")
        self.db.commit()
    def add(self,state,type_,message,data=None):
        self.db.execute("INSERT INTO events(ts,state,type,message,data) VALUES(?,?,?,?,?)",(time.time(),state,type_,message,json.dumps(data or {}))); self.db.commit()
    def recent(self,n=50):
        rows=self.db.execute("SELECT state,type,message,data FROM events ORDER BY id DESC LIMIT ?",(n,)).fetchall()[::-1]
        return [{"state":s,"type":t,"message":m,"data":json.loads(d)} for s,t,m,d in rows]
    def close(self): self.db.close()
