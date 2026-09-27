import { useEffect, useState } from "react";
import { Filter, Search, X } from "lucide-react";
import { getOpportunities, getSavedOpportunities, removeSavedOpportunity, saveOpportunity } from "../services/api";
import Loading from "../components/Loading";
import OpportunityCard from "../components/OpportunityCard";

const categories = ["Internship", "Hackathon", "Workshop", "Certification", "Competition", "Scholarship", "Course"];

export default function OpportunitiesPage() {
  const studentId = localStorage.getItem("studentId");
  const [opportunities, setOpportunities] = useState([]); const [savedIds, setSavedIds] = useState(new Set()); const [filters, setFilters] = useState({ search: "", category: "", location: "" }); const [loading, setLoading] = useState(true); const [error, setError] = useState("");

  async function load() {
    setLoading(true); setError("");
    try { const items = await getOpportunities(filters); setOpportunities(items); if (studentId) { const saved = await getSavedOpportunities(studentId); setSavedIds(new Set(saved.map((item) => item.opportunity.id))); } }
    catch (err) { setError(err.message); } finally { setLoading(false); }
  }
  useEffect(() => { load(); }, []);
  function change(field, value) { setFilters((current) => ({ ...current, [field]: value })); }
  async function toggleSave(id) { if (!studentId) { setError("Create a profile before saving opportunities."); return; } try { if (savedIds.has(id)) { await removeSavedOpportunity(id, studentId); setSavedIds((current) => new Set([...current].filter((item) => item !== id))); } else { await saveOpportunity(id, studentId); setSavedIds((current) => new Set([...current, id])); } } catch (err) { setError(err.message); } }
  function clear() { setFilters({ search: "", category: "", location: "" }); setTimeout(load, 0); }

  return <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8"><p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-700">Opportunity explorer</p><h1 className="mt-2 text-4xl font-black tracking-tight text-slate-950">Find your next move.</h1><p className="mt-3 text-sm text-slate-500">Search the full opportunity catalog and narrow it to what fits.</p>
    <form onSubmit={(e) => { e.preventDefault(); load(); }} className="mt-8 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"><div className="grid gap-3 lg:grid-cols-[1fr_180px_180px_auto]"><label className="relative"><Search size={17} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" /><input value={filters.search} onChange={(e) => change("search", e.target.value)} placeholder="Search Python, AI, internships..." className="w-full rounded-xl border border-slate-200 py-3 pl-10 pr-3 text-sm outline-none focus:border-cyan-500" /></label><select value={filters.category} onChange={(e) => change("category", e.target.value)} className="rounded-xl border border-slate-200 bg-white px-3 py-3 text-sm outline-none focus:border-cyan-500"><option value="">All categories</option>{categories.map((category) => <option key={category}>{category}</option>)}</select><input value={filters.location} onChange={(e) => change("location", e.target.value)} placeholder="Location" className="rounded-xl border border-slate-200 px-3 py-3 text-sm outline-none focus:border-cyan-500" /><button className="inline-flex items-center justify-center gap-2 rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white hover:bg-cyan-800"><Filter size={16} />Apply</button></div>{Object.values(filters).some(Boolean) && <button type="button" onClick={clear} className="mt-3 inline-flex items-center gap-1 text-xs font-bold text-slate-500"><X size={14} />Clear filters</button>}</form>
    {error && <p className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</p>}
    {loading ? <Loading text="Loading opportunities..." /> : <><p className="mb-4 mt-7 text-sm font-semibold text-slate-500">{opportunities.length} opportunities found</p>{opportunities.length ? <div className="grid gap-5 lg:grid-cols-2">{opportunities.map((opportunity) => <OpportunityCard key={opportunity.id} recommendation={opportunity} saved={savedIds.has(opportunity.id)} onSave={toggleSave} />)}</div> : <div className="rounded-2xl border border-dashed border-slate-300 p-12 text-center text-sm text-slate-500">No opportunities match those filters.</div>}</>}
  </div>;
}
