import { useState } from 'react';
import styles from './RepoForm.module.css';

export default function RepoForm({ onSubmit, loading }) {
  const [owner, setOwner] = useState('');
  const [repo, setRepo] = useState('');
  const [urlInput, setUrlInput] = useState('');

  function parseGitHubUrl(value) {
    try {
      const url = new URL(value);
      if (url.hostname === 'github.com') {
        const parts = url.pathname.replace(/^\//, '').split('/');
        if (parts.length >= 2) {
          setOwner(parts[0]);
          setRepo(parts[1]);
          setUrlInput('');
        }
      }
    } catch {
      // not a valid URL
    }
  }

  function handleUrlChange(e) {
    const value = e.target.value;
    setUrlInput(value);
    parseGitHubUrl(value);
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (!owner.trim() || !repo.trim()) return;
    onSubmit(owner.trim(), repo.trim());
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div className={styles.row}>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="owner">GitHub UserName</label>
          <input
            id="owner"
            className={styles.input}
            type="text"
            placeholder="abcd1234"
            value={owner}
            onChange={(e) => setOwner(e.target.value)}
            disabled={loading}
            required
          />
        </div>
        <div className={styles.separator}>/</div>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="repo">Repository</label>
          <input
            id="repo"
            className={styles.input}
            type="text"
            placeholder="project1"
            value={repo}
            onChange={(e) => setRepo(e.target.value)}
            disabled={loading}
            required
          />
        </div>
      </div>

      <div className={styles.urlSection}>
        <label className={styles.label} htmlFor="url">GitHub Repository URL</label>
        <input
          id="url"
          className={styles.inputFull}
          type="text"
          placeholder="https://github.com/user_name/repository_name"
          value={urlInput}
          onChange={handleUrlChange}
          disabled={loading}
        />
      </div>

      <div className={styles.btnWrap}>
        <button className={styles.submitBtn} type="submit" disabled={loading || !owner || !repo}>
          CREATE
        </button>
      </div>
    </form>
  );
}
