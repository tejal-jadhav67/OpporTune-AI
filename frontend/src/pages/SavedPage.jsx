import { useEffect, useState } from "react";
import { Bookmark } from "lucide-react";
import { Link } from "react-router-dom";
import { getSavedOpportunities, removeSavedOpportunity } from "../services/api";
import Loading from "../components/Loading";

export default function SavedPage() {
  const studentId = localStorage.getItem("studentId"); const [saved, setSaved] = useState([]); const [loading, setLoading] = useState(Boolean(studentId)); const [error, setError] = useState("");
  useEffect(() => { if (!studentId) return; getSavedOpportunities(studentId).then(setSaved).catch((err) => setError(err.message)).finally(() => setLoading(false)); }, [studentId]);
  async function remove(id) { try { await removeSavedOpportunity(id, studentId); setSaved((current) => current.filter((item) => item.opportunity.id !== id)); } catch (err) { setError(err.message); } }
  if (!studentId) return <Empty title="Create a profile first" text="Your shortlist will live here once you start saving opportunities." action="Build profile" to="/profile" />;
  if (loading) return <Loading text="Loading your shortlist..." />;
  return <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8"><p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-700">Your shortlist</p><h1 className="mt-2 text-4xl font-black tracking-tight text-slate-950">Saved opportunities</h1><p className="mt-3 text-sm text-slate-500">Keep the possibilities worth revisiting close at hand.</p>{error && <p className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</p>}{saved.length === 0 ? <Empty title="Nothing saved yet" text="Explore the catalog and bookmark opportunities you want to revisit." action="Explore opportunities" to="/opportunities" /> : <div className="mt-8 grid gap-5 lg:grid-cols-2">{saved.map((item) => <article key={item.saved_id} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-xs font-bold uppercase tracking-[0.16em] text-cyan-700">{item.opportunity.category}</p><h2 className="mt-2 text-xl font-black text-slate-950">{item.opportunity.title}</h2><p className="mt-1 text-sm font-semibold text-slate-500">{item.opportunity.organization}</p><p className="mt-4 text-sm leading-6 text-slate-600">{item.opportunity.description}</p><div className="mt-5 flex gap-2"><Link to={`/opportunities/${item.opportunity.id}`} className="flex-1 rounded-xl bg-slate-950 px-4 py-2.5 text-center text-sm font-bold text-white">View details</Link><button onClick={() => remove(item.opportunity.id)} className="rounded-xl border border-slate-200 px-4 py-2.5 text-sm font-bold text-slate-600 hover:bg-slate-50">Remove</button></div></article>)}</div>}</div>;
}

function Empty({ title, text, action, to }) { return <div className="mx-auto max-w-xl px-4 py-24 text-center"><Bookmark size={34} className="mx-auto text-slate-300" /><h2 className="mt-4 text-2xl font-black text-slate-950">{title}</h2><p className="mt-2 text-sm leading-6 text-slate-500">{text}</p><Link to={to} className="mt-6 inline-flex rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white">{action}</Link></div>; }
