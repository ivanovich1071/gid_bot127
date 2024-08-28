import os

def choose_image_by_temperature(temperature):
    if 20 <= temperature <= 50:
        return "photo/sunnycity.jpeg"
    elif -50 <= temperature < 0:
        return "photo/snowycity.jpeg"
    elif 0 <= temperature < 10:
        return "photo/rainycity.jpeg"
    elif 10 <= temperature < 20:
        return "photo/springcity.jpeg"
    else:
        return None
