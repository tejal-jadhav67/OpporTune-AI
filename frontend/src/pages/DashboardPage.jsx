import { useEffect, useState } from "react";
import { ArrowRight, Bookmark, Compass, UserRound } from "lucide-react";
import { Link } from "react-router-dom";
import { getProfile, getRecommendations, getSavedOpportunities, removeSavedOpportunity, saveOpportunity } from "../services/api";
import Loading from "../components/Loading";
import OpportunityCard from "../components/OpportunityCard";

function NoProfile() {
  return <div className="mx-auto max-w-xl px-4 py-24 text-center"><div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-cyan-50 text-cyan-700"><UserRound /></div><h1 className="mt-5 text-3xl font-black text-slate-950">Start with your profile</h1><p className="mt-3 text-sm leading-6 text-slate-500">Tell us about your skills and interests, and the dashboard will do the sorting.</p><Link to="/profile" className="mt-6 inline-flex rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white">Build profile</Link></div>;
}

export default function DashboardPage() {
  const studentId = localStorage.getItem("studentId");
  const [profile, setProfile] = useState(null); const [recommendations, setRecommendations] = useState([]); const [savedIds, setSavedIds] = useState(new Set()); const [loading, setLoading] = useState(Boolean(studentId)); const [error, setError] = useState("");

  useEffect(() => {
    if (!studentId) return;
    Promise.all([getProfile(studentId), getRecommendations(studentId, 6), getSavedOpportunities(studentId)]).then(([profileData, recommendationData, savedData]) => { setProfile(profileData); setRecommendations(recommendationData); setSavedIds(new Set(savedData.map((item) => item.opportunity.id))); }).catch((err) => setError(err.message)).finally(() => setLoading(false));
  }, [studentId]);

  async function toggleSave(opportunityId) {
    try {
      if (savedIds.has(opportunityId)) { await removeSavedOpportunity(opportunityId, studentId); setSavedIds((current) => new Set([...current].filter((id) => id !== opportunityId))); }
      else { await saveOpportunity(opportunityId, studentId); setSavedIds((current) => new Set([...current, opportunityId])); }
    } catch (err) { setError(err.message); }
  }

  if (!studentId) return <NoProfile />;
  if (loading) return <Loading text="Finding your strongest matches..." />;
  if (error) return <div className="mx-auto max-w-7xl px-4 py-10"><p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</p></div>;

  return <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
    <section className="overflow-hidden rounded-3xl bg-slate-950 px-6 py-8 text-white sm:px-10 sm:py-10">
      <p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-300">Personalized discovery</p>
      <h1 className="mt-3 max-w-2xl text-4xl font-black tracking-tight sm:text-5xl">Good morning, {profile?.name || "there"}.</h1>
      <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-300">These opportunities rise to the top because they fit your skills, interests, eligibility, and preferences.</p>
      <div className="mt-6 flex flex-wrap gap-2">{profile?.skills?.slice(0, 6).map((skill) => <span key={skill} className="rounded-full bg-white/10 px-3 py-1.5 text-xs font-semibold text-slate-200">{skill}</span>)}</div>
    </section>

    <section className="mt-10"><div className="mb-5 flex items-end justify-between"><div><p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-700">Recommendation engine</p><h2 className="mt-2 text-3xl font-black text-slate-950">Your top matches</h2></div><Link to="/opportunities" className="hidden items-center gap-1 text-sm font-bold text-cyan-700 sm:flex">Explore all <ArrowRight size={16} /></Link></div>{recommendations.length ? <div className="grid gap-5 lg:grid-cols-2">{recommendations.map((item) => <OpportunityCard key={item.opportunity.id} recommendation={item} saved={savedIds.has(item.opportunity.id)} onSave={toggleSave} />)}</div> : <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center text-sm text-slate-500">Add more profile details to improve your matches.</div>}</section>

    <div className="mt-8 grid gap-4 sm:grid-cols-3"><QuickLink to="/profile" icon={UserRound} title="Update profile" text="Improve your matches" /><QuickLink to="/opportunities" icon={Compass} title="Explore" text="Browse all opportunities" /><QuickLink to="/saved" icon={Bookmark} title="Saved" text="Review your shortlist" /></div>
  </div>;
}

function QuickLink({ to, icon: Icon, title, text }) { return <Link to={to} className="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-cyan-200"><span className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-50 text-cyan-700"><Icon size={19} /></span><span><strong className="block text-sm text-slate-950">{title}</strong><small className="text-xs text-slate-500">{text}</small></span></Link>; }
