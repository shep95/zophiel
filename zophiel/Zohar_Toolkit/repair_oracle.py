import re
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def repair():
    path = "Intelligence_Database/ORACLE_KNOWLEDGE_BASE.json"
    
    if not os.path.exists(path):
        print("File not found.")
        return

    print("Reading file...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    print(f"Original length: {len(content)}")
    
    # It seems the file is valid JSON up until the massive string.
    # The massive string starts with "Author" and captures the rest of the line.
    # We can try to find the pattern and truncate it.
    
    # Look for the specific problematic entry
    # "value": [ ... "Author", "Notice: ACL ...
    
    # Heuristic: Find any string literal longer than 1000 chars and truncate it.
    # But doing this on raw JSON text is risky.
    
    # Better approach:
    # The file might just be incomplete or have a syntax error.
    # The error was "Expecting ',' delimiter".
    
    # Let's try to find where the JSON breaks.
    # We know line 6435 is huge.
    
    lines = content.split('\n')
    print(f"Total lines: {len(lines)}")
    
    new_lines = []
    for i, line in enumerate(lines):
        if len(line) > 2000:
            print(f"Truncating massive line {i+1} (Length: {len(line)})")
            # It's likely inside a string quote.
            # We want to keep the start, close the quote, and maybe the structure.
            # The structure is likely: "value": [ "Author", "MASSIVE_CONTENT" ],
            
            # If we just replace the line with a placeholder, we need to be careful about JSON structure.
            # The line content from the `Read` tool looked like: 
            # "                    \"Notice: ACL Config Found\"),o)))):null},R=()=>d.createElement(\"div\",{className:\"twtr-container\"},d.createElement(\"div\",{className:\"twtr-grid\"},d.createElement(\"div\",{className:\"twtr-col-12  twtr-text-center\"},d.createElement(\"span\",{\"aria-label\":\"Loading\",className:\"Icon Icon--loadingMedium\"}))));function I(e,t){return class extends d.Component{constructor(e){super(e),this.state={hasAccess:!1,showAuthorNote:!1}}componentDidUpdate(e){this.props.location.pathname!==e.location.pathname&&this.componentDidMount()}componentDidMount(){return(0,r.sH)(this,void 0,void 0,(function*(){if(this.isDiffPagePath())return void this.setState({hasAccess:!0});const[e,t,n,r]=yield Promise.all([this.gdprRedirect(),(0,o.A)(this.props.regionRestriction),_(this.props.userRoles),P(this.props.denyUserRoles)]);u().debug(`withAcl ${this.props.cqPath}: gdprRedirect[${e}] regionPass[${t}] allowedRolesPass[${n}] deniedRolesPass[${r}]`);const i=e=>{const t=null==e?void 0:e.path,n=this.props.cqPath;return t?t!==n||(u().debug(\"Skipping redirect that would result in loop\",t),!1):(u().debug(\"Skipping missing redirect\",t),!1)};e&&i(e)?this.doRedirect(e):!t&&i(this.props.regionRestrictionRedirect)?this.doRedirect(this.props.regionRestrictionRedirect):!n&&i(this.props.noAccessPage)?this.doRedirect(this.props.noAccessPage):!r&&i(this.props.denyRolesRedirect)?this.doRedirect(this.props.denyRolesRedirect):this.setState({hasAccess:!0}),this.setState({showAuthorNote:!0})}))}gdprRedirect(){return(0,i.JB)()&&(this.props.nonEuroGdprRedirectPath||this.props.euroGdprRedirectPath)?a().then((e=>{if(\"offboarded\"===e){const e=document.getElementById(\"twGeoLocationRegion\");if(!e)return this.props.nonEuroGdprRedirectPath||null;const t=e.getAttribute(\"data-value\");return\"eu\"===t||\"EU\"===t?this.props.euroGdprRedirectPath||null:this.props.nonEuroGdprRedirectPath||null}return Promise.resolve(null)})).catch((e=>(u().error(\"Failed to verify user state for logged in user\"[... 497307 chars omitted ...]"
            
            # We will replace it with: "                    \"[TRUNCATED MASSIVE CONTENT]\""
            # But we need to check if it ends with a comma or bracket.
            
            # Simpler: just replace the whole line with a safe string if it's the value line.
            # But the line might be part of a list.
            
            # Let's try to locate the start of the string and just cut it.
            # Assuming the line is mostly the string content.
            
            new_lines.append('                    "[TRUNCATED MASSIVE BLOB]"')
        else:
            new_lines.append(line)
            
    reconstructed = '\n'.join(new_lines)
    
    # Try to parse
    try:
        json.loads(reconstructed)
        print("Repair successful! JSON is valid.")
        with open(path, "w", encoding="utf-8") as f:
            f.write(reconstructed)
    except json.JSONDecodeError as e:
        print(f"JSON still invalid: {e}")
        # If it's just a missing closing brace/bracket at the very end (common if write was interrupted)
        if "Expecting value" in str(e) or "Expecting ',' delimiter" in str(e):
             # Try adding closing tags
             print("Attempting to close open structures...")
             # Count braces
             open_braces = reconstructed.count('{')
             close_braces = reconstructed.count('}')
             open_brackets = reconstructed.count('[')
             close_brackets = reconstructed.count(']')
             
             needed_braces = open_braces - close_braces
             needed_brackets = open_brackets - close_brackets
             
             print(f"Needed }} : {needed_braces}")
             print(f"Needed ] : {needed_brackets}")
             
             # This is naive because order matters, but often works for simple tail cuts.
             # Usually it's ] } ] } sequence.
             
             # Let's assume the standard structure: 
             # root { intelligence { secrets_found [ { ... } ... ] ... } ... }
             
             # If we are deep inside secrets_found, we probably need:
             # ] (close value list)
             # } (close secret object)
             # ] (close secrets_found array)
             # } (close intelligence object)
             # } (close root)
             
             # Let's just try appending combinations until it works? No, too slow.
             
             # Let's look at the end of the file again.
             print("Tail of reconstructed:")
             print(reconstructed[-200:])
             
             # If the last line was the truncated one, we might need to add comma or closing.
             
             # If we can't parse it, we might just save the truncated version and hope the user can inspect, 
             # OR we aggressive close it.
             
             suffix = ""
             if needed_brackets > 0: suffix += "]" * needed_brackets
             if needed_braces > 0: suffix += "}" * needed_braces
             
             # Try with suffix
             try:
                 json.loads(reconstructed + suffix)
                 print("Repair with suffix successful!")
                 with open(path, "w", encoding="utf-8") as f:
                    f.write(reconstructed + suffix)
                return
            except Exception as e:
                logging.error(f"Repair with suffix failed: {e}")
                 
             # Try reverse order
             suffix = ""
             if needed_braces > 0: suffix += "}" * needed_braces
             if needed_brackets > 0: suffix += "]" * needed_brackets
             
             try:
                 json.loads(reconstructed + suffix)
                 print("Repair with reverse suffix successful!")
                 with open(path, "w", encoding="utf-8") as f:
                    f.write(reconstructed + suffix)
                return
            except Exception as e:
                logging.error(f"Repair with reverse suffix failed: {e}")
                 
             # If all fails, save the truncated version anyway so we can at least read it.
             print("Could not fully auto-repair JSON structure, but saved truncated version.")
             with open(path, "w", encoding="utf-8") as f:
                 f.write(reconstructed)

if __name__ == "__main__":
    repair()
