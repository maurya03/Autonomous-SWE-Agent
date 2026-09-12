import json,sys
from .tools import TOOLS
SCHEMAS={name:{"name":name,"description":f"{name} tool"} for name in TOOLS}
def handle(req):
    method=req.get("method"); rid=req.get("id")
    if method=="initialize": return {"jsonrpc":"2.0","id":rid,"result":{"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"ase-tools","version":"1.0.0"}}}
    if method=="notifications/initialized": return None
    if method=="tools/list": return {"jsonrpc":"2.0","id":rid,"result":{"tools":list(SCHEMAS.values())}}
    if method=="tools/call":
        p=req.get("params",{}); name=p.get("name"); args=p.get("arguments",{})
        if name not in TOOLS: return {"jsonrpc":"2.0","id":rid,"error":{"code":-32602,"message":"unknown tool"}}
        try: out=TOOLS[name](**args); return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text":json.dumps(out,default=str)}],"isError":False}}
        except Exception as e:return {"jsonrpc":"2.0","id":rid,"result":{"content":[{"type":"text","text":str(e)}],"isError":True}}
    return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"method not found"}}
if __name__=="__main__":
    for line in sys.stdin:
        if line.strip():
            out=handle(json.loads(line));
            if out is not None: print(json.dumps(out),flush=True)
