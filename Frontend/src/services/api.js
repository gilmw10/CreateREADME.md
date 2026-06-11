const BASE_URL = 'http://localhost:8000';

export async function analyzeRepo(owner, repo) {
  const response = await fetch(`${BASE_URL}/github/${owner}/${repo}`);

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const errorData = await response.json();
      if (errorData.detail) message = errorData.detail;
      else if (errorData.message) message = errorData.message;
    } catch {
    }
    throw new Error(message);
  }

  return response.json();
}

export async function generateReadme(owner, repo) {
  const response = await fetch(`${BASE_URL}/readme/${owner}/${repo}`);

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const errorData = await response.json();
      if (errorData.detail) message = errorData.detail;
      else if (errorData.message) message = errorData.message;
    } catch {
    }
    throw new Error(message);
  }

  return response.json();
}
