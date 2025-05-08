import pickle
import locale
import pandas as pd
import streamlit as st
import datetime
from datetime import date
from datetime import timedelta
from io import BytesIO

def countCurUseFul(dateTuple):
    dateIni = dateTuple[0]
    num = dateTuple[1]
    mode = dateTuple[2]
    expr = dateTuple[3]
    dateIniStr = dateIni.strftime("%d/%m/%Y")
    dateIniName = dateIni.strftime("%#d de %B de %Y")
    count = 0 
    n = 0 
    if mode == 0:
        st.markdown(f'**Data inicial**  : {dateIniStr} ({dateIniName})')
        st.markdown(f'**Número de dias**: {num}')
        st.markdown(f"***:blue-background[{expr}]***")
    else:
        st.markdown(f"***:red-background[{expr}]***")
    while count < num:
        dateNew = dateIni + datetime.timedelta(days=n)
        weekNum = dateNew.weekday()
        weekName = dateNew.strftime("%A")
        dateFormat = dateNew.strftime("%d/%m/%Y")
        dateName = dateNew.strftime("%#d de %B de %Y")
        if n == 0:
            status = 'não conta'
        else: 
            if mode == 0:
                if count == num - 1: 
                    if any ([weekNum == 5 or weekNum == 6]):
                        status = 'não conta'
                    else:
                        status = 'conta'
                        count += 1
                else:
                    status = 'conta'
                    count += 1
            else:
                if any ([weekNum == 5 or weekNum == 6]):
                    status = 'não conta'
                else:
                    status = 'conta'
                    count += 1
        if status == 'conta': 
            countStr = f'{str(count)}.°'
        else: 
            countStr = ''        
        infoCombo = [f'{dateFormat} ({dateName})', weekName, status, countStr, n + 1]
        for i, info in enumerate(infoCombo):
            key = keyCurrent[i]
            dateCurrUse[key].append(info)    
        n += 1

# Function to convert DataFrame to Excel file in memory
def toExcel(sheet):
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name=sheet)
    writer.close()
    xlsx = output.getvalue()
    return xlsx
    
def toCsv():
    csv = df.to_csv(index=False).encode('ISO-8859-1')
    return csv

def toPickle():
    pkl = pickle.dumps(df)
    return pkl

def toHtml():
    htmlText = df.to_html(index=False)
    hmtlPlus = """
    <style>
        .button {
          background-color: #04AA6D; /* Green */
          border: None;
          color: white;
          text-align: center;
          text-decoration: none;
          display: inline-block;
          font-size: 13px;
          margin: 6px 2px;
          cursor: pointer;
        }
        .button1 {padding: 8px 14px;}
    </style>
    <button class="button button1" onclick=window.print()>Imprime</button>
    """    
    htmlText += f"<body>{hmtlPlus}</body>"
    return htmlText
    
def toTxt():
    txt = df.to_string(index=False).encode('ISO-8859-1')
    return txt
    
def iniVars():
    #Xlsx
    #st.download_button(
    #    label="dataframe <-> xlsx",
    #    data=toExcel('plan1'),
    #    file_name='data.xlsx',
    #    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #)
    #Csv
    st.download_button(
        label="dataframe <-> csv",
        data=toCsv(),
        file_name='dfTable.csv',
        mime='text/csv'  
    )
    #Pkl
    st.download_button(
        label="dataframe <-> pickle",
        data=toPickle(),
        file_name="dfTable.pkl",
        mime="application/octet-stream"
    )   
    #Html
    st.download_button(
        label="dataframe <-> html",
        data=toHtml(),
        file_name="dfTable.html"
    )
    #String
    st.download_button(
        label="dataframe <-> txt",
        data=toTxt(),
        file_name="dfTable.txt"
    )
    
def main():
    global output, df
    global keyCurrent, keyUseFul
    global dateCurrUse
    keyCurrent = ['dia do mês', 'dias da semana', 
                  'condição', 'sequencial', 'contador geral']
    dateCurrUse = {key:[] for key in keyCurrent}
    dateNow = datetime.date.today()
    d = date(2025, 5, 9)
    arg = (d, 12, 0, 'Contagem em dias corridos')
    countCurUseFul(arg)
    df = pd.DataFrame(dateCurrUse)
    st.dataframe(data=df, hide_index=True, use_container_width=True)
    output = BytesIO() 
    iniVars()

if __name__ == '__main__':
    main()

