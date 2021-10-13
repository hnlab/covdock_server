#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, url_for, redirect
from markupsafe import Markup
import flask_excel as excel
import pandas as pd
import sys, os

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

def prepare_dataset( inputfile = "/home/fuqiuyu/work/cavity_server/data/output.xlsx" ):
    # inputfile = "/home/fuqiuyu/work/cavity_server/data/output.xlsx"
    df = pd.read_excel(inputfile)
    selected_df = df[["uniprot", "description", "PDB", "residues"]]
    selected_df = selected_df[selected_df["PDB"].notnull()]
    selected_df["residues"] = df.apply(map_func, axis=1)
    return selected_df

app = Flask(__name__, static_url_path="", static_folder="", template_folder="")


@app.route("/browse/<dataset>")
def browse(dataset = None):
    df = prepare_dataset()
    return render_template(
        "html/template.html",
        content=Markup( df.to_html(escape=False, table_id="main_table") ) ,
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
            if os.path.getsize( "output/my_docking.pdbqt" ) > 32:
                os.chdir("../../..")
                return view_single_exist(dirname)
            else:
                os.chdir("../..")
                os.system("rm -r {dirname}")
                os.chdir("..")
                return view_single_fail(dirname)
    else:
        return False
        pass

@app.route("/view_single_exist/<dirname>")
def view_single_exist(dirname=None):
    return render_template(
        "html/view_single.html",
        dirname=dirname,
    )

@app.route("/all_datasets")
def list_datasets():
    content = f'''
        <p>Avaliable dataset listed below:</p>
        <table>
            <thead>
                <tr>
                    <th>publication</th>
                    <th>compound id</th>
                    <th>compound</th>
                    <th>view_link</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>The Proteome-Wide Potential for Reversible Covalency at Cysteine. Kristine Senkane. DOI: 10.1002/anie.201905829</td>
                    <td>1</td>
                    <td><img src="/img/compound1.png" alt="compound1" class=compoundimg ></td>
                    <td><a href="/view_dataset_1">View link</a></td>
                </tr>
                <tr>
                    <td>The Proteome-Wide Potential for Reversible Covalency at Cysteine. Kristine Senkane. DOI: 10.1002/anie.201905829</td>
                    <td>2</td>
                    <td><img src="/img/compound2.png" alt="compound2" class=compoundimg ></td>
                    <td><a href="/view_dataset_2">View link</a></td>
                </tr>
                <tr>
                    <td>The Proteome-Wide Potential for Reversible Covalency at Cysteine. Kristine Senkane. DOI: 10.1002/anie.201905829</td>
                    <td>3</td>
                    <td><img src="/img/compound3.png" alt="compound3" class=compoundimg ></td>
                    <td><a href="/view_dataset_3">View link</a></td>
                </tr>
                <tr>
                    <td>The Proteome-Wide Potential for Reversible Covalency at Cysteine. Kristine Senkane. DOI: 10.1002/anie.201905829</td>
                    <td>4</td>
                    <td><img src="/img/compound4.png" alt="compound4" class=compoundimg ></td>
                    <td><a href="/view_dataset_4">View link</a></td>
                </tr>
                <tr>
                    <td>The Proteome-Wide Potential for Reversible Covalency at Cysteine. Kristine Senkane. DOI: 10.1002/anie.201905829</td>
                    <td>5</td>
                    <td><img src="/img/compound5.png" alt="compound5" class=compoundimg ></td>
                    <td><a href="/view_dataset_5">View link</a></td>
                </tr>
            </tbody>
        </table>
        '''
    return render_template(
        "html/template.html",
        content = Markup(content)
    )

@app.route("/view_single_fail/<dirname>")
def view_single_fail(dirname=None):
    return render_template(
        "html/view_single_fail.html",
        dirname=dirname,
    )

@app.route("/view_dataset_4")
def view_dataset_4():
    return browse()

@app.route("/")
def root():
    return list_datasets()

@app.route("/index")
def index():
    return redirect( url_for("root") )

if __name__ == "__main__":
    app.run(host="192.168.54.37", debug=True)
