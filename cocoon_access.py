import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
st.title('イチゲブログ、イチゲブログ別館2階の週間アクセス数（Cocoon集計値）')
st.caption('WordPress+テーマCocoonで運用しているブログ。データベースから取得して表示しています。')
st.markdown('###### 詳細は')
link = '[イチゲブログ](https://kikuichige.com/23946/)'
st.markdown(link, unsafe_allow_html=True)
selected_blog = st.selectbox("ブログを選択してください", ["イチゲブログ", "イチゲブログ別館2階"])
#csvをデータフレームで開く
if selected_blog == 'イチゲブログ':
    df = pd.read_csv("weekly_ona.csv",index_col=0)
    df1 = pd.read_csv('wp_posts_ona.csv', usecols=["ID","post_title"])
else:
    df = pd.read_csv("weekly.csv",index_col=0)
    df1 = pd.read_csv('wp_posts.csv', usecols=["ID","post_title"])
# 特定の列名を変更
df1.rename(columns={'ID': 'post_id'}, inplace=True)
# post_idをキーにして内部結合
# merged_df = pd.merge(df, df1, on='post_id', how='inner')

# df1だけにあるpost_idの行を削除
# merged_df = merged_df[merged_df['post_id'].isin(df1['post_id'])]
# post_id重複行を削除
# merged_df=merged_df.drop_duplicates(subset=['post_id'])
# 日付型 (datetime) に変換
df['date'] = pd.to_datetime(df['date'])
# 先週の日付を取得
last_week_start = df['date'].max() - pd.DateOffset(weeks=1)
last_week_end = last_week_start + pd.DateOffset(days=6)

# 先週のデータを抽出
last_week_data = df[(df['date'] >= last_week_start) & (df['date'] <= last_week_end)]

# 先週のアクセス数で降順に並び替え
last_week_sorted = last_week_data.sort_values(by='count', ascending=False)
# post_idをキーにして内部結合
merged_lastweek_df = pd.merge(last_week_sorted, df1, on='post_id', how='inner')

# df1だけにあるpost_idの行を削除
merged_lastweek_df = merged_lastweek_df[merged_lastweek_df['post_id'].isin(df1['post_id'])]
merged_df=merged_lastweek_df
# 記事選択post_id
# セレクトボックスでpost_titleを選択
selected_title1 = st.selectbox('post_titleを選択してください。アクセス数を表示します。（赤表示）', merged_df['post_title'], key='selectbox1')
# 選択されたpost_titleに対応するIDを取得
selected_id1 = merged_df[merged_df['post_title'] == selected_title1]['post_id'].values[0]
# 結果を表示
st.write(f'Selected Post ID: {selected_id1}')
# セレクトボックスでpost_titleを選択
selected_title2 = st.selectbox('post_titleを選択してください。アクセス数を表示します。（青表示）', merged_df['post_title'], key='selectbox2',index=1)
selected_id2 = merged_df[merged_df['post_title'] == selected_title2]['post_id'].values[0]

# 結果を表示
st.write(f'Selected Post ID: {selected_id2}')



# データフレーム選択
data = df

# 区間選択
start_date = st.date_input("開始日", value=date(2023, 10, 7))
end_date = st.date_input("終了日", value=date(2024, 2, 18))

# 散布図の表示
plt.figure(figsize=(10, 6))
plt.plot(data['date'][data['post_id'] == selected_id1], data['count'][data['post_id'] == selected_id1], color='red', label='Post ID '+str(selected_id1))
plt.plot(data['date'][data['post_id'] == selected_id2], data['count'][data['post_id'] == selected_id2], color='blue', label='Post ID '+str(selected_id2))
# y軸の最大値を指定
ymax=20
st.write(data['count'][data['post_id'] == selected_id1].max(),data['count'][data['post_id'] == selected_id2].max())
if data['count'][data['post_id'] == selected_id1].max()>ymax:
    ymax=data['count'][data['post_id'] == selected_id1].max()
if data['count'][data['post_id'] == selected_id2].max()>ymax:
    ymax=data['count'][data['post_id'] == selected_id2].max()
# y軸の範囲を0からymaxに設定（小数点になってしまう、それを直すため下にするとymaxが大きいとき見えなくなる）
# plt.ylim(0,ymax)  
# y軸の目盛を指定（ymaxが大きくなると見えなくなるので上をつかったほうがいい）
# np.arange(0, ymax+1, 1)は、0からymaxまでの範囲を1刻みで生成した配列です。この配列をyticksに渡すことで、y軸の目盛を1刻みで表示することができます。
if ymax>50:
    unit=5
else:
    unit=1
plt.yticks(np.arange(0, ymax+1, unit))
plt.xlabel('Date')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend()

# Set the x-axis limits
plt.xlim(start_date, end_date)

# Streamlitで表示
st.pyplot(plt)
# 水平線を表示
st.markdown("<hr>", unsafe_allow_html=True)
st.title('以下、管理人領域')
password = st.text_input("パスワードを入力してください", type="password")
correct_password = "mysecret"
if password == correct_password:
    st.success("CSVファイルをアップロードしてください。")
    uploaded_file1 = st.file_uploader("weekly.csvファイルのアップロード", type=["csv"], key="uploaded_file1")

    # アップロードされたファイルが存在する場合
    if uploaded_file1 is not None:
        # アップロードされたファイルをデータフレームに読み込む
        df7 = pd.read_csv(uploaded_file1,index_col=0) 

        # データフレームを保存
        df7.to_csv("weekly.csv")
        # st.success("weekly.CSVファイルをアップロードしてください。")

    uploaded_file2 = st.file_uploader("wp_posts.csvファイルのアップロード", type=["csv"], key="uploaded_file2")

    # アップロードされたファイルが存在する場合
    if uploaded_file2 is not None:
        # アップロードされたファイルをデータフレームに読み込む
        df8 = pd.read_csv(uploaded_file2,index_col=0) 

        # データフレームを保存
        df8.to_csv("wp_posts.csv")
        # st.success("wp_posts.csvファイルをアップロードしてください。")
    uploaded_file3 = st.file_uploader("weekly_ona.csvファイルのアップロード", type=["csv"], key="uploaded_file3")

    # アップロードされたファイルが存在する場合
    if uploaded_file3 is not None:
        # アップロードされたファイルをデータフレームに読み込む
        df7 = pd.read_csv(uploaded_file3,index_col=0) 

        # データフレームを保存
        df7.to_csv("weekly_ona.csv")

    uploaded_file4 = st.file_uploader("wp_posts_ona.csvファイルのアップロード", type=["csv"], key="uploaded_file4")

    # アップロードされたファイルが存在する場合
    if uploaded_file4 is not None:
        # アップロードされたファイルをデータフレームに読み込む
        df8 = pd.read_csv(uploaded_file4,index_col=0) 

        # データフレームを保存
        df8.to_csv("wp_posts_ona.csv")
else:
    st.error("パスワードが正しくありません。再試行してください。")


