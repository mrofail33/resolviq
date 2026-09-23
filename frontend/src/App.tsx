import { useEffect, useMemo, useState } from "react";
import { AlertCircle, CheckCircle2, Scale } from "lucide-react";
import { CaseForm } from "./components/CaseForm";
import { CaseList } from "./components/CaseList";
import { CaseDetail } from "./components/CaseDetail";
import { createCase, createDeadline, listCases, updateStatus, uploadDocument } from "./api/client";
import type { CaseCategory, CaseRecord, CaseStatus } from "./types/case";

export default function App() {
  const [cases, setCases] = useState<CaseRecord[]>([]);
  const [selectedId, setSelectedId] = useState<number | undefined>();
  const [message, setMessage] = useState<string>("");
  const [error, setError] = useState<string>("");

  const activeCase = useMemo(
    () => cases.find((item) => item.id === selectedId) ?? cases[0],
    [cases, selectedId],
  );

  useEffect(() => {
    refresh();
  }, []);

  async function refresh() {
    try {
      const data = await listCases();
      setCases(data);
      if (!selectedId && data[0]) setSelectedId(data[0].id);
    } catch {
      setError("Start the backend server to load cases.");
    }
  }

  async function handleCreate(title: string, category: CaseCategory) {
    clearNotices();
    try {
      const created = await createCase(title, category);
      setCases((current) => [created, ...current]);
      setSelectedId(created.id);
      setMessage("Case created.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create case.");
    }
  }

  async function handleUpload(caseId: number, file: File) {
    clearNotices();
    try {
      const updated = await uploadDocument(caseId, file);
      replaceCase(updated);
      setMessage("Document analyzed and case updated.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not analyze document.");
    }
  }

  async function handleStatus(caseId: number, status: CaseStatus) {
    clearNotices();
    const updated = await updateStatus(caseId, status);
    replaceCase(updated);
  }

  async function handleDeadline(caseId: number, label: string, dueDate: string) {
    clearNotices();
    await createDeadline(caseId, label, dueDate);
    await refresh();
  }

  function replaceCase(updated: CaseRecord) {
    setCases((current) => current.map((item) => (item.id === updated.id ? updated : item)));
  }

  function clearNotices() {
    setMessage("");
    setError("");
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span><Scale size={22} /></span>
          <div>
            <h1>Resolviq</h1>
            <p>Administrative resolution platform</p>
          </div>
        </div>
        <CaseForm onCreate={handleCreate} />
        <CaseList cases={cases} selectedId={activeCase?.id} onSelect={setSelectedId} />
      </aside>

      <section className="workspace">
        <div className="topbar">
          <div>
            <p className="eyebrow">Refunds, warranties, travel</p>
            <h2>Case dashboard</h2>
          </div>
          <div className="mode-pill">Mock AI mode</div>
        </div>

        {message && (
          <div className="notice success">
            <CheckCircle2 size={18} />
            {message}
          </div>
        )}
        {error && (
          <div className="notice error">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        <CaseDetail
          activeCase={activeCase}
          onUpload={handleUpload}
          onStatusChange={handleStatus}
          onDeadline={handleDeadline}
        />
      </section>
    </main>
  );
}
