import os
import json
import httpx

from dotenv import load_dotenv
from analyzer import (
    analyze_requirements,
    analyze_package_json
)

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json"
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


async def github_get(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=HEADERS
        )

    response.raise_for_status()

    return response.json()


async def download_file(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        return None

    return response.text


async def get_file_content(
    owner: str,
    repo: str,
    path: str
):
    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{path}"
    )

    file_info = await github_get(url)

    download_url = file_info.get(
        "download_url"
    )

    if not download_url:
        return None

    return await download_file(
        download_url
    )


async def get_analysis(
    owner: str,
    repo: str
):

    repo_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}"
    )

    repo_info = await github_get(
        repo_url
    )

    default_branch = repo_info[
        "default_branch"
    ]

    tree_url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/git/trees/"
        f"{default_branch}?recursive=1"
    )

    tree_data = await github_get(
        tree_url
    )

    all_files = [
        item["path"]
        for item in tree_data["tree"]
        if item["type"] == "blob"
    ]

    requirements_files = [
        path
        for path in all_files
        if path.endswith("requirements.txt")
    ]

    package_files = [
        path
        for path in all_files
        if path.endswith("package.json")
    ]

    requirements_text = None
    package_json_text = None

    if requirements_files:
        requirements_text = (
            await get_file_content(
                owner,
                repo,
                requirements_files[0]
            )
        )

    if package_files:
        package_json_text = (
            await get_file_content(
                owner,
                repo,
                package_files[0]
            )
        )

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

    tech_stack = list(
        set(tech_stack)
    )

    return {
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
            "stars": repo_info.get(
                "stargazers_count"
            )
        },
        "tech_stack": tech_stack,
        "files": all_files[:100],
        "requirements_txt": requirements_text,
        "package_json": package_json_text
    }