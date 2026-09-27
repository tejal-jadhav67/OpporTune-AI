import { useEffect, useState } from "react";
import { CheckCircle2, Save } from "lucide-react";
import { createProfile, getProfile } from "../services/api";

const categories = ["Internship", "Hackathon", "Workshop", "Certification", "Competition", "Scholarship", "Course"];
const initialForm = { name: "", education: "B.Tech", year: 3, branch: "CSE-AIML", skills: "", interests: "", preferred_categories: [], preferred_location: "Pune / Remote" };

function listFromText(value) {
  return value.split(",").map((item) => item.trim()).filter(Boolean);
}

function Field({ label, children }) {
  return <label className="block"><span className="mb-2 block text-sm font-bold text-slate-700">{label}</span>{children}</label>;
}

function inputClass() {
  return "w-full rounded-xl border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-900 outline-none transition focus:border-cyan-500 focus:ring-4 focus:ring-cyan-50";
}

export default function ProfilePage() {
  const [form, setForm] = useState(initialForm);
  const [studentId, setStudentId] = useState(localStorage.getItem("studentId"));
  const [loading, setLoading] = useState(Boolean(studentId));
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!studentId) { setLoading(false); return; }
    getProfile(studentId).then((profile) => setForm({ ...profile, skills: profile.skills.join(", "), interests: profile.interests.join(", ") })).catch((err) => setError(err.message)).finally(() => setLoading(false));
  }, [studentId]);

  function update(field, value) { setForm((current) => ({ ...current, [field]: value })); }

  function toggleCategory(category) {
    setForm((current) => ({ ...current, preferred_categories: current.preferred_categories.includes(category) ? current.preferred_categories.filter((item) => item !== category) : [...current.preferred_categories, category] }));
  }

  async function submit(event) {
    event.preventDefault(); setSaving(true); setMessage(""); setError("");
    try {
      const profile = await createProfile({ ...form, year: Number(form.year), skills: listFromText(form.skills), interests: listFromText(form.interests) });
      localStorage.setItem("studentId", String(profile.id)); setStudentId(String(profile.id)); setMessage("Profile saved. Your recommendations are ready.");
    } catch (err) { setError(err.message); } finally { setSaving(false); }
  }

  if (loading) return <div className="mx-auto max-w-3xl px-4 py-20 text-center text-slate-500">Loading your profile...</div>;

  return (
    <div className="mx-auto max-w-3xl px-4 py-10 sm:px-6 lg:px-8">
      <p className="text-xs font-bold uppercase tracking-[0.2em] text-cyan-700">Student profile</p>
      <h1 className="mt-2 text-4xl font-black tracking-tight text-slate-950">Tell us what makes you, you.</h1>
      <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-500">Your skills and preferences become the signal behind every match.</p>

      <form onSubmit={submit} className="mt-8 space-y-5">
        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
          <h2 className="text-lg font-bold text-slate-950">About you</h2>
          <div className="mt-5 grid gap-5 sm:grid-cols-2">
            <Field label="Name"><input className={inputClass()} required value={form.name} onChange={(e) => update("name", e.target.value)} placeholder="Your name" /></Field>
            <Field label="Education"><input className={inputClass()} required value={form.education} onChange={(e) => update("education", e.target.value)} placeholder="B.Tech" /></Field>
            <Field label="Current year"><select className={inputClass()} value={form.year} onChange={(e) => update("year", Number(e.target.value))}>{[1, 2, 3, 4].map((year) => <option key={year} value={year}>{year}{year === 1 ? "st" : year === 2 ? "nd" : year === 3 ? "rd" : "th"} year</option>)}</select></Field>
            <Field label="Branch"><input className={inputClass()} required value={form.branch} onChange={(e) => update("branch", e.target.value)} placeholder="CSE-AIML" /></Field>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
          <h2 className="text-lg font-bold text-slate-950">Skills and interests</h2>
          <p className="mt-1 text-sm text-slate-500">Separate items with commas so the matcher can compare them clearly.</p>
          <div className="mt-5 space-y-5">
            <Field label="Skills"><textarea className={`${inputClass()} resize-none`} required rows="3" value={form.skills} onChange={(e) => update("skills", e.target.value)} placeholder="Python, Machine Learning, SQL, React" /></Field>
            <Field label="Interests"><textarea className={`${inputClass()} resize-none`} rows="3" value={form.interests} onChange={(e) => update("interests", e.target.value)} placeholder="Artificial Intelligence, Web Development, GenAI" /></Field>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-[0_10px_30px_rgba(15,23,42,0.04)]">
          <h2 className="text-lg font-bold text-slate-950">What are you looking for?</h2>
          <div className="mt-5"><p className="mb-3 text-sm font-bold text-slate-700">Opportunity types</p><div className="flex flex-wrap gap-2">{categories.map((category) => <button type="button" key={category} onClick={() => toggleCategory(category)} className={`rounded-full border px-3 py-2 text-xs font-bold transition ${form.preferred_categories.includes(category) ? "border-cyan-700 bg-cyan-700 text-white" : "border-slate-200 text-slate-600 hover:border-cyan-300"}`}>{category}</button>)}</div></div>
          <div className="mt-5"><Field label="Preferred location"><input className={inputClass()} value={form.preferred_location} onChange={(e) => update("preferred_location", e.target.value)} placeholder="Pune / Remote / Any" /></Field></div>
        </section>

        {error && <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{error}</p>}
        {message && <p className="flex items-center gap-2 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm font-bold text-emerald-700"><CheckCircle2 size={17} />{message}</p>}
        <button disabled={saving} className="flex w-full items-center justify-center gap-2 rounded-xl bg-slate-950 px-5 py-3 text-sm font-bold text-white transition hover:bg-cyan-800 disabled:opacity-60"><Save size={17} />{saving ? "Saving profile..." : studentId ? "Update profile" : "Save profile"}</button>
      </form>
    </div>
  );
}
