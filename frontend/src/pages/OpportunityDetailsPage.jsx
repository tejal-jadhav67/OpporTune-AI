import { useParams } from "react-router-dom";

function OpportunityDetailsPage() {
  const { id } = useParams();

  return (
    <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
      <p className="text-sm font-semibold text-indigo-600">OPPORTUNITY</p>
      <h1 className="mt-2 text-3xl font-bold text-slate-900">
        Opportunity Details
      </h1>
      <p className="mt-3 text-slate-600">Opportunity ID: {id}</p>
      <p className="mt-2 text-slate-500">
        Detailed opportunity information and AI match analysis will be implemented
        later.
      </p>
    </div>
  );
}

export default OpportunityDetailsPage;
