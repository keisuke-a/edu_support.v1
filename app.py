# 以下を「app.py」に書き込み
import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは中学生と高校生の教育に関する優秀な研究者です。
私が指定した教育テーマに関して、Bloomのタキソノミーにおける「評価」の段階の目標を達成するような課題を5つ出力します。
教育と関係ない質問に対しては、決して回答することはありません。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("授業準備サポート.bot(中高生教員向け/ver.1)")
st.write("教科名と授業テーマを入力してください（例：）。Bloomタキソノミーにおける「評価」の段階の課題例を5つ出力します。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "👤"
        if message["role"]=="assistant":
            speaker="👨‍🦳"

        st.write(speaker + ": " + message["content"])
