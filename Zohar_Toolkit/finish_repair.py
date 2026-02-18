import json

path = "Intelligence_Database/ORACLE_KNOWLEDGE_BASE.json"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# The file currently ends at "TRUNCATED MASSIVE BLOB]\"" based on my previous script logic?
# No, my previous script joined with newlines.
# The tail output showed:
#                     "[TRUNCATED MASSIVE BLOB]"

# So it ends with a quote.
# It needs:
# ]  (close value list)
# }  (close object)
# ]  (close secrets_found list)
# }  (close intelligence object)
# }  (close root object)

# Let's try appending valid closers until it parses.
closers = ["]", "}", "]", "}", "}"]
# We might need more or fewer.

# Let's try to find the last valid JSON prefix.
# Or just append and pray.

attempt = content + "\n]}]}}"

try:
    json.loads(attempt)
    print("Fixed with ]}]}}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(attempt)
except json.JSONDecodeError as e:
    print(f"Failed: {e}")
    # Try other combinations
    # Maybe it was just `]}]}` ?
    
    # Let's count again on the *truncated* content
    o_brace = content.count('{')
    c_brace = content.count('}')
    o_brack = content.count('[')
    c_brack = content.count(']')
    
    print(f"Braces: {o_brace} open, {c_brace} close -> Need {o_brace - c_brace} closing")
    print(f"Brackets: {o_brack} open, {c_brack} close -> Need {o_brack - c_brack} closing")
    
    suffix = ""
    # We usually close brackets then braces, or vice versa depending on context.
    # But here we know we are deep in structure.
    # We are in `value` (list) inside `secret` (object) inside `secrets_found` (list) inside `intelligence` (object) inside `root` (object).
    # So: List -> Object -> List -> Object -> Object
    # ] -> } -> ] -> } -> }
    
    # But wait, `intelligence` might be inside something else? No, usually root.
    
    suffix += "]" * (o_brack - c_brack)
    suffix += "}" * (o_brace - c_brace)
    
    try:
        json.loads(content + suffix)
        print(f"Fixed with calculated suffix: {suffix}")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content + suffix)
    except Exception as e2:
        print(f"Still failed: {e2}")

