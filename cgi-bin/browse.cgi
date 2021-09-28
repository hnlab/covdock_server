#!/usr/bin/env python
import sys,os
import imp
fml = imp.load_source("fmysql_lib","/home/fuqy/work/SPA_database/module/fmysql_lib.py")
import cgi
import cgitb

# cgitb.enable(display=0, logdir="/log")
form = cgi.FieldStorage()
content = ''
refresh = form.getvalue('update')

spahome = os.environ['SPA_DATABASE_HOME']

for line in open(f"{spahome}/www/html/browse.cache.html"):
    print(line,end='')

sys.exit()

if True:

    template = "/home/fuqy/work/SPA_database/www/html/template.html"

    result = fml.list_all(category = 'RESPA')

    content = """
    <style type="text/css">
    .tg  {border-collapse:collapse;border-spacing:0;border-color:#ccc;width:50%;}
    .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-top-width:1px;border-bottom-width:1px;border-color:#ccc;color:#333;background-color:#fff;}
    .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-top-width:1px;border-bottom-width:1px;border-color:#ccc;color:#333;background-color:#f0f0f0;}
    .tg .tg-cly1{text-align:center;vertical-align:middle;font-color:#eee;}
    .tg .tg-0lax{text-align:center;vertical-align:middle;}
    a.in-table{color:#00f;}
    </style>
    <table class="tg" align="center">
    <hr width="90%" align="center" />
    """
    content = content + '''
      <tr>
        <th class="tg-0lax">%s</th>
        <th class="tg-0lax">%s</th>
        <th class="tg-0lax">%s</th>
        <th class="tg-0lax">%s</th>
        <th class="tg-0lax">%s</th>
        <th class="tg-0lax">%s</th>
        <th class="tg-0lax">%s</th>
      </tr>
    '''%("Index","PDB id","Chain","Pocket","Number of hydration sites","Protein name","Update date")

    for i in result:
        items = i
        # (28206, '16pk', 'RESPA', 'ALL', 'A', 'BIS', 0.0, 82, None, datetime.datetime(2020, 8, 31, 16, 11, 14))
        index = items[0]
        pdbid = items[1]
        category = items[2]
        source = items[3]
        chain = items[4]
        pocket = items[5]
        resolution = items[6]
        num_waters = items[7]
        alternative_pose = items[8] 
        date = items[9]
        protein_name = fml.get_protein_name(index)

        content = content + '''
          <tr>
            <th class="tg-cly1"><a class="in-table" href='/cgi-bin/single_entry.cgi?ac=%d'>%s</a></th>
            <th class="tg-cly1">%s</th>
            <th class="tg-cly1">%s</th>
            <th class="tg-cly1">%s</th>
            <th class="tg-cly1">%s</th>
            <th class="tg-cly1">%s</th>
            <th class="tg-cly1">%s</th>
          </tr>
        '''%(index,index,pdbid,chain,pocket,num_waters,protein_name,date)

    content = content + """\n</table>\n"""

    all_content = open(template).read()
    all_content = all_content.replace("MAIN_CONTENT",content)

    print(all_content)

