import os
import xml.etree.ElementTree as ET

def create_tableau_workbook():
    os.makedirs('deliverables', exist_ok=True)
    twb_path = os.path.join('deliverables', 'Executive_Sales_Performance.twb')

    # Create Tableau XML structure
    workbook = ET.Element('workbook', {
        'source-build': '2023.3.0',
        'source-platform': 'win',
        'version': '18.1',
        'xmlns:user': 'http://www.tableausoftware.com/xml/user'
    })

    # Preferences & Document properties
    ET.SubElement(workbook, 'preferences')

    # Datasources
    datasources = ET.SubElement(workbook, 'datasources')
    datasource = ET.SubElement(datasources, 'datasource', {
        'caption': 'Sales Financial Dataset',
        'inline': 'true',
        'name': 'federated.sales_financial',
        'version': '18.1'
    })

    connection = ET.SubElement(datasource, 'connection', {
        'class': 'federated'
    })

    named_connections = ET.SubElement(connection, 'named-connections')
    named_conn = ET.SubElement(named_connections, 'named-connection', {
        'caption': 'sales_financial_dataset',
        'name': 'textscan.sales_financial'
    })
    
    # Relative path to CSV
    ET.SubElement(named_conn, 'connection', {
        'class': 'textscan',
        'directory': '../data',
        'filename': 'sales_financial_dataset.csv',
        'separator': ','
    })

    # Calculated Fields in Tableau
    # 1. Profit Margin %
    col_pm = ET.SubElement(datasource, 'column', {
        'caption': 'Profit Margin %',
        'datatype': 'real',
        'default-format': 'p0.0%',
        'name': '[Calculation_ProfitMargin]',
        'role': 'measure',
        'type': 'quantitative'
    })
    ET.SubElement(col_pm, 'calculation', {
        'class': 'tableau',
        'formula': 'SUM([Profit]) / SUM([Sales])'
    })

    # 2. Profit Status (Color Indicator)
    col_ps = ET.SubElement(datasource, 'column', {
        'caption': 'Profit Status',
        'datatype': 'string',
        'name': '[Calculation_ProfitStatus]',
        'role': 'dimension',
        'type': 'nominal'
    })
    ET.SubElement(col_ps, 'calculation', {
        'class': 'tableau',
        'formula': 'IF SUM([Profit]) >= 0 THEN "Profitable" ELSE "Unprofitable" END'
    })

    # 3. Target Sales Variance
    col_tv = ET.SubElement(datasource, 'column', {
        'caption': 'Target Variance %',
        'datatype': 'real',
        'default-format': 'p0.0%',
        'name': '[Calculation_TargetVariance]',
        'role': 'measure',
        'type': 'quantitative'
    })
    ET.SubElement(col_tv, 'calculation', {
        'class': 'tableau',
        'formula': '(SUM([Sales]) - SUM([Target Sales])) / SUM([Target Sales])'
    })

    # 4. Regional LOD Benchmark
    col_lod = ET.SubElement(datasource, 'column', {
        'caption': 'Region Benchmark Sales',
        'datatype': 'real',
        'name': '[Calculation_RegionLOD]',
        'role': 'measure',
        'type': 'quantitative'
    })
    ET.SubElement(col_lod, 'calculation', {
        'class': 'tableau',
        'formula': '{ FIXED [Region] : SUM([Sales]) }'
    })

    # Worksheets
    worksheets = ET.SubElement(workbook, 'worksheets')
    
    sheet_names = [
        'KPI_Scorecards',
        'Monthly_Sales_Profit_Trend',
        'Regional_Performance',
        'SubCategory_Profit_Matrix',
        'Customer_Segment_Share'
    ]

    for s_name in sheet_names:
        ws = ET.SubElement(worksheets, 'worksheet', {'name': s_name})
        table = ET.SubElement(ws, 'table')
        view = ET.SubElement(table, 'view')
        ET.SubElement(view, 'datasources')
        ET.SubElement(table, 'panes')
        ET.SubElement(table, 'rows')
        ET.SubElement(table, 'cols')

    # Dashboards
    dashboards = ET.SubElement(workbook, 'dashboards')
    dashboard = ET.SubElement(dashboards, 'dashboard', {'name': 'Executive_Sales_Performance_Dashboard'})
    ET.SubElement(dashboard, 'style')
    size = ET.SubElement(dashboard, 'size', {
        'maxheight': '900',
        'maxwidth': '1440',
        'minheight': '900',
        'minwidth': '1440',
        'sizing-mode': 'fixed'
    })

    zones = ET.SubElement(dashboard, 'zones')
    zone_root = ET.SubElement(zones, 'zone', {
        'h': '100000',
        'id': '1',
        'type-v2': 'layout-basic',
        'w': '100000',
        'x': '0',
        'y': '0'
    })

    # Write formatted XML
    tree = ET.ElementTree(workbook)
    ET.indent(tree, space="  ", level=0)
    tree.write(twb_path, encoding='utf-8', xml_declaration=True)
    print(f"Tableau Workbook file created at: {twb_path}")

if __name__ == '__main__':
    create_tableau_workbook()
