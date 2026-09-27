export default function Loading({ text = "Loading..." }) {
  return (
    <div className="flex min-h-48 items-center justify-center">
      <div className="text-center">
        <div className="mx-auto mb-3 h-8 w-8 animate-spin rounded-full border-2 border-slate-200 border-t-cyan-600" />
        <p className="text-sm text-slate-500">{text}</p>
      </div>
    </div>
  );
}
