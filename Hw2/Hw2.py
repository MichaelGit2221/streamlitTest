import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import streamlit as st
from scipy import stats
from scipy.stats import mannwhitneyu
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats import power


def check_categories(data_frame, col1, col2):
    if data_frame[col1].dtype != 'object' or data_frame[col2].dtype == 'object':
        st.write(
            '\n**Для работы данного алгоритма нужно: Сделать первую колонку категориальной, Вторая колонка должна быть некатегориальной (Самые первые два dropdown)**')
        return True
    return False


def choose_test(data_frame, col1, col2):
    st.write(
        '\n\n**A/B тестирование\n Здесь выбираются группы из колонок для теста.**')
    st.write('Для теста из выбранных ранее колонок первая должна быть категориальная, вторая колонка может быть некатегориальной/категориальной\n\n')
    st.write('Выбор группы из колонок\n')
    a = st.selectbox(
        "Выбор группы A из 1 колонки", data_frame[col1])
    b = st.selectbox(
        "Выбор группы B из 1 колонки", data_frame[data_frame[col1] != a][col1])
    st.write('\n\n')
    algo = st.selectbox(
        "Выбор алгоритма для теста гипотез",
        [
            "t-test",
            "mann-whitney U-test",

        ]

    )
    if algo == "t-test":
        if check_categories(data_frame, col1, col2):
            return
        tstat, pvalue, df = sm.stats.ttest_ind(
            data_frame.loc[data_frame[col1] == a][col2],
            data_frame.loc[data_frame[col1] == b][col2],
            usevar='unequal', alternative='smaller')
        st.write(f'p-value: {pvalue:.4f}')

    elif algo == "mann-whitney U-test":
        if check_categories(data_frame, col1, col2):
            st.write('**!!!**')
            return
        man = mannwhitneyu(data_frame[data_frame[col1] == a][col2],
                           data_frame[data_frame[col1] == b][col2])
        st.write(man)


def dataset_menu(data_frame, name):
    columns_labels = data_frame.columns
    sd = st.selectbox(name, list(columns_labels))
    fig = plt.figure(figsize=(12, 6))
    if data_frame[sd].dtype != 'object':
        chart = sns.violinplot(x=data_frame[sd])
    else:
        valcounts = data_frame[sd].value_counts().nlargest(15)
        labels = valcounts.index.to_list()
        chart = plt.pie(
            valcounts, labels=labels, autopct='%1.1f%%', textprops={'fontsize': 14})
    st.pyplot(fig)
    return sd


def run():
    st.title("Домашнее задание 2.0")
    html_temp = """

    """
    dataset_filename = st.file_uploader("Выберите CSV файл")
    if dataset_filename is not None:
        data_frame = pd.read_csv(dataset_filename)
        col1 = dataset_menu(data_frame, 'Выбор колонки 1')
        col2 = dataset_menu(data_frame, 'Выбор колонки 2')
        choose_test(data_frame, col1, col2)


if __name__ == '__main__':
    run()
