import os

import httpx

from dotenv import load_dotenv

from analyzer import (
    analyze_requirements,
    analyze_package_json
)


load_dotenv()


GITHUB_TOKEN = os.getenv(
    "GITHUB_TOKEN"
)


HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}


if GITHUB_TOKEN:
    HEADERS["Authorization"] = (
        f"Bearer {GITHUB_TOKEN}"
    )


async def github_get(
    url: str
):
    async with httpx.AsyncClient(
        timeout=20.0
    ) as client:
        response = await client.get(
            url,
            headers=HEADERS
        )

    if response.status_code == 404:
        raise Exception(
            "GitHub 저장소 또는 파일을 찾을 수 없습니다."
        )

    if response.status_code == 401:
        raise Exception(
            "GitHub 토큰이 올바르지 않습니다."
        )

    if response.status_code == 403:
        raise Exception(
            "GitHub API 요청 한도를 초과했거나 "
            "접근 권한이 없습니다."
        )

    response.raise_for_status()

    return response.json()


async def get_file_content(
    owner: str,
    repo: str,
    path: str
):
    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{path}"
    )

    try:
        file_info = await github_get(
            url
        )

    except Exception:
        return None

    if not isinstance(
        file_info,
        dict
    ):
        return None

    download_url = file_info.get(
        "download_url"
    )

    if not download_url:
        return None

    try:
        async with httpx.AsyncClient(
            timeout=20.0
        ) as client:
            response = await client.get(
                download_url
            )

        if response.status_code != 200:
            return None

        return response.text

    except httpx.RequestError:
        return None


def find_file(
    all_files: list,
    filename: str
):
    matches = [
        path
        for path in all_files
        if path.lower().endswith(
            filename.lower()
        )
    ]

    if not matches:
        return None

    # 루트 디렉토리에 가까운 파일 우선
    matches.sort(
        key=lambda path: (
            path.count("/"),
            len(path)
        )
    )

    return matches[0]


def shorten_text(
    text: str | None,
    max_length: int
):
    if not text:
        return None

    if len(text) <= max_length:
        return text

    return (
        text[:max_length]
        + "\n\n[내용 일부 생략]"
    )


async def get_analysis(
    owner: str,
    repo: str
):
    # --------------------------
    # 1. 저장소 정보
    # --------------------------

    repo_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}"
    )

    repo_info = await github_get(
        repo_url
    )

    default_branch = repo_info.get(
        "default_branch"
    )

    if not default_branch:
        raise Exception(
            "기본 브랜치를 확인할 수 없습니다."
        )

    # --------------------------
    # 2. 전체 파일 트리
    # --------------------------

    tree_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/git/trees/"
        f"{default_branch}?recursive=1"
    )

    tree_data = await github_get(
        tree_url
    )

    tree = tree_data.get(
        "tree",
        []
    )

    all_files = [
        item["path"]
        for item in tree
        if (
            item.get("type") == "blob"
            and item.get("path")
        )
    ]

    # --------------------------
    # 3. 주요 파일 찾기
    # --------------------------

    requirements_path = find_file(
        all_files,
        "requirements.txt"
    )

    package_json_path = find_file(
        all_files,
        "package.json"
    )

    main_py_path = find_file(
        all_files,
        "main.py"
    )

    app_py_path = find_file(
        all_files,
        "app.py"
    )

    dockerfile_path = find_file(
        all_files,
        "Dockerfile"
    )

    # --------------------------
    # 4. 주요 파일 읽기
    # --------------------------

    requirements_text = None

    if requirements_path:
        requirements_text = (
            await get_file_content(
                owner,
                repo,
                requirements_path
            )
        )

    package_json_text = None

    if package_json_path:
        package_json_text = (
            await get_file_content(
                owner,
                repo,
                package_json_path
            )
        )

    main_py_text = None

    if main_py_path:
        main_py_text = (
            await get_file_content(
                owner,
                repo,
                main_py_path
            )
        )

    app_py_text = None

    if app_py_path:
        app_py_text = (
            await get_file_content(
                owner,
                repo,
                app_py_path
            )
        )

    dockerfile_text = None

    if dockerfile_path:
        dockerfile_text = (
            await get_file_content(
                owner,
                repo,
                dockerfile_path
            )
        )

    # --------------------------
    # 5. 기술 스택 분석
    # --------------------------

    tech_stack = []

    tech_stack.extend(
        analyze_requirements(
            requirements_text
        )
    )

    tech_stack.extend(
        analyze_package_json(
            package_json_text
        )
    )

    github_language = repo_info.get(
        "language"
    )

    if github_language:
        tech_stack.append(
            github_language
        )

    if dockerfile_path:
        tech_stack.append(
            "Docker"
        )

    # 순서 유지하며 중복 제거
    tech_stack = list(
        dict.fromkeys(
            tech_stack
        )
    )

    # --------------------------
    # 6. 프로젝트 종류 추론
    # --------------------------

    project_type = "Unknown"

    python_source = (
        (main_py_text or "")
        + "\n"
        + (app_py_text or "")
    )

    if "FastAPI(" in python_source:
        project_type = "FastAPI Backend"

    elif "Flask(" in python_source:
        project_type = "Flask Backend"

    if "React" in tech_stack:
        if project_type == "Unknown":
            project_type = "React Frontend"

        else:
            project_type += (
                " + React Frontend"
            )

    if "Next.js" in tech_stack:
        project_type = (
            "Next.js Project"
        )

    # --------------------------
    # 7. AI 전송용 데이터 압축
    # --------------------------

    # 파일 구조는 최대 50개만 전달
    files_for_ai = all_files[:50]

    # AI가 기술/실행 방식을 파악할 정도만 전달
    requirements_for_ai = shorten_text(
        requirements_text,
        2500
    )

    package_json_for_ai = shorten_text(
        package_json_text,
        3500
    )

    main_py_for_ai = shorten_text(
        main_py_text,
        2500
    )

    app_py_for_ai = shorten_text(
        app_py_text,
        2500
    )

    dockerfile_for_ai = shorten_text(
        dockerfile_text,
        1200
    )

    # --------------------------
    # 8. 최종 분석 결과
    # --------------------------

    analysis = {
        "repository": {
            "name": repo_info.get(
                "name"
            ),
            "description": repo_info.get(
                "description"
            ),
            "language": repo_info.get(
                "language"
            ),
            "default_branch": default_branch
        },

        "project_type": project_type,

        "tech_stack": tech_stack,

        "files_count": len(
            all_files
        ),

        "files": files_for_ai,

        "important_files": {
            "requirements": (
                requirements_path
            ),
            "package_json": (
                package_json_path
            ),
            "main_py": (
                main_py_path
            ),
            "app_py": (
                app_py_path
            ),
            "dockerfile": (
                dockerfile_path
            )
        },

        "requirements_txt": (
            requirements_for_ai
        ),

        "package_json": (
            package_json_for_ai
        ),

        "main_py_excerpt": (
            main_py_for_ai
        ),

        "app_py_excerpt": (
            app_py_for_ai
        ),

        "dockerfile": (
            dockerfile_for_ai
        )
    }

    return analysis