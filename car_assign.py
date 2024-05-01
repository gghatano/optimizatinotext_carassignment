import pandas as pd
import pulp

def optimize_car_assignment(cars_df, students_df):
    # 問題のインスタンス作成
    prob = pulp.LpProblem('ClubCarProblem', pulp.LpMinimize)

    # リストの定義
    S = students_df['student_id'].tolist()
    C = cars_df['car_id'].tolist()
    G = [1, 2, 3, 4]
    SC = [(s, c) for s in S for c in C]
    S_license = students_df[students_df['license']==True]['student_id'].tolist()
    S_g = {g: students_df[students_df['grade']==g]['student_id'].tolist() for g in G}
    S_male = students_df[students_df['gender']=='M']['student_id'].tolist()
    S_female = students_df[students_df['gender']=='F']['student_id'].tolist()

    # 定数の定義
    U = cars_df['capacity'].tolist()

    # 変数の定義
    x = pulp.LpVariable.dicts('x', SC, cat='Binary')

    # 制約条件の定義
    # (1) 各学生を1つの車に割り当てる
    for s in S:
        prob += pulp.lpSum([x[s, c] for c in C]) == 1

    # (2) 法規制に関する制約：各車には乗車定員より多く乗ることができない
    for c in C:
        prob += pulp.lpSum([x[s, c] for s in S]) <= U[c]

    # (3) 法規制に関する制約：各車にドライバーを1人以上割り当てる
    for c in C:
        prob += pulp.lpSum([x[s, c] for s in S_license]) >= 1

    # (4) 懇親を目的とした制約：各車に各学年の学生を1人以上割り当てる
    for c in C:
        for g in G:
            prob += pulp.lpSum([x[s, c] for s in S_g[g]]) >= 1

    # (5) ジェンダーバランスを考慮した制約：各車に男性を1人以上割り当てる
    for c in C:
        prob += pulp.lpSum([x[s, c] for s in S_male]) >= 1

    # (6) ジェンダーバランスを考慮した制約：各車に女性を1人以上割り当てる
    for c in C:
        prob += pulp.lpSum([x[s, c] for s in S_female]) >= 1

    # 問題の求解
    status = prob.solve()
    print('Status:', pulp.LpStatus[status])

    # 結果の出力
    assignment = {}
    for s in S:
        for c in C:
            if x[s, c].value() == 1:
                assignment[s] = c

    return assignment
