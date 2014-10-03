from eppy import readhtml
import pprint

htmlDoc = open('/Users/eayoungs/repo/Sim/Templates/Scripting/Output/ASHRAE90.1_RetailStandalone_STD2010_SalemTable.html', 'r')
thisLinesTable = readhtml.lines_table(htmlDoc, True)
pp = pprint.PrettyPrinter(depth=6)

def _report_tables(linesTable):
    """Uses the output of lines_table function to produce a set
    of report tables addressable by name """
    
    reportNm = []
    tableDict = {}
    reportDict = {}
    indx = 0

    for i in range(len(linesTable)):
        reportHeader = (linesTable[i][0])
        for j in range(len(reportHeader)):
            if 'Report: ' in reportHeader[j]:
                reportNm.append(reportHeader[j])
                if reportNm[indx] != reportNm[indx-1]:
                    print('!=',reportNm[indx], reportHeader[2], 'Report')
                    reportDict[reportHeader[j]] = linesTable[i][1]
                else: 
                    print(reportNm[indx], reportHeader[2], 'Table')
                indx = indx+1
    pp.pprint(reportDict.keys())
    return 

# def select_table(report_name, table_name, html_doc):
#    """Uses the output of report_tables function to produce a
#        set of nested tables where table values can be
#        addressed by column & row names"""
#    htmlDoc = open(html_doc, 'r')
#    htmlContents = htmlDoc.read()
#    tableDict = report_tables(htmlContents)
#    grid = tableDict[report_name]
#    return grid

def test_report_tables():
    """py.test for test_named_tables"""
    result = _report_tables(thisLinesTable)
    assert result == [u'Report: Annual Building Utility Performance Summary',
 u'Report: Input Verification and Results Summary',
 u'Report: Climatic Data Summary',
 u'Report: Envelope Summary',
 u'Report: Equipment Summary',
 u'Report: HVAC Sizing Summary',
 u'Report: System Summary',
 u'Report: Component Sizing Summary',
 u'Report: MONTHLY INDOOR TEMP',
 u'Report: OCCUPANT COMFORT DATA SUMMARY',
 u'Report: EMISSIONS DATA SUMMARY',
 u'Report: OUTDOOR AIR SUMMARY',
 u'Report: VENTILATION LOAD COMPONENTS',
 u'Report: OVERALL HVAC AIR SYSTEM LOADS',
 u'Report: OVERALL HVAC SYSTEM ENERGY',
 u'Report: COMPONENTS OF PEAK ELECTRICAL DEMAND',
 u'Report: COMPONENTS OF PEAK NET ELECTRICAL DEMAND',
 u'Report: SETPOINTS NOT MET WITH TEMPERATURES',
 u'Report: BUILDING LOADS - COOLING',
 u'Report: BUILDING LOADS - HEATING',
 u'Report: BUILDING LOADS - ELECTRIC',
 u'Report: SPACE LOADS',
 u'Report: ENERGY CONSUMPTION - ELECTRICITY & NATURAL GAS',
 u'Report: BUILDING ENERGY PERFORMANCE - ELECTRICITY',
 u'Report: BUILDING ENERGY PERFORMANCE - NATURAL GAS',
 u'Report: PEAK ENERGY END-USE - ELECTRICITY PART 1',
 u'Report: PEAK ELECTRICAL DEMAND',
 u'Report: PEAK GAS DEMAND',
 u'Report: EndUseEnergyConsumptionElectricityMonthly']