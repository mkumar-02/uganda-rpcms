"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { NgoRequest } from "@/lib/types";
import { PageHeader, StatusPill, ErrorBanner, Empty, fmtDate } from "@/components/ui";

const FILTERS = [
  "",
  "created",
  "compliance_passed",
  "mou_attached",
  "approved",
  "rejected",
];

export default function RequestsPage() {
  const [rows, setRows] = useState<NgoRequest[]>([]);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    const q = status ? `?status=${encodeURIComponent(status)}` : "";
    api
      .get<{ requests: NgoRequest[] }>(`/requests${q}`)
      .then((d) => setRows(d.requests))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [status]);

  return (
    <div>
      <PageHeader
        title="Requests"
        subtitle="Verify → MoU → Approve · then Registry Agent + PBMS Agency/Program"
        action={
          <Link href="/onboard" className="btn-primary">
            + Onboard partner
          </Link>
        }
      />

      <div className="flex flex-wrap items-center gap-2 mb-4">
        {FILTERS.map((f) => (
          <button
            key={f || "all"}
            onClick={() => setStatus(f)}
            className={status === f ? "btn-primary" : "btn-secondary"}
          >
            {f ? f.replace(/_/g, " ") : "All"}
          </button>
        ))}
      </div>

      <ErrorBanner message={error} />

      {loading ? (
        <Empty message="Loading…" />
      ) : rows.length === 0 ? (
        <Empty message="No requests found." />
      ) : (
        <div className="card p-0 overflow-hidden">
          <table className="data-table">
            <thead>
              <tr>
                <th>Partner</th>
                <th>Type</th>
                <th>Status</th>
                <th>Submitted</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.id}>
                  <td>
                    <Link
                      href={`/requests/${r.id}`}
                      className="font-medium hover:underline"
                    >
                      {r.ngo_name || r.ngo_id.slice(0, 8)}
                    </Link>
                  </td>
                  <td>{r.request_type}</td>
                  <td>
                    <StatusPill status={r.status} />
                  </td>
                  <td>{r.submitted_by || "—"}</td>
                  <td>{fmtDate(r.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
