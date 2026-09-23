import { CalendarPlus, FileUp, Save } from "lucide-react";
import { type FormEvent, useState } from "react";
import type { CaseRecord, CaseStatus } from "../types/case";

interface Props {
  activeCase: CaseRecord | undefined;
  onUpload: (caseId: number, file: File) => Promise<void>;
  onStatusChange: (caseId: number, status: CaseStatus) => Promise<void>;
  onDeadline: (caseId: number, label: string, dueDate: string) => Promise<void>;
}

const statusLabels: Record<CaseStatus, string> = {
  draft: "Draft",
  waiting_on_company: "Waiting on company",
  follow_up_needed: "Follow-up needed",
  resolved: "Resolved",
  closed: "Closed",
};

export function CaseDetail({ activeCase, onUpload, onStatusChange, onDeadline }: Props) {
  const [deadlineLabel, setDeadlineLabel] = useState("");
  const [deadlineDate, setDeadlineDate] = useState("");
  const [localDraft, setLocalDraft] = useState("");

  if (!activeCase) {
    return <section className="panel detail-panel empty-panel">Select or create a case.</section>;
  }

  const currentCase = activeCase;
  const draft = localDraft || currentCase.generated_draft || "";

  async function upload(fileList: FileList | null) {
    const file = fileList?.[0];
    if (file) await onUpload(currentCase.id, file);
  }

  async function addDeadline(event: FormEvent) {
    event.preventDefault();
    if (!deadlineLabel || !deadlineDate) return;
    await onDeadline(currentCase.id, deadlineLabel, deadlineDate);
    setDeadlineLabel("");
    setDeadlineDate("");
  }

  return (
    <section className="detail-panel">
      <div className="detail-header">
        <div>
          <p className="eyebrow">{activeCase.category.replace("_", " ")}</p>
          <h2>{activeCase.title}</h2>
          <p>{activeCase.summary ?? "Upload a receipt, denial email, or PDF to organize the case."}</p>
        </div>
        <select value={activeCase.status} onChange={(event) => onStatusChange(activeCase.id, event.target.value as CaseStatus)}>
          {Object.entries(statusLabels).map(([value, label]) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </div>

      <div className="metric-grid">
        <div>
          <span>Company</span>
          <strong>{activeCase.company ?? "Unknown"}</strong>
        </div>
        <div>
          <span>Amount</span>
          <strong>{activeCase.disputed_amount ? `$${activeCase.disputed_amount}` : "Not found"}</strong>
        </div>
        <div>
          <span>Documents</span>
          <strong>{activeCase.documents.length}</strong>
        </div>
      </div>

      <div className="two-column">
        <section className="panel">
          <h3>Documents</h3>
          <label className="upload-box">
            <FileUp size={22} />
            <span>Upload TXT or PDF evidence</span>
            <input type="file" accept=".txt,.pdf,text/plain,application/pdf" onChange={(event) => upload(event.target.files)} />
          </label>
          {activeCase.documents.map((doc) => (
            <div className="document-row" key={doc.id}>
              <strong>{doc.filename}</strong>
              <small>{doc.extracted_text.slice(0, 100)}...</small>
            </div>
          ))}
        </section>

        <section className="panel">
          <h3>Case analysis</h3>
          <p><strong>Reason:</strong> {activeCase.dispute_reason ?? "Waiting for document analysis."}</p>
          <h4>Evidence</h4>
          <ul>{activeCase.evidence.map((item) => <li key={item}>{item}</li>)}</ul>
          <h4>Missing information</h4>
          <ul>{activeCase.missing_information.map((item) => <li key={item}>{item}</li>)}</ul>
        </section>
      </div>

      <div className="two-column">
        <section className="panel">
          <h3>Claim draft</h3>
          <textarea value={draft} onChange={(event) => setLocalDraft(event.target.value)} placeholder="A claim draft appears after analysis." />
          <button className="secondary-button" type="button">
            <Save size={16} />
            Keep edits locally
          </button>
        </section>

        <section className="panel">
          <h3>Deadlines</h3>
          <form className="deadline-form" onSubmit={addDeadline}>
            <input value={deadlineLabel} onChange={(event) => setDeadlineLabel(event.target.value)} placeholder="Send follow-up" />
            <input type="date" value={deadlineDate} onChange={(event) => setDeadlineDate(event.target.value)} />
            <button className="icon-button" aria-label="Add deadline">
              <CalendarPlus size={18} />
            </button>
          </form>
          {activeCase.deadlines.map((deadline) => (
            <div className="deadline-row" key={deadline.id}>
              <strong>{deadline.label}</strong>
              <span>{deadline.due_date}</span>
            </div>
          ))}
        </section>
      </div>
    </section>
  );
}
