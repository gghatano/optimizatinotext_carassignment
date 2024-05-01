import streamlit as st
import pandas as pd
from car_assign import optimize_car_assignment

ss = st.session_state

# 状態変数==================================
if 'now' not in ss:     # 初期化
    ss.now = 0          # 初期化
def countup():          # コールバック関数(1/3):次へ
    ss.now += 1
def countdown():        # コールバック関数(2/3):戻る
    ss.now -= 1
def reset():            # コールバック関数(3/3):リセット
    ss.now = 0

# UIパーツ=================================
def buttons(now):
    col = st.columns(3)
    if ss.now > 0:
        col[0].button('前へ戻る', on_click=countdown)
    if ss.now < 3:
        col[2].button('次へ進む', on_click=countup)
    if ss.now > 1:
        col[1].button('はじめから', on_click=reset)

# サンプルデータ=================================
sample_cars_data = pd.DataFrame({
    'car_id': [0, 1,],
    'capacity': [4, 5,]
})
sample_students_data = pd.DataFrame({
    'student_id': [0, 1, 2, 3, 4, 5, 6, 7],
    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Gin', 'Hay'],
    'grade': [1, 1, 2, 2, 3, 3, 4, 4,],
    'gender': ['F', 'F', 'F', 'F', 'M', 'M', 'M', 'M'],
    'license': [False, False, False, False, True, True, True, True]
})

# アプリ本体=================================
st.title('サークル旅行の車配置アプリ')

if ss.now == 0:
    st.write('#### ステップ1: データのアップロード')

    # 車データのアップロード
    uploaded_car_file = st.file_uploader("車データのアップロード", type=['csv'])
    
    # 車データのサンプルデータダウンロードボタン
    st.download_button(
        label='車データのサンプルダウンロード',
        data=sample_cars_data.to_csv(index=False),
        file_name='sample_car_data.csv',
        mime='text/csv'
    )

    # 学生データのアップロード
    uploaded_student_file = st.file_uploader("学生データのアップロード", type=['csv'])
    
    # 学生データのサンプルデータダウンロードボタン
    st.download_button(
        label='学生データのサンプルダウンロード',
        data=sample_students_data.to_csv(index=False),
        file_name='sample_student_data.csv',
        mime='text/csv'
    )
    
    if uploaded_car_file is not None and uploaded_student_file is not None:
        ss.car_df = pd.read_csv(uploaded_car_file)
        ss.student_df = pd.read_csv(uploaded_student_file)
        st.write('車データ')
        st.write(ss.car_df)
        st.write('学生データ')
        st.write(ss.student_df)
    buttons(ss.now)

elif ss.now == 1:
    st.write('#### ステップ2: 制約の入力')
    st.write('同じ車に乗せる学生のIDを入力してください（例: (1,2),(1,3)）')
    pair_together = st.text_input('ペア（カンマ区切り）', key='pair_together')
    st.write('同じ車に乗せない学生のIDを入力してください（例: (3,4),(5,6)）')
    pair_separate = st.text_input('ペア（カンマ区切り）', key='pair_separate')
    buttons(ss.now)

elif ss.now == 2:
    st.write('#### ステップ3: 配置問題の解決')
    if 'car_df' in ss and 'student_df' in ss:
        assignment = optimize_car_assignment(ss.car_df, ss.student_df)

        # 車IDをキーとし、割り当てられた学生のリストを値とする辞書を作成
        car_assignments = {}
        for student_id, car_id in assignment.items():
            if car_id not in car_assignments:
                car_assignments[car_id] = []
            car_assignments[car_id].append(student_id)

        # 結果の表示
        for car_id, student_ids in car_assignments.items():
            st.write(f"車 {car_id}:")
            student_names = []
            for student_id in student_ids:
                student = ss.student_df[ss.student_df['student_id'] == student_id].iloc[0]
                name = student['name']
                gender = student['gender']
                license = student['license']
                if license:
                    name = f"⭐ {name}"
                if gender == 'M':
                    name = f"<font color='blue'>{name}</font>"
                else:
                    name = f"<font color='red'>{name}</font>"
                student_names.append(name)
            st.write(', '.join(student_names), unsafe_allow_html=True)
            st.write('')  # 改行
    else:
        st.warning('車データと学生データをアップロードしてください')
    buttons(ss.now)

else:
    st.write('### 完了！')
    st.success('全てのステップが完了しました')
    buttons(ss.now)
