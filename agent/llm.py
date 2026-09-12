import json,os,urllib.request
class OpenAICompatibleClient:
    def __init__(self,base_url=None,api_key=None,model=None):
        self.base_url=(base_url or os.getenv("LLM_BASE_URL","https://api.openai.com/v1")).rstrip("/"); self.api_key=api_key or os.getenv("LLM_API_KEY"); self.model=model or os.getenv("LLM_MODEL","gpt-5.6")
    def chat(self,messages,temperature=0):
        if not self.api_key: raise RuntimeError("LLM_API_KEY is not configured")
        body=json.dumps({"model":self.model,"messages":messages,"temperature":temperature}).encode()
        req=urllib.request.Request(self.base_url+"/chat/completions",data=body,headers={"Content-Type":"application/json","Authorization":"Bearer "+self.api_key})
        with urllib.request.urlopen(req,timeout=60) as r:return json.loads(r.read())["choices"][0]["message"]["content"]
