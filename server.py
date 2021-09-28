#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from markupsafe import Markup
import flask_excel as excel
import pandas as pd
import sys, os

inputfile = "/home/fuqiuyu/work/cavity_server/data/output.xlsx"

df = pd.read_excel(inputfile)

selected_df = df[["uniprot", "description", "PDB", "residues"]]
selected_df = selected_df[selected_df["PDB"].notnull()]


def button_html(url, input_value, text, cls="btn-link"):
    line = f"""<form action="{url}" method="post">"""
    line = (
        line
        + f"""<button type="submit" name="input" value="{input_value}" class="{cls}">"""
    )
    line = line + f"""{text}</button></form>"""
    return line


def map_func(x):
    index = str(x[0])
    all_cys = [a.strip() for a in x["residues"].split(",")]
    outhtml = ""

    for cys in all_cys:
        url = "/view_single"
        input_value = index + "|" + cys
        text = cys
        outhtml = outhtml + button_html(url, input_value, text)
    return outhtml


selected_df["residues"] = df.apply(map_func, axis=1)


app = Flask(__name__, static_url_path="", static_folder="", template_folder="")


@app.route("/browse")
def browse():
    return render_template(
        "html/template.html",
        content=Markup(selected_df.to_html(escape=False, table_id="main_table")),
    )


@app.route("/<path:path>")
def send_js(path):
    return send_from_directory("/", path)


@app.route("/view_single", methods=["GET", "POST"])
def view_single(**args):
    if request.method == "POST":
        input_str = request.form["input"]
        index = int( input_str.split('|')[0] )
        cys   = input_str.split('|')[1]
        dirname = f"{index}:{cys}"
        if os.path.isdir(f"data/work/{dirname}"):
            return view_single_exist(dirname)
        else:
            os.mkdir(f"data/work/{dirname}")
            import module.covdock as covdock
            os.chdir(f"data/work/{dirname}")
            covdock.runcovdock(dirname)
            os.chdir("../../..")
            return view_single_exist(dirname)
    else:
        return False
        pass

@app.route("/view_single_exist/<dirname>")
def view_single_exist(dirname=None):
    return render_template(
        "html/template.html",
        content=dirname
    )


@app.route("/")
def index():
    return browse()


if __name__ == "__main__":
    app.run(host="192.168.54.37", debug=True)
