export default function DocIcon({ size = 48 }) {
  const w = Math.round((size * 40) / 48);
  return (
    <svg width={w} height={size} viewBox="0 0 40 48" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M0 4C0 1.79 1.79 0 4 0H28L40 12V44C40 46.21 38.21 48 36 48H4C1.79 48 0 46.21 0 44V4Z" fill="#3D3D3D"/>
      <path d="M28 0L40 12H30C28.9 12 28 11.1 28 10V0Z" fill="#555555"/>
      <rect x="8" y="20" width="24" height="3" rx="1.5" fill="white" fillOpacity="0.85"/>
      <rect x="8" y="27" width="24" height="3" rx="1.5" fill="white" fillOpacity="0.85"/>
      <rect x="8" y="34" width="16" height="3" rx="1.5" fill="white" fillOpacity="0.85"/>
    </svg>
  );
}
