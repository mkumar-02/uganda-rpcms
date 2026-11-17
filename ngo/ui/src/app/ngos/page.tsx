"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { Ngo } from "@/lib/types";
import { PageHeader, StatusPill, ErrorBanner, Empty, fmtDate } from "@/components/ui";

const FILTERS = ["", "active", "pending_compliance", "pending_mou", "pending_approval", "rejected"];

export default function NgosPage() {
  const [rows, setRows] = useState<Ngo[]>([]);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    const q = status ? `?status=${encodeURIComponent(status)}` : "";
    api
      .get<{ ngos: Ngo[] }>(`/ngos${q}`)
      .then((d) => setRows(d.ngos))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [status]);

  return (
    <div>
      <PageHeader
        title="Partners"
        subtitle="Organisations onboarded for refugee assistance delivery"
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
        <Empty message="No partners yet." />
      ) : (
        <div className="card p-0 overflow-hidden">
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Code</th>
                <th>Status</th>
                <th>Agency</th>
                <th>Created</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((n) => (
                <tr key={n.id}>
                  <td>
                    <Link href={`/ngos/${n.id}`} className="font-medium hover:underline">
                      {n.name}
                    </Link>
                  </td>
                  <td>{n.short_code || "—"}</td>
                  <td>
                    <StatusPill status={n.status} />
                  </td>
                  <td className="font-mono text-xs">{n.pbms_agency_id || "—"}</td>
                  <td>{fmtDate(n.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
