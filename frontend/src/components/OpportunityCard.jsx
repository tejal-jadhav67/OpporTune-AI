import { ArrowUpRight, Bookmark, CalendarDays, MapPin } from "lucide-react";
import { Link } from "react-router-dom";
import MatchBadge from "./MatchBadge";
import SkillPill from "./SkillPill";

export default function OpportunityCard({ recommendation, saved = false, onSave }) {
  const opportunity = recommendation.opportunity || recommendation;
  const score = recommendation.match_percentage;

  return (
    <article className="group flex h-full flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_10px_30px_rgba(15,23,42,0.05)] transition duration-200 hover:-translate-y-1 hover:border-cyan-200 hover:shadow-[0_18px_40px_rgba(8,145,178,0.12)]">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-bold uppercase tracking-[0.16em] text-cyan-700">{opportunity.category}</p>
          <Link to={`/opportunities/${opportunity.id}`} className="mt-2 block text-lg font-bold leading-tight text-slate-950 group-hover:text-cyan-700">
            {opportunity.title}
          </Link>
          <p className="mt-1 text-sm font-medium text-slate-500">{opportunity.organization}</p>
        </div>
        {typeof score === "number" && <MatchBadge score={score} />}
      </div>

      <p className="mt-4 line-clamp-3 text-sm leading-6 text-slate-600">{opportunity.description}</p>

      <div className="mt-4 flex flex-wrap gap-3 text-xs font-medium text-slate-500">
        <span className="inline-flex items-center gap-1"><MapPin size={14} />{opportunity.location}</span>
        <span className="inline-flex items-center gap-1"><CalendarDays size={14} />{opportunity.deadline}</span>
      </div>

      {recommendation.matching_skills?.length > 0 && (
        <div className="mt-4">
          <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-500">Matching skills</p>
          <div className="flex flex-wrap gap-2">{recommendation.matching_skills.slice(0, 5).map((skill) => <SkillPill key={skill} type="match">{skill}</SkillPill>)}</div>
        </div>
      )}

      {recommendation.skill_gaps?.length > 0 && (
        <div className="mt-3">
          <p className="mb-2 text-xs font-bold uppercase tracking-wide text-slate-500">Skill gaps</p>
          <div className="flex flex-wrap gap-2">{recommendation.skill_gaps.slice(0, 4).map((skill) => <SkillPill key={skill} type="gap">{skill}</SkillPill>)}</div>
        </div>
      )}

      {recommendation.explanation && <p className="mt-4 rounded-xl bg-slate-50 p-3 text-xs leading-5 text-slate-600">{recommendation.explanation}</p>}

      <div className="mt-auto flex gap-2 pt-5">
        <Link to={`/opportunities/${opportunity.id}`} className="group/details inline-flex flex-1 items-center justify-center gap-2 rounded-xl bg-cyan-700 px-4 py-3 text-center text-sm font-bold !text-white shadow-sm transition hover:bg-cyan-800 hover:shadow-md focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-cyan-200 active:translate-y-px"><span>View details</span><ArrowUpRight size={16} aria-hidden="true" className="transition-transform group-hover/details:translate-x-0.5 group-hover/details:-translate-y-0.5" /></Link>
        {onSave && <button type="button" onClick={() => onSave(opportunity.id)} aria-label={saved ? "Remove saved opportunity" : "Save opportunity"} title={saved ? "Remove from saved" : "Save opportunity"} className={`rounded-xl border px-3 transition ${saved ? "border-cyan-200 bg-cyan-50 text-cyan-700" : "border-slate-200 text-slate-600 hover:bg-slate-50"}`}><Bookmark size={18} fill={saved ? "currentColor" : "none"} /></button>}
      </div>
    </article>
  );
}
