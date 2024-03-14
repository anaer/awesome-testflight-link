#!/usr/bin/python

import sqlite3
import re, os, sys

README_TEMPLATE_FILE = "./data/README.template"

def renew_readme():
    markdown = []
    markdown.append(f"# Available Testflight App List\n")
    markdown.append(f"Collect Public Testflight app URL's (iOS/iPad OS/macOS), feel free to create a issue.\n\n")
    markdown.append(f"| type | name | link | last_modify |\n")
    markdown.append(f"| --- | --- | --- | --- |\n")

    conn = sqlite3.connect('../db/sqlite3.db')
    cur = conn.cursor()
    for table in {'chinese', 'ios_game', 'ios', 'macos'}:
        res = cur.execute(f"""SELECT app_name, testflight_link, status, last_modify FROM {table} WHERE status = 'Y' ORDER BY last_modify DESC;""")
        for row in res:
            app_name, testflight_link, status, last_modify = row
            testflight_link = f"[https://testflight.apple.com/join/{testflight_link}](https://testflight.apple.com/join/{testflight_link})"
            markdown.append(f"| {table} | {app_name} | {testflight_link} | {last_modify} |\n")
        markdown.append(f"| --- | --- | --- | --- |\n")

    with open("../README.md", 'w') as f:
        f.writelines(markdown)
    conn.close()

def main():
    renew_readme()

if __name__ == "__main__":
    os.chdir(sys.path[0])
    main()
