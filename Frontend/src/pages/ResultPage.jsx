import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Header from '../components/Header';
import Footer from '../components/Footer';
import styles from './ResultPage.module.css';

export default function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state;
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!state?.data) {
      navigate('/', { replace: true });
    }
  }, [state, navigate]);

  if (!state?.data) return null;

  const { data } = state;
  const markdown = data.readme || '';
  const repoName = data.repository || 'Repository';

  function handleCopy() {
    navigator.clipboard.writeText(markdown).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  function handleDownload() {
    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'README.md';
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className={styles.page}>
      <Header />
      <div className={styles.toolbar}>
        <button className={styles.btnBack} onClick={() => navigate('/create')}>
          ← New Create
        </button>
        <div className={styles.btnGroup}>
          <button className={styles.btnDownload} onClick={handleDownload}>
            DOWNLOAD
          </button>
          <button className={styles.btnCopy} onClick={handleCopy}>
            {copied ? 'COPIED!' : 'COPY'}
          </button>
        </div>
      </div>
      <main className={styles.main}>
        <div className={styles.card}>
          <h1 className={styles.repoTitle}>{repoName}</h1>
          <hr className={styles.divider} />
          <div className={styles.content}>
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {markdown}
            </ReactMarkdown>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
