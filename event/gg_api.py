from google.cloud import translate_v2 as translate

from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    translate_client = translate.Client()
    result = translate_client.translate(
        ["你好", "再见"],
        source_language='zh',
        target_language='vi'
    )
    print(result['translatedText'])