export default function SkillPill({ children, type = "default" }) {
  const styles = {
    default: "bg-slate-100 text-slate-700",
    match: "bg-emerald-50 text-emerald-700",
    gap: "bg-amber-50 text-amber-700",
  };

  return <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${styles[type] || styles.default}`}>{children}</span>;
}
