import streamlit as st
import openai
import requests
from io import BytesIO
from PIL import Image
import os

openai.api_key = st.secrets["api_key"]

st.title("GET /api Module Project1")

if "image_url" not in st.session_state:
    st.session_state.image_url = None


with st.form("form"):
    user_input = st.text_input("Prompt")
    size = st.selectbox("Size", ["1024x1024", "512x512", "256x256"])
    submit = st.form_submit_button("Submit")


if submit and user_input:
    gpt_prompt = [{
        "role": "system",
        "content": "Imagine the detail appeareance of the input. Response it shortly around 20 words"
    }]

    gpt_prompt.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Waiting for ChatGPT..."):
        gpt_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt_prompt
        )

    prompt = gpt_response["choices"][0]["message"]["content"]
    st.write(prompt)

    with st.spinner("Waiting for DALL-E..."):
        dalle_response = openai.Image.create(
            prompt=prompt,
            size=size
        )
        st.session_state.image_url = dalle_response["data"][0]["url"]  # session_state에 저장
        st.image(st.session_state.image_url)  # 이미지 표시

if st.session_state.image_url:
        save = st.button("Save to Local", key="save_button")

        if save:
            # 이미지 데이터를 요청하여 가져오기
            image_data = requests.get(st.session_state.image_url).content
            image = Image.open(BytesIO(image_data))

            # 지정된 경로에 이미지 파일 저장
            save_path = "C:/Users/82104/Downloads/st"
            os.makedirs(save_path, exist_ok=True)  # 경로가 없으면 생성
            image_path = os.path.join(save_path, user_input+".png")
            image.save(image_path)

            st.success(f"Image saved locally at {image_path}")