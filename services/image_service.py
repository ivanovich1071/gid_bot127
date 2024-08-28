import os


def choose_image_by_temperature(temperature):
    try:
        if 20 <= temperature <= 50:
            path = "photo/sunnycity.jpeg"
        elif -50 <= temperature < 0:
            path = "photo/snowycity.jpeg"
        elif 0 <= temperature < 10:
            path = "photo/rainycity.jpeg"
        elif 10 <= temperature < 20:
            path = "photo/springcity.jpeg"
        else:
            path = None

        if path:
            if not os.path.exists(path):
                # Запасной вариант
                path = "photo/default.jpeg"
                if not os.path.exists(path):
                    raise FileNotFoundError(f"Image file not found: {path}")

        return path
    except Exception as e:
        print(f"Error: {e}")
        return None

