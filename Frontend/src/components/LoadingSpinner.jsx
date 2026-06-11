import styles from './LoadingSpinner.module.css';

export default function LoadingSpinner() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.spinner}>
        {Array.from({ length: 8 }, (_, i) => (
          <span
            key={i}
            className={styles.dot}
            style={{
              transform: `rotate(${i * 45}deg)`,
              opacity: Math.max(0.12, 1 - i * 0.115),
            }}
          />
        ))}
      </div>
      <p className={styles.title}>CREATING README.md...</p>
      <p className={styles.subtitle}>please waiting more second</p>
    </div>
  );
}
