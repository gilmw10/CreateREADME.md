import { useNavigate } from 'react-router-dom';
import DocIcon from '../components/DocIcon';
import Footer from '../components/Footer';
import styles from './LandingPage.module.css';

export default function LandingPage() {
  const navigate = useNavigate();
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <DocIcon size={64} />
        <h1 className={styles.title}>
          CREATE<br />FOR<br />README.md
        </h1>
        <button className={styles.startBtn} onClick={() => navigate('/create')}>
          START CREATE
        </button>
      </main>
      <Footer />
    </div>
  );
}
