import { useState, useCallback } from 'react';
import { generateReadme } from '../services/api';

export function useReadme() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generate = useCallback(async (owner, repo) => {
    setLoading(true);
    setError(null);

    try {
      const result = await generateReadme(owner, repo);
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setData(null);
    setError(null);
  }, []);

  return { generate, data, loading, error, reset };
}
