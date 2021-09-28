#!/usr/bin/env python
import sys,os
import imp
fml = imp.load_source("fmysql_lib","/home/fuqy/work/SPA_database/module/fmysql_lib.py")
import cgi
import cgitb
# import importlib
# importlib.import_module(name, package=None)

#cgitb.enable(display=0, logdir="/log")

form = cgi.FieldStorage() 
content = ''
ac = form.getvalue('ac')
ac = int(ac)
system_info,waters,files = fml.fetch_query(ac=ac)

pdbid = system_info[1]
chain = system_info[2]
ligname = system_info[3]
resolution = system_info[4]
n_waters = system_info[5]
time = system_info[6]
graphicpdb = files['graphicpdb']

content = '''
  <hr width="90%%" align="center" />
  <table width="80%%" border="0" cellspacing="0" cellpadding="0" align="center"> <!-- structure information -->
    <tr class="STYLE3" align="center">
      <td valign="middle">PDB ID:&nbsp;&nbsp;<a href=https://www.rcsb.org/structure/%s>%s</a></td>
      <td valign="middle">Resolution:&nbsp;&nbsp;%g</td>
      <td valign="middle">Chain:&nbsp;&nbsp;%s</td>
      <td valign="middle">Pocket:&nbsp;&nbsp;%s</td>
      <td valign="middle">Number of Waters:&nbsp;&nbsp;%d</td>
      <td valign="middle">Deposited Date:&nbsp;&nbsp;%s</td>
    </tr>
  </table>
  <hr width="90%%" align="center"/>
'''%(pdbid,pdbid.upper(),resolution,chain,ligname,n_waters,time)

content = content + '''
  <table width="90%"  height=600 cellspacing="1" cellpadding="0" align="center" frame="hsides" rules="cols"> <!-- graphic applet & water data -->
      <tr>
        <td width="5%" align="center" valign='top'><font size="4.5" color="#0099FF">  
        </td>
        <td width="45%" align="center" valign='top'><font size="4.5" color="#0099FF">  <!-- Applet 0 -->
            <script type="text/javascript">
                Jmol.getApplet("jmolApplet0", Info0);
            </script>
        </td>

        <td width="45" align="center"><font size="4.5" color="#0099FF"> <!-- table data 1 -->
          <div style="overflow:scroll;height:600px">
              <table class="tg" scrolling="yes" height = 800 >
                <tr>
                  <th class="tg-amwm" width="30%" align=center>Water No.</th>
                  <th class="tg-amwm" width="30%" align=center>SPA energy ( kcal/mol )</th>
                  <th class="tg-amwm" width="30%" align=center>Occupancy</th>
                </tr>
'''

keys = waters.keys()
# keys.sort()
for key in keys:
    water = waters[key]
    index = water[1]
    occ = water[2]
    spa_g = water[9]
    tmp_ = '''
                    <tr onClick="javascript:highlight_water(jmolApplet0,%d);togglecolor(this)">
                      <td class="tg-baqh" align=center>%d</td>
                      <td class="tg-baqh" align=center>%g</td>
                      <td class="tg-baqh" align=center>%g%%</td>
                    </tr>
    '''%(index,index,spa_g,occ*100)
    content = content + tmp_

content = content + '''
              </table>
          </div>
        <td width="5%%" align="center" valign='top'><font size="4.5" color="#0099FF">  
        </td>
      </tr>
  </table>

  <hr width="90%%" align="center" />
  <table border="0" cellpadding="5" align="center" height="10" class="YJ" > <!-- Download -->
    <tr>
      <style>
      p{ color:black; text-decoration:none; }
      </style>
      <td align="center" width="%%20" border="5" bgcolor="#D1D8BA">
          <a class="link" href="%s"><p>Download This Complex</p></a></td>
      </td>
      <td align="center" width="%%10" border="5">
      </td>
      <td align="center" width="%%20" border="5" bgcolor="#D1D8BA">
          <a class="link" href="%s"><p>Download SPA Summary</p></a></td>
      </td>
    </tr>
  </table>
'''%(files['graphicpdb'],files['spasummary'])

template = "/home/fuqy/work/SPA_database/www/html/template.html"
all_content = open(template).read()
all_content = all_content.replace("MAIN_CONTENT",content)
all_content = all_content.replace("PDB_FILE",graphicpdb)
print(all_content)

