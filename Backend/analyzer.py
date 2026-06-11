import json


def analyze_requirements(requirements_text: str):
    result = []

    if not requirements_text:
        return result

    text = requirements_text.lower()

    mapping = {
        "fastapi": "FastAPI",
        "uvicorn": "Uvicorn",
        "sqlalchemy": "SQLAlchemy",
        "pydantic": "Pydantic",
        "django": "Django",
        "flask": "Flask",
        "pytest": "Pytest",
    }

    for key, value in mapping.items():
        if key in text:
            result.append(value)

    return result


def analyze_package_json(package_json_text: str):
    result = []

    if not package_json_text:
        return result

    try:
        package_data = json.loads(package_json_text)

        deps = package_data.get("dependencies", {})
        dev_deps = package_data.get("devDependencies", {})

        all_deps = {**deps, **dev_deps}

        mapping = {
            "react": "React",
            "next": "Next.js",
            "axios": "Axios",
            "typescript": "TypeScript",
            "tailwindcss": "TailwindCSS",
            "vite": "Vite",
            "express": "Express"
        }

        for key, value in mapping.items():
            if key in all_deps:
                result.append(value)

    except Exception:
        pass

    return result