from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from github_service import get_analysis
from ai_service import generate_readme


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://create-readme-md-theta.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )