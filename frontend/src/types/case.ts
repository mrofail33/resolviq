export type CaseCategory = "refund" | "warranty" | "travel";
export type CaseStatus = "draft" | "waiting_on_company" | "follow_up_needed" | "resolved" | "closed";

export interface Deadline {
  id: number;
  label: string;
  due_date: string;
  completed: boolean;
}

export interface DocumentRecord {
  id: number;
  filename: string;
  content_type: string;
  extracted_text: string;
  created_at: string;
}

export interface ImportantDate {
  label: string;
  date: string;
}

export interface CaseRecord {
  id: number;
  title: string;
  category: CaseCategory;
  status: CaseStatus;
  company: string | null;
  disputed_amount: string | null;
  summary: string | null;
  dispute_reason: string | null;
  generated_draft: string | null;
  created_at: string;
  documents: DocumentRecord[];
  deadlines: Deadline[];
  evidence: string[];
  missing_information: string[];
  important_dates: ImportantDate[];
}
