import os
import time
from huggingface_hub import snapshot_download
from model.cloth_masker import AutoMasker
import json
import base64
from PIL import Image
from io import BytesIO
import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = str(os.environ["ACCESS_KEY_ID"])
AWS_SECRET_ACCESS_KEY = str(os.environ["SECRET_ACCESS_KEY"])

print(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

s3 = boto3.client(
    "s3",
    region_name="ap-northeast-2",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def save_and_upload_s3(mask, username, cloth_type, start_timestamp):

    output_dir = "/tmp/mask_results"
    os.makedirs(output_dir, exist_ok=True)

    # timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    new_image_name = f"{username}_{start_timestamp}_{cloth_type}.png"
    mask.save(os.path.join(output_dir, new_image_name))

    filename = os.path.join(output_dir, new_image_name)
    bucket_name = "githubsalt-bucket"
    object_name = f"{username}/{start_timestamp}/{cloth_type}.png"

    s3.upload_file(filename, bucket_name, object_name)


def get_mask(image, cloth_type, username, start_timestamp):
    repo_path = "zhengchong/CatVTON"
    repo_path = snapshot_download(repo_id=repo_path, cache_dir="/tmp/snapshot_cache")

    automasker = AutoMasker(
        densepose_ckpt=os.path.join(repo_path, "DensePose"),
        schp_ckpt=os.path.join(repo_path, "SCHP"),
        device="cpu",
    )

    image = base64.b64decode(image)
    image = Image.open(BytesIO(image))

    mask = automasker(image, cloth_type)["mask"]

    save_and_upload_s3(
        mask=mask,
        username=username,
        cloth_type=cloth_type,
        start_timestamp=start_timestamp,
    )


def handler(event, context):
    start = time.time()
    start_timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())

    body = event["body-json"]

    username = body["username"]
    img = body["img"]

    for cloth_type in ["upper", "lower", "overall", "inner", "outer"]:
        get_mask(
            image=img,
            cloth_type=cloth_type,
            username=username,
            start_timestamp=start_timestamp,
        )

    result = f"Hello, {username}"

    print("Time taken: ", time.time() - start)

    return {"statusCode": 200, "body": json.dumps(result)}


if __name__ == "__main__":
    start = time.time()

    with open("mantest.jpg", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    img = encoded_image

    for cloth_type in ["upper", "lower", "overall", "inner", "outer"]:
        get_mask(img, cloth_type, username="jongmin")

    print("Time taken: ", time.time() - start)
