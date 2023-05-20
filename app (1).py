# 以下を「app.py」に書き込み
import streamlit as st
import openai

openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀な奄美大島研究家です。
どんな質問されても、奄美大島に関連する情報を含めて回答します。
奄美大島に関連する情報を含めずに解答することは絶対にありません。
全ての回答は70文字以内で行います。
もし奄美大島と関係ない質問が来ても、まずその質問に回答したあとで、奄美大島に関連する情報を追加して回答します。
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
st.title("奄美のおっちゃん.bot")
st.write("なんでも話しかけてみてください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "👤"
        if message["role"]=="assistant":
            speaker="👨‍🦳"

        st.write(speaker + ": " + message["content"])
