# test_new_process.py

from app.new_process import preprocess_image

def main():
    # 替换为你本地的一张测试图像路径
    image_path = "test_face.jpg"

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        result = preprocess_image(image_bytes)

        if result is not None:
            print("✅ 预处理成功，输出 shape:", result.shape)
        else:
            print("❌ 无法处理图像（可能无人脸）")

    except Exception as e:
        print(f"❌ 程序运行出错：{e}")

if __name__ == "__main__":
    main()
