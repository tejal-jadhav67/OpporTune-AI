import { Link } from "react-router-dom";
import { ArrowRight, BrainCircuit, Search, Target } from "lucide-react";

function LandingPage() {
  return (
    <div>
      <section className="bg-gradient-to-b from-indigo-50 via-white to-slate-50">
        <div className="mx-auto max-w-7xl px-4 py-20 text-center sm:px-6 lg:px-8">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-indigo-100 bg-indigo-50 px-4 py-2 text-sm font-medium text-indigo-700">
            <BrainCircuit size={16} />
            AI-powered opportunity discovery
          </div>

          <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-6xl">
            Find opportunities
            <span className="block text-indigo-600">made for you.</span>
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600">
            OpporTune AI helps students discover internships, hackathons, courses,
            scholarships and more through personalized, explainable recommendations.
          </p>

          <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
            <Link
              to="/profile"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white shadow-sm transition hover:bg-indigo-700"
            >
              Build My Profile
              <ArrowRight size={18} />
            </Link>

            <Link
              to="/opportunities"
              className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white px-6 py-3 font-semibold text-slate-700 transition hover:bg-slate-50"
            >
              Explore Opportunities
              <Search size={18} />
            </Link>
          </div>
        </div>
      </section>

      <section className="border-t border-slate-200 bg-slate-50">
        <div className="mx-auto grid max-w-7xl gap-6 px-4 py-16 sm:px-6 md:grid-cols-3 lg:px-8">
          <div className="rounded-2xl border border-slate-200 bg-white p-6">
            <Target className="mb-4 text-indigo-600" size={28} />
            <h2 className="text-lg font-semibold text-slate-900">Personalized</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Recommendations are based on your skills, interests, eligibility,
              category and location preferences.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6">
            <BrainCircuit className="mb-4 text-indigo-600" size={28} />
            <h2 className="text-lg font-semibold text-slate-900">AI-powered</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              AI turns structured matching results into clear, easy-to-understand
              recommendations.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6">
            <Search className="mb-4 text-indigo-600" size={28} />
            <h2 className="text-lg font-semibold text-slate-900">Explainable</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              See why an opportunity matches you and which skills you could develop
              next.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default LandingPage;
