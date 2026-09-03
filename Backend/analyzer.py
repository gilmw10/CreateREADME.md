import json


def analyze_requirements(
    requirements_text: str
):
    tech_stack = []

    if not requirements_text:
        return tech_stack

    text = requirements_text.lower()

    mapping = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "sqlalchemy": "SQLAlchemy",
        "pydantic": "Pydantic",
        "django": "Django",
        "flask": "Flask",
        "pytest": "Pytest",
        "numpy": "NumPy",
        "pandas": "Pandas",
        "requests": "Requests",
        "httpx": "HTTPX",
        "psycopg": "PostgreSQL",
        "asyncpg": "PostgreSQL"
    }

    for keyword, name in mapping.items():
        if keyword in text:
            tech_stack.append(name)

    return tech_stack


def analyze_package_json(
    package_json_text: str
):
    tech_stack = []

    if not package_json_text:
        return tech_stack

    try:
        package_data = json.loads(
            package_json_text
        )

        dependencies = package_data.get(
            "dependencies",
            {}
        )

        dev_dependencies = package_data.get(
            "devDependencies",
            {}
        )

        all_dependencies = {
            **dependencies,
            **dev_dependencies
        }

        mapping = {
            "react": "React",
            "next": "Next.js",
            "vue": "Vue",
            "axios": "Axios",
            "typescript": "TypeScript",
            "tailwindcss": "TailwindCSS",
            "vite": "Vite",
            "express": "Express",
            "prisma": "Prisma"
        }

        for keyword, name in mapping.items():
            if keyword in all_dependencies:
                tech_stack.append(name)

    except json.JSONDecodeError:
        pass

    return tech_stack