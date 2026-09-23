import { useState } from "react";
import { Plus } from "lucide-react";
import type { CaseCategory } from "../types/case";

interface Props {
  onCreate: (title: string, category: CaseCategory) => Promise<void>;
}

export function CaseForm({ onCreate }: Props) {
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState<CaseCategory>("refund");
  const [busy, setBusy] = useState(false);

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    if (title.trim().length < 3) return;
    setBusy(true);
    await onCreate(title.trim(), category);
    setTitle("");
    setBusy(false);
  }

  return (
    <form className="case-form" onSubmit={submit}>
      <label>
        Case title
        <input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Laptop warranty denied" />
      </label>
      <label>
        Category
        <select value={category} onChange={(event) => setCategory(event.target.value as CaseCategory)}>
          <option value="refund">Refund dispute</option>
          <option value="warranty">Warranty claim</option>
          <option value="travel">Travel claim</option>
        </select>
      </label>
      <button className="primary-button" disabled={busy || title.trim().length < 3}>
        <Plus size={18} />
        Create case
      </button>
    </form>
  );
}
