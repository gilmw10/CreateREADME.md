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
    analysis_text = json.dumps(
        analysis,
        ensure_ascii=False,
        indent=2
    )

    system_prompt = """
너는 GitHub 저장소를 분석하여
정확하고 전문적인 README.md를 작성하는
시니어 소프트웨어 개발자다.

반드시 실제로 제공된 프로젝트 정보만 사용한다.

저장소에서 확인할 수 없는 기능이나
기술을 임의로 만들어내지 않는다.

설치 방법이나 실행 명령어를 확실하게
판단할 수 없는 경우에는 거짓 명령어를
만들지 않는다.

출력은 README.md 본문만 반환한다.
Markdown 코드블록으로 README 전체를
감싸지 않는다.
"""

    user_prompt = f"""
아래는 GitHub 저장소를 분석한 결과다.

이 정보를 기반으로 해당 프로젝트의
README.md를 작성해라.

[작성 규칙]

0. 이모티콘은 사용하지 않는다.

1. 가장 위에는 프로젝트 이름을
   # 제목 형식으로 작성한다.

2. 프로젝트 설명을 작성한다.

3. 실제 코드와 파일 구조에서 확인 가능한
   주요 기능을 정리한다.

4. 기술 스택을 정리한다.

5. 설치 방법을 작성한다.

6. 실행 방법을 작성한다.

7. 프로젝트 구조를 tree 형태의
   코드 블록으로 작성한다.

8. 필요한 경우 환경변수 설정 방법도 작성한다.

9. 분석 결과에 없는 기능을 지어내지 않는다.

10. 불필요한 문구나 AI가 작성했다는
    설명은 넣지 않는다.

11. README 본문만 출력한다.

[GitHub 저장소 분석 결과]

{analysis_text}
"""

    response = await (
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",

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

            max_completion_tokens=5000
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