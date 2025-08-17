# test_preprocess.py

from preprocess import preprocess_image

def main():
    # 替换为你本地的一张测试图像路径
    image_path = "test_face.jpg"

    # 读取图片为 bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    try:
        result = preprocess_image(image_bytes)
        print(f"✅ 预处理成功，输出 shape: {result.shape}")
    except Exception as e:
        print(f"❌ 预处理失败：{e}")

if __name__ == "__main__":
    main()
if result is None:
    print("❌ 无法处理该图像（无脸 / 错误）")