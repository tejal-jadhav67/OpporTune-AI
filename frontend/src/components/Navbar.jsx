import { Link, NavLink } from "react-router-dom";
import { Sparkles } from "lucide-react";

function Navbar() {
  const getNavClass = ({ isActive }) =>
    `text-sm font-medium transition ${
      isActive ? "text-indigo-600" : "text-slate-600 hover:text-indigo-600"
    }`;

  return (
    <header className="border-b border-slate-200 bg-white/80 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-indigo-600 text-white">
            <Sparkles size={18} />
          </div>

          <div>
            <p className="text-base font-bold tracking-tight text-slate-900">
              OpporTune AI
            </p>
            <p className="hidden text-[10px] font-medium text-slate-500 sm:block">
              Personalized opportunities
            </p>
          </div>
        </Link>

        <nav className="flex items-center gap-4 sm:gap-6">
          <NavLink to="/dashboard" className={getNavClass}>
            Dashboard
          </NavLink>

          <NavLink to="/opportunities" className={getNavClass}>
            Opportunities
          </NavLink>

          <NavLink to="/saved" className={getNavClass}>
            Saved
          </NavLink>

          <Link
            to="/profile"
            className="rounded-lg bg-indigo-600 px-3 py-2 text-sm font-semibold text-white transition hover:bg-indigo-700"
          >
            Profile
          </Link>
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
