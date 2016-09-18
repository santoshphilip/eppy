"""sample html for pytesting"""
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

sample_html = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN""http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title> 1050PageMillRoad Mountain View Moffett Fld Nas CA USA TMY3 WMO#=745090
  2014-01-13
  16:47:19 
 - EnergyPlus</title>
</head>
<body>
<p><a href="#toc" style="float: right">Table of Contents</a></p>
<a name=top></a>
<p>Program Version:<b>EnergyPlus-Windows-32 8.1.0.008, YMD=2014.01.13 16:47</b></p>
<p>Tabular Output Report in Format: <b>HTML</b></p>
<p>Building: <b>1050PageMillRoad</b></p>
<p>Environment: <b>Mountain View Moffett Fld Nas CA USA TMY3 WMO#=745090</b></p>
<p>Simulation Timestamp: <b>2014-01-13
  16:47:19</b></p>
<hr>
<p><a href="#toc" style="float: right">Table of Contents</a></p>
<a name=AnnualBuildingUtilityPerformanceSummary::EntireFacility></a>
<p>Report:<b> Annual Building Utility Performance Summary</b></p>
<p>For:<b> Entire Facility</b></p>
<p>Timestamp: <b>2014-01-13
    16:47:19</b></p>
<b>Values gathered over      8760.00 hours</b><br><br>
<b></b><br><br>
<b>Site and Source Energy</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Site and Source Energy-->
<table border="1" cellspacing="0" cellpadding="4">
    <tr>
        <td>a</td>
        <td>2</td>
    </tr>
    <tr>
        <td>3</td>
        <td>4</td>
    </tr>
</table><br><br>
<b>Site to Source Energy Conversion Factors</b><br><br>
<!-- FullName:Annual Building Utility Performance Summary_Entire Facility_Site to Source Energy Conversion Factors-->
<table border="1" cellspacing="0" cellpadding="4">
    <tr>
        <td>b</td>
        <td>6</td>
    </tr>
    <tr>
        <td>7</td>
        <td>8</td>
    </tr>
</table><br><br>
<p>Some:<b> Random stuff</b></p>

<hr>
<p>Report:<b> COMPONENTS OF PEAK ELECTRICAL DEMAND</b></p>
<p>For:<b> Meter</b></p>
<p>Timestamp: <b>2014-01-13
    16:47:19</b></p>
<b>Custom Monthly Report</b><br><br>
<table border="1" cellspacing="0" cellpadding="4">
    <tr>
        <td>c</td>
        <td>16</td>
    </tr>
    <tr>
        <td>17</td>
        <td>18</td>
    </tr>
</table><br><br>

<hr>
<p>Report:<b> COMPONENTS OF PEAK NET ELECTRICAL DEMAND</b></p>
<p>For:<b> Meter</b></p>
<p>Timestamp: <b>2014-01-13
    16:47:19</b></p>
<b>Custom Monthly Report</b><br><br>
<table border="1" cellspacing="0" cellpadding="4">
    <tr>
        <td>d</td>
        <td>26</td>
    </tr>
    <tr>
        <td>27</td>
        <td>28</td>
    </tr>
</table><br><br>


<br><br>
<b>Computation -  Automatic</b><br><br>
MONTHLYRATEGASCHARGE FROM TotalEnergy CA_MONTHLYGASRATES<br>
EnergyCharges SUM MONTHLYRATEGASCHARGE<br>
Basis SUM EnergyCharges DemandCharges ServiceCharges<br>
Subtotal SUM Basis Adjustment Surcharge<br>
TAXOFEIGHTPERCENT FROM Subtotal<br>
Taxes SUM TAXOFEIGHTPERCENT<br>
Total SUM Subtotal Taxes<br>
</body>
</html>
"""
