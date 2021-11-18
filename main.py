import streamlit as st
import urllib
import pandas as pd
from downloader import queries_to_results

DATA_URL_ROOT = "https://raw.githubusercontent.com/sweetcocoa/word_batch_finder/master/"
test_on_local = True

if test_on_local:

    @st.cache(show_spinner=False)
    def get_file_content_as_string(path):
        return open(path, "r", encoding="utf-8").read()


else:

    @st.cache(show_spinner=False)
    def get_file_content_as_string(path):
        global DATA_URL_ROOT
        url = DATA_URL_ROOT + path
        response = urllib.request.urlopen(url)
        return response.read().decode("utf-8")


@st.cache(show_spinner=False)
def convert_df(df, encoding):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode(encoding=encoding)


@st.cache(show_spinner=True)
def cached_search(queries):
    result, fail_list = queries_to_results(queries)
    return result, fail_list


def show_result(queries):
    result, fail_list = queries_to_results(queries)
    df = pd.DataFrame.from_dict(result, orient="index")
    st.dataframe(data=df, width=None, height=None)
    if len(fail_list) > 0:
        st.text("Fail: \n" + "\n".join(fail_list))
    return df


def main():
    # Once we have the dependencies, add a selector for the app mode on the sidebar.
    md_guide = st.markdown(get_file_content_as_string("guide.md"))
    txt_queries = st.text_area(label="단어들을 줄로 나눠서 입력하세요", value="sweet\ncocoa\nひらがな\n손")
    encoding = st.radio(label="인코딩(모르면 그냥 두세요)", index=0, options=("cp949", "utf-8"))

    csv_data = None
    if st.button("검색하기"):
        df = show_result(txt_queries.split())
        csv_data = convert_df(df, encoding)
    if csv_data is not None:

        st.download_button(
            label="엑셀로 다운", data=csv_data, file_name="words_means.csv", mime="text/csv"
        )


if __name__ == "__main__":
    main()
