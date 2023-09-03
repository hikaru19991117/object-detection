from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import os
from PIL import Image
import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont
import logging

# ログの設定
logging.basicConfig(
    filename=r"C:\Users\池田　光\OneDrive\デスクトップ\python_test\物体検出アプリ\log\app.log",
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# KEYの設定
subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# タグの取得
def get_tags(filepath):
    local_image = open(filepath, "rb")

    Tag_result = computervision_client.tag_image_in_stream(local_image)
    tags = Tag_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)

    return tags_name

# オブジェクトの検出
def detect_objects(filepath):
    local_image = open(filepath, "rb")
    st.write(local_image)
    detect_result = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_result.objects

    return objects

try:
    st.title('物体検出アプリ')

    uploaded_file = st.file_uploader('Choose an image...',type=['jpg', 'png'])
    logging.info('処理開始')
    
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        img_path = f'img/{uploaded_file.name}'
        img.save(img_path)
        objects = detect_objects(img_path)

        # 描画
        draw = ImageDraw.Draw(img)
        for object in objects:
            x = object.rectangle.x
            y = object.rectangle.y
            w = object.rectangle.w
            h = object.rectangle.h
            caption = object.object_property

            font = ImageFont.truetype(font='./Helvetica 400.ttf', size=50, )
            text_w, text_h = draw.textsize(caption, font=font)

            draw.rectangle([(x, y), (x+w, y+h)], fill=None, outline='green', width=5)
            draw.rectangle([(x, y), (x+text_w, y+text_h)], fill='green')
            draw.text([x, y], caption, fill='white', font=font)

        st.image(img)
        tags_name = get_tags(img_path)
        tags_name = ', '.join(tags_name)

        st.markdown('**認識されたコンテンツタグ**')
        st.markdown(f'> {tags_name}')
        logging.info('処理正常実行')
except Exception as e:
    logging.error((f'Error: {e}'))
    st.write('エラーが起きています。')