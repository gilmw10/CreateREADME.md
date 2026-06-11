import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import RepoForm from '../components/RepoForm';
import LoadingSpinner from '../components/LoadingSpinner';
import { useReadme } from '../hooks/useReadme';
import styles from './HomePage.module.css';

const FEATURES = [
  { icon: '⚡', title: '빠른 분석', desc: '레포 구조를 즉시 분석합니다' },
  { icon: '🤖', title: 'AI 생성', desc: 'Gemini AI가 README를 작성합니다' },
  { icon: '📋', title: '즉시 복사', desc: '한 클릭으로 복사하고 사용하세요' },
];

export default function HomePage() {
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
        <section className={styles.hero}>
          <h1 className={styles.heading}>
            GitHub README를{' '}
            <span className={styles.gradientText}>자동으로 생성</span>하세요
          </h1>
          <p className={styles.subtext}>
            레포지토리 URL만 입력하면 AI가 멋진 README를 만들어드립니다
          </p>
        </section>

        <div className={styles.card}>
          {loading ? (
            <LoadingSpinner message="README 생성 중... 잠시 기다려주세요" />
          ) : (
            <>
              <RepoForm onSubmit={generate} loading={loading} />
              {error && (
                <div className={styles.error}>
                  ⚠️ {error}
                </div>
              )}
            </>
          )}
        </div>

        <div className={styles.features}>
          {FEATURES.map((f) => (
            <div key={f.title} className={styles.featureCard}>
              <span className={styles.featureIcon}>{f.icon}</span>
              <h3 className={styles.featureTitle}>{f.title}</h3>
              <p className={styles.featureDesc}>{f.desc}</p>
            </div>
          ))}
        </div>
      </main>

      <footer className={styles.footer}>
        <p>© 2025 ReadmeAI · Powered by Gemini</p>
      </footer>
    </div>
  );
}
