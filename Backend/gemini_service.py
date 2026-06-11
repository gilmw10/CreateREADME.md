import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)


async def generate_readme(
    analysis: dict
):

    prompt = f"""
너는 시니어 개발자다.

다음 GitHub 프로젝트를
분석하여 README.md를 작성해라.

반드시 포함:

# 프로젝트 소개
# 주요 기능
# 기술 스택
# 설치 방법
# 실행 방법
# 프로젝트 구조

Markdown만 출력해라.

분석 데이터:

{json.dumps(
    analysis,
    ensure_ascii=False,
    indent=2
)}
"""

    response = (
        client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    )

    return response.text