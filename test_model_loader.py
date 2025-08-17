from app.model_loader import predict_all

def main():
    with open("test_face.jpg", "rb") as f:
        image_bytes = f.read()

    result = predict_all(image_bytes)
    print("🎯 最终预测结果:", result)

if __name__ == "__main__":
    main()
