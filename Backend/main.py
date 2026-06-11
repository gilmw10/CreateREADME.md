from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from github_service import (
    get_analysis
)

from gemini_service import (
    generate_readme
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "README Generator API"
    }


@app.get(
    "/github/{owner}/{repo}"
)
async def analyze_repo(
    owner: str,
    repo: str
):
    return await get_analysis(
        owner,
        repo
    )


@app.get(
    "/readme/{owner}/{repo}"
)
async def create_readme(
    owner: str,
    repo: str
):

    analysis = await get_analysis(
        owner,
        repo
    )

    readme = await generate_readme(
        analysis
    )

    return {
        "repository": analysis[
            "repository"
        ]["name"],
        "readme": readme
    }