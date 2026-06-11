import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import RepoForm from '../components/RepoForm';
import LoadingSpinner from '../components/LoadingSpinner';
import { useReadme } from '../hooks/useReadme';
import styles from './CreatePage.module.css';

export default function CreatePage() {
  const navigate = useNavigate();
  const { generate, data, loading, error } = useReadme();

  useEffect(() => {
    if (data) {
      navigate('/result', { state: { data } });
    }
  }, [data, navigate]);

  return (
    <div className={styles.page}>
      <Header />
      <main className={styles.main}>
        <div className={styles.card}>
          {loading ? (
            <LoadingSpinner />
          ) : (
            <>
              <RepoForm onSubmit={generate} loading={loading} />
              {error && <p className={styles.error}>{error}</p>}
            </>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}
