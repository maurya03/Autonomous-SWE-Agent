from pathlib import Path
import ast, operator, subprocess
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv,ast.Mod:operator.mod}

def _safe(root,path):
    base=Path(root).resolve(); p=(base/path).resolve()
    if base not in p.parents and p!=base: raise ValueError("path escapes workspace")
    return p

def list_files(root=".",limit=200):
    base=Path(root); return [str(p.relative_to(base)) for p in sorted(base.rglob("*")) if p.is_file() and ".git" not in p.parts][:limit]

def read_file(path,root=".",max_chars=12000): return _safe(root,Path(path)).read_text(errors="replace")[:max_chars]

def search_text(query,root=".",limit=30):
    q=query.lower(); out=[]
    for f in list_files(root,1000):
        p=_safe(root,Path(f))
        try: lines=p.read_text(errors="replace").splitlines()
        except Exception: continue
        for no,line in enumerate(lines,1):
            if q in line.lower(): out.append({"file":f,"line":no,"text":line[:500]})
            if len(out)>=limit:return out
    return out

def calculate(expression):
    tree=ast.parse(expression,mode="eval")
    def ev(n):
        if isinstance(n,ast.Constant) and isinstance(n.value,(int,float)):return n.value
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.USub,ast.UAdd)): return -ev(n.operand) if isinstance(n.op,ast.USub) else ev(n.operand)
        if isinstance(n,ast.BinOp) and type(n.op) in OPS:return OPS[type(n.op)](ev(n.left),ev(n.right))
        raise ValueError("unsupported expression")
    return ev(tree.body)

def run_tests(command=("python","-m","pytest","-q"),cwd=".",timeout=120):
    p=subprocess.run(list(command),cwd=cwd,text=True,capture_output=True,timeout=min(timeout,120)); return {"exit_code":p.returncode,"stdout":p.stdout[-8000:],"stderr":p.stderr[-4000:]}

def git_diff(root="."):
    p=subprocess.run(["git","diff","--","."],cwd=root,text=True,capture_output=True,timeout=20); return {"exit_code":p.returncode,"diff":p.stdout[-12000:]}

TOOLS={"list_files":list_files,"read_file":read_file,"search_text":search_text,"calculate":calculate,"run_tests":run_tests,"git_diff":git_diff}
RISK={"list_files":"low","read_file":"low","search_text":"low","calculate":"low","git_diff":"low","run_tests":"medium"}
