const API_BASE_URL = import.meta.env.VITE_API_URL || "";

async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let errorMessage = `API request failed with status ${response.status}`;

    try {
      const errorData = await response.json();

      errorMessage = errorData.detail || errorData.message || errorMessage;
    } catch {
      // Keep the default error message if the response is not JSON.
    }

    throw new Error(errorMessage);
  }

  return response.json();
}

export async function checkBackendHealth() {
  return apiRequest("/api/health");
}

export async function createProfile(profile) {
  return apiRequest("/api/profile", {
    method: "POST",
    body: JSON.stringify(profile),
  });
}

export async function getProfile(studentId) {
  return apiRequest(`/api/profile/${studentId}`);
}

export async function getOpportunities(filters = {}) {
  const params = new URLSearchParams();
  if (filters.search) params.set("search", filters.search);
  if (filters.category) params.set("category", filters.category);
  if (filters.location) params.set("location", filters.location);
  const query = params.toString();
  return apiRequest(`/api/opportunities${query ? `?${query}` : ""}`);
}

export async function getOpportunity(opportunityId) {
  return apiRequest(`/api/opportunities/${opportunityId}`);
}

export async function getRecommendations(studentId, limit = 10) {
  return apiRequest(`/api/recommendations/${studentId}?limit=${limit}`);
}

export async function matchOpportunity(studentId, opportunityId) {
  return apiRequest("/api/match", {
    method: "POST",
    body: JSON.stringify({
      student_id: Number(studentId),
      opportunity_id: Number(opportunityId),
    }),
  });
}

export async function getAIExplanation(studentId, opportunityId) {
  return apiRequest("/api/ai/explanation", {
    method: "POST",
    body: JSON.stringify({
      student_id: Number(studentId),
      opportunity_id: Number(opportunityId),
    }),
  });
}

export async function saveOpportunity(opportunityId, studentId) {
  return apiRequest(`/api/opportunities/${opportunityId}/save?student_id=${studentId}`, {
    method: "POST",
  });
}

export async function removeSavedOpportunity(opportunityId, studentId) {
  return apiRequest(`/api/opportunities/${opportunityId}/save?student_id=${studentId}`, {
    method: "DELETE",
  });
}

export async function getSavedOpportunities(studentId) {
  return apiRequest(`/api/saved/${studentId}`);
}

export default apiRequest;
