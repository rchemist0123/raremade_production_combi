import polars as pl
import streamlit as st
import itertools as it

def get_combination(name, color, size):
    combi = list(it.product(name, color, size))
    df = pl.DataFrame(combi, schema=['Name', 'Color', 'Size'], orient="row")
    return(df)

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
            # if len(amounts) != combi.height:
            #     st.error("입력한 수량의 수가 상품의 조합과 맞지 않음!")
            combi = combi.with_columns(pl.lit('').alias("Amount"))
            st.session_state.combinations = st.session_state.combinations.vstack(combi)

    if not st.session_state.combinations.is_empty():
        st.write('### 상품 리스트')
        st.data_editor(st.session_state.combinations, width=800, height=400)
        csv_data = st.session_state.combinations.write_csv()

    else:
        st.info('단추 이름과 옵션을 입력해주세요!')
    # st.download_button(
    #     label="Download as CSV",
    #     data=csv_data,
    #     file_name='combinations.csv',
    #     mime='text/csv'
    # )