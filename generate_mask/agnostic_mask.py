import os
import time
from huggingface_hub import snapshot_download
from model.cloth_masker import AutoMasker


def get_mask(image, cloth_type):
    repo_path = "zhengchong/CatVTON"
    repo_path = snapshot_download(repo_id=repo_path)

    automasker = AutoMasker(
        densepose_ckpt=os.path.join(repo_path, "DensePose"),
        schp_ckpt=os.path.join(repo_path, "SCHP"),
        device="cpu",
    )

    print("this is automasker: ", automasker)

    mask = automasker(image, cloth_type)["mask"]

    print("this is mask: ", mask)

    output_dir = "./mask_results"
    os.makedirs(output_dir, exist_ok=True)
    new_image_name = f"{os.path.basename(image).replace('.jpg', '')}_{cloth_type}.png"
    mask.save(os.path.join(output_dir, new_image_name))


if __name__ == "__main__":
    start = time.time()

    for i in ["upper", "lower", "overall"]:
        get_mask("mantest.jpg", i)

    print("Time taken: ", time.time() - start)
