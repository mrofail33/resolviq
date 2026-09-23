import { FileText, Plane, Receipt, ShieldCheck } from "lucide-react";
import type { CaseRecord } from "../types/case";

interface Props {
  cases: CaseRecord[];
  selectedId?: number;
  onSelect: (caseId: number) => void;
}

const icons = {
  refund: Receipt,
  warranty: ShieldCheck,
  travel: Plane,
};

export function CaseList({ cases, selectedId, onSelect }: Props) {
  if (cases.length === 0) {
    return (
      <div className="empty-state">
        <FileText size={28} />
        <p>Create a case to start organizing documents.</p>
      </div>
    );
  }

  return (
    <div className="case-list">
      {cases.map((item) => {
        const Icon = icons[item.category];
        return (
          <button
            key={item.id}
            className={`case-list-item ${selectedId === item.id ? "active" : ""}`}
            onClick={() => onSelect(item.id)}
          >
            <span className="case-icon">
              <Icon size={18} />
            </span>
            <span>
              <strong>{item.title}</strong>
              <small>{item.company ?? item.category}</small>
            </span>
          </button>
        );
      })}
    </div>
  );
}
