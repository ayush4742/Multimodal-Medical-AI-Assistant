import os

from brain_of_the_doctor import (
    encode_image,
    analyze_image_with_query
)

DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def analyze_image(
    image_path,
    prompt,
    model=DEFAULT_MODEL
):
    """
    Vision Wrapper
    """

    if image_path is None:
        return None

    if not os.path.exists(image_path):
        return None

    try:

        encoded_image = encode_image(
            image_path
        )

        response = analyze_image_with_query(

            query=prompt,

            encoded_image=encoded_image,

            model=model

        )

        return response

    except Exception as e:

        print(f"[VISION ERROR] {e}")

        return None


def analyze_image_safe(
    image_path,
    prompt
):

    result = analyze_image(
        image_path,
        prompt
    )

    if result is None:

        return "No image analysis available."

    return result


def health_check():

    return True


if __name__ == "__main__":

    prompt = """
Patient has red rashes on the face.
"""

    print(

        analyze_image_safe(

            "sample.jpg",

            prompt

        )

    )