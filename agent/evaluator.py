def evaluate(result,expected_tools=None):
    tools=[x["tool"] for x in result.get("trace",[])]
    expected=expected_tools or []
    matched=sum(a==b for a,b in zip(tools,expected)); precision=matched/len(tools) if tools else 0.0; recall=matched/len(expected) if expected else 1.0
    return {"tool_sequence":tools,"expected_tools":expected,"precision":round(precision,3),"recall":round(recall,3),"success":result.get("status")=="completed" and (not expected or tools==expected)}
