from fastapi import FastAPI, HTTPException

from github_service import get_analysis
from ai_service import generate_readme


app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "README Generator API"
    }


@app.get("/github/{owner}/{repo}")
async def analyze_repo(
    owner: str,
    repo: str
):
    try:
        analysis = await get_analysis(
            owner,
            repo
        )

        return analysis

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.get("/readme/{owner}/{repo}")
async def create_readme(
    owner: str,
    repo: str
):
    try:
        # GitHub 저장소 분석
        analysis = await get_analysis(
            owner,
            repo
        )

        # AI README 생성
        readme = await generate_readme(
            analysis
        )

        return {
            "repository": analysis[
                "repository"
            ]["name"],
            "readme": readme
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )