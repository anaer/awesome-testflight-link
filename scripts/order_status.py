#!/usr/bin/python

import sqlite3
import re, os, sys

README_TEMPLATE_FILE = "./data/README.template"

def renew_readme():
    markdown = []
    markdown.append(f"# Available Testflight App List\n")
    markdown.append(f"| type | name | last_modify |\n")
    markdown.append(f"| --- | --- | --- |\n")

    conn = sqlite3.connect('../db/sqlite3.db')
    cur = conn.cursor()
    res = cur.execute(f"""
      SELECT 'chinese' type, app_name, testflight_link, status, last_modify FROM chinese WHERE status = 'Y' 
UNION SELECT 'ios_game' type, app_name, testflight_link, status, last_modify FROM ios_game WHERE status = 'Y' 
UNION SELECT 'ios' type, app_name, testflight_link, status, last_modify FROM ios WHERE status = 'Y' 
UNION SELECT 'macos' type, app_name, testflight_link, status, last_modify FROM macos WHERE status = 'Y' 
    ORDER BY last_modify DESC;
    """)
    for row in res:
        type, app_name, testflight_link, status, last_modify = row
        app_name = f"[{app_name}](https://testflight.apple.com/join/{testflight_link})"
        markdown.append(f"| {type} | {app_name} | {last_modify} |\n")

    with open("../README.md", 'w') as f:
        f.writelines(markdown)
    conn.close()

def main():
    renew_readme()

if __name__ == "__main__":
    os.chdir(sys.path[0])
    main()
