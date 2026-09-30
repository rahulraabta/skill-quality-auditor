EXPLANATIONS = {
    "SC2": {
        "title": "Downloads and runs a script from the internet",
        "risk": "The skill fetches code from an external website and executes it on your computer. If that website is compromised or malicious, an attacker could run anything on your machine.",
        "action": "Do not install. If this came from a trusted source, ask them to bundle the script into the skill instead.",
    },
    "TM2": {
        "title": "Chains commands to bypass safety checks",
        "risk": "The skill strings multiple commands together with pipes or semicolons, which can hide malicious behavior behind a normal-looking first step.",
        "action": "Review each command in the chain carefully before installing.",
    },
    "PE3": {
        "title": "Reads sensitive credential files",
        "risk": "The skill accesses files like AWS credentials, SSH keys, or .env files. Anyone who controls the skill could use your cloud accounts or steal secrets.",
        "action": "Do not install unless you fully trust the author. Never install on a machine with real credentials.",
    },
    "LP3": {
        "title": "Does not declare which tools it uses",
        "risk": "The skill does not list its permissions, so it is impossible to verify what it can access.",
        "action": "Ask the author to add an allowed-tools or permissions field to the SKILL.md frontmatter.",
    },
    "E1": {
        "title": "Sends data to an external server",
        "risk": "The skill transmits data to a remote URL. This could be legitimate telemetry, or it could be exfiltration of your private data.",
        "action": "Inspect the destination URL. If it is not a well-known service, do not install.",
    },
    "EA2": {
        "title": "Makes decisions without asking you first",
        "risk": "The skill can perform high-impact actions without human confirmation.",
        "action": "Only install if the skill is designed for automation and you understand the consequences.",
    },
}


DEFAULT_EXPLANATION = {
    "title": "Unknown issue",
    "risk": "This finding does not have a plain-English explanation yet.",
    "action": "Review the raw finding details carefully.",
}


def explain_finding(rule_id):
    return EXPLANATIONS.get(rule_id, DEFAULT_EXPLANATION)
