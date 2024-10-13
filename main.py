import polars as pl
import pandas as pd
import streamlit as st
import itertools as it
import datetime
from io import BytesIO

def get_combination(name, color, size):
    combi = list(it.product(name, color, size))
    df = pl.DataFrame(combi, schema=['Name', 'Color', 'Size'], orient="row")
    return(df)

def toExcel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_pandas().to_excel(writer, index=False, sheet_name='Sheet1')
    # writer = pd.ExcelWriter(output, engine='xlsxwriter')
    # df.to_pandas().to_excel(writer, index=False, sheet_name='Sheet1')
    # # workbook = writer.book
    # # worksheet = writer.sheets['Sheet1']
    # # format1 = workbook.add_format({'num_format': '0'}) 
    # worksheet.set_column('A:A', None, format1)  
    # writer.save()
    # processed_data = output.getvalue()
    output.seek(0)  # Rewind the buffer
    return output

if 'combinations' not in st.session_state:
    st.session_state.combinations = pl.DataFrame({
        'Name': pl.Series([], dtype=pl.Utf8),  # Empty string column
        'Color': pl.Series([], dtype=pl.Utf8), # Empty string column
        'Size': pl.Series([], dtype=pl.Utf8),  # Empty string column
        'Amount': pl.Series([], dtype=pl.Utf8)
    })

st.title("Raremade 상품 조합 생성기")

# num:int = 1;
with st.form("hi",clear_on_submit=True):
    name_input = st.text_input("상품명")
    color_input = st.text_input("색상 종류(,로 구분)")
    size_input = st.text_input("사이즈 종류(,로 구분)")
    add = st.form_submit_button("추가")
    if add:
        names = [name_input]
        colors = [c.strip() for c in color_input.split(",")]
        sizes = [s.strip()+"mm" for s in size_input.split(",")]
        if names and colors and sizes:
            combi = get_combination(names, colors, sizes)
            combi = combi.with_columns(pl.lit('').alias("Amount"))
            st.session_state.combinations = st.session_state.combinations.vstack(combi)
    else:
        st.info('단추 이름과 옵션을 입력해주세요!')

if not st.session_state.combinations.is_empty():
    st.write('### 상품 리스트')
    st.data_editor(st.session_state.combinations, width=800, height=400, )
    df_xlsx = toExcel(st.session_state.combinations)
    st.download_button(label='엑셀파일로 다운로드',
                        data=df_xlsx,
                        icon= "👇🏻",
                        file_name= f'{datetime.date.today().strftime("%Y-%m-%d")}_레어메이드 신제품.xlsx')