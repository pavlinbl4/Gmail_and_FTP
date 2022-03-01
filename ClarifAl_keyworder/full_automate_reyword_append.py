from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from cred import key
from deep_translator import GoogleTranslator
import pyexiv2
import os


def get_keywords(file_path):
    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
    api_key = key
    metadata = (('authorization', f'Key {api_key}'),)

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    request = service_pb2.PostModelOutputsRequest(
        model_id='general-image-recognition',
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                )
            )
        ])
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Request failed, status code: " + str(response.status.code))

    keywords = []
    for concept in response.outputs[0].data.concepts:
        keywords.append(concept.name)
    return keywords


def translate_english(keywords):  # принимает список с ключевыми словами
    return GoogleTranslator(source='en', target='ru').translate_batch(keywords)


def add_keywords(new_keywords, file_path):  # добавляет новые ключевые слова
    changes = {}
    with open(file_path, 'rb+') as image_file:
        with pyexiv2.ImageData(image_file.read()) as meta_data:
            data = meta_data.read_xmp()
            old_keywords = data.get('Xmp.dc.subject', [])
            changes['Xmp.dc.subject'] = list(set(old_keywords + new_keywords))
            meta_data.modify_xmp(changes)
            image_file.seek(0)
            image_file.truncate()
            image_file.write(meta_data.get_bytes())
        image_file.seek(0)


image_folder = "/Volumes/big4photo-2/My photo 2022/add_keywords"
files = os.listdir(image_folder)
for file in files:
    if file.endswith('.JPG'):
        file_path = f"{image_folder}/{file}"
        new_keywords = translate_english(get_keywords(file_path))  # перевожу ключевые слова на русский
        new_keywords = [word.lower() for word in new_keywords]  # перевожу слова в нижний регистр
        add_keywords(new_keywords, file_path)


