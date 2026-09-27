function matchTone(score) {
  if (score >= 80) return "border-emerald-200 bg-emerald-50 text-emerald-700";
  if (score >= 60) return "border-cyan-200 bg-cyan-50 text-cyan-700";
  if (score >= 40) return "border-amber-200 bg-amber-50 text-amber-700";
  return "border-slate-200 bg-slate-100 text-slate-600";
}

export default function MatchBadge({ score }) {
  return (
    <span className={`inline-flex rounded-full border px-3 py-1 text-sm font-bold ${matchTone(score)}`}>
      {Math.round(score)}% match
    </span>
  );
}
