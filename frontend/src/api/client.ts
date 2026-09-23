import type { CaseCategory, CaseRecord, CaseStatus, Deadline } from "../types/case";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";
const DEMO_API_KEY = import.meta.env.VITE_DEMO_API_KEY;
const DEMO_USER = import.meta.env.VITE_DEMO_USER ?? "demo@resolviq.local";

function authHeaders(): Record<string, string> {
  const headers: Record<string, string> = { "X-Demo-User": DEMO_USER };
  if (DEMO_API_KEY) headers["X-API-Key"] = DEMO_API_KEY;
  return headers;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...authHeaders(),
      ...(options?.headers ?? {}),
    },
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail ?? "Request failed");
  }
  return response.json();
}

export function listCases(): Promise<CaseRecord[]> {
  return request<CaseRecord[]>("/cases");
}

export function createCase(title: string, category: CaseCategory): Promise<CaseRecord> {
  return request<CaseRecord>("/cases", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, category }),
  });
}

export function uploadDocument(caseId: number, file: File): Promise<CaseRecord> {
  const form = new FormData();
  form.append("file", file);
  return request<CaseRecord>(`/cases/${caseId}/documents`, {
    method: "POST",
    body: form,
  });
}

export function updateStatus(caseId: number, status: CaseStatus): Promise<CaseRecord> {
  return request<CaseRecord>(`/cases/${caseId}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
}

export function createDeadline(caseId: number, label: string, dueDate: string): Promise<Deadline> {
  return request<Deadline>(`/cases/${caseId}/deadlines`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ label, due_date: dueDate }),
  });
}
