import os
import json

from dotenv import load_dotenv
from groq import AsyncGroq


load_dotenv()


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY가 .env에 없습니다."
    )


client = AsyncGroq(
    api_key=GROQ_API_KEY
)


async def generate_readme(
    analysis: dict
):
    # AI에 꼭 필요한 데이터만 추림
    compact_analysis = {
        "repository": (
            analysis.get("repository")
        ),

        "project_type": (
            analysis.get("project_type")
        ),

        "tech_stack": (
            analysis.get("tech_stack")
        ),

        "files": (
            analysis.get("files", [])[:50]
        ),

        "important_files": (
            analysis.get("important_files")
        ),

        "requirements_txt": (
            analysis.get(
                "requirements_txt"
            )
        ),

        "package_json": (
            analysis.get(
                "package_json"
            )
        ),

        "main_py_excerpt": (
            analysis.get(
                "main_py_excerpt"
            )
        ),

        "app_py_excerpt": (
            analysis.get(
                "app_py_excerpt"
            )
        ),

        "dockerfile": (
            analysis.get(
                "dockerfile"
            )
        )
    }

    analysis_text = json.dumps(
        compact_analysis,
        ensure_ascii=False,
        indent=2
    )

    system_prompt = """
너는 GitHub 저장소를 분석하여
README.md를 작성하는 개발자다.

주어진 저장소 정보만 사용한다.

확인되지 않은 기능,
라이브러리,
실행 명령어는 만들지 않는다.

출력은 README.md 본문만 작성한다.
README 전체를 ```markdown 코드 블록으로
감싸지 않는다.

설명은 간결하고 실용적으로 작성한다.
"""

    user_prompt = f"""
다음 GitHub 저장소 분석 결과를 기반으로
README.md를 작성해라.

필요한 구성:

# 프로젝트 이름

프로젝트에 대한 짧은 소개

## 주요 기능

코드와 파일 구조에서 확인할 수 있는
기능만 작성

## 기술 스택

## 설치 방법

확실히 판단 가능한 설치 명령어만 작성

## 실행 방법

확실히 판단 가능한 실행 명령어만 작성

## 프로젝트 구조

중요한 파일을 중심으로 간단한
트리 구조 작성

규칙:

- 존재하지 않는 기능을 지어내지 않는다.
- 분석할 수 없는 내용은 억지로 작성하지 않는다.
- README에 불필요한 장문을 넣지 않는다.
- Markdown 본문만 반환한다.
- 프로젝트 구조에는 모든 파일을
  무조건 나열하지 않는다.

저장소 분석 결과:

{analysis_text}
"""

    response = await (
        client.chat.completions.create(
            model="openai/gpt-oss-20b",

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.2,

            max_completion_tokens=1800
        )
    )

    readme = (
        response
        .choices[0]
        .message
        .content
    )

    if not readme:
        raise Exception(
            "AI가 README를 생성하지 못했습니다."
        )

    return readme