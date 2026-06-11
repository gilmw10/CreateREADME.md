import DocIcon from './DocIcon';
import styles from './Header.module.css';

export default function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <DocIcon size={30} />
        <span className={styles.title}>Create For README.md</span>
      </div>
    </header>
  );
}
