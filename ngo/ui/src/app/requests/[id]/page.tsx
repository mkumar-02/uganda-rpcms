"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import { ComplianceCheck, Mou, Ngo, NgoRequest } from "@/lib/types";
import {
  BackLink,
  Empty,
  ErrorBanner,
  GateSteps,
  PageHeader,
  StatusPill,
  fmtDate,
} from "@/components/ui";

export default function RequestDetailPage() {
  const params = useParams();
  const id = params.id as string;

  const [req, setReq] = useState<NgoRequest | null>(null);
  const [ngo, setNgo] = useState<Ngo | null>(null);
  const [checks, setChecks] = useState<ComplianceCheck[]>([]);
  const [mous, setMous] = useState<Mou[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [mouTitle, setMouTitle] = useState("OPM–Partner MoU");
  const [mouUri, setMouUri] = useState("");
  const [comment, setComment] = useState("");

  const reload = useCallback(async () => {
    setError(null);
    const r = await api.get<NgoRequest>(`/requests/${id}`);
    setReq(r);
    const [n, c, m] = await Promise.all([
      api.get<Ngo>(`/ngos/${r.ngo_id}`),
      api.get<ComplianceCheck[]>(`/requests/${id}/compliance`).catch(() => []),
      api.get<{ mous: Mou[] }>(`/ngos/${r.ngo_id}/mous`).then((d) => d.mous),
    ]);
    setNgo(n);
    setChecks(c);
    setMous(m);
  }, [id]);

  useEffect(() => {
    reload().catch((e) => setError(e.message));
  }, [reload]);

  async function act(fn: () => Promise<unknown>) {
    setBusy(true);
    setError(null);
    try {
      await fn();
      await reload();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  if (!req || !ngo) {
    return (
      <div>
        <BackLink href="/requests" label="Requests" />
        <div className="mt-4">
          <ErrorBanner message={error} />
          {!error && <Empty message="Loading…" />}
        </div>
      </div>
    );
  }

  return (
    <div>
      <BackLink href="/requests" label="Requests" />
      <div className="mt-3">
        <PageHeader
          title={ngo.name}
          subtitle={`Request ${req.id.slice(0, 8)} · ${req.request_type}`}
          action={<StatusPill status={req.status} />}
        />
      </div>

      <GateSteps status={req.status} />
      <ErrorBanner message={error} />

      <div className="grid gap-4 md:grid-cols-2 mb-6">
        <div className="card">
          <h2 className="text-lg mb-3">Organisation</h2>
          <dl className="text-sm space-y-2">
            <div>
              <dt className="text-[color:var(--color-text-muted)]">Short code</dt>
              <dd>{ngo.short_code || "—"}</dd>
            </div>
            <div>
              <dt className="text-[color:var(--color-text-muted)]">URSB</dt>
              <dd>{ngo.ursb_number || ngo.registration_number || "—"}</dd>
            </div>
            <div>
              <dt className="text-[color:var(--color-text-muted)]">NGO Bureau</dt>
              <dd>{ngo.ngo_bureau_number || "—"}</dd>
            </div>
            <div>
              <dt className="text-[color:var(--color-text-muted)]">Contact</dt>
              <dd>
                {ngo.contact_email || "—"}
                {ngo.contact_phone ? ` · ${ngo.contact_phone}` : ""}
              </dd>
            </div>
            <div>
              <Link href={`/ngos/${ngo.id}`} className="text-sm underline">
                Open partner record
              </Link>
            </div>
          </dl>
        </div>

        <div className="card">
          <h2 className="text-lg mb-3">Provisioned IDs</h2>
          <dl className="text-sm space-y-2">
            <div>
              <dt className="text-[color:var(--color-text-muted)]">Registry Agent</dt>
              <dd className="font-mono text-xs">{ngo.registry_agent_id || "—"}</dd>
            </div>
            <div>
              <dt className="text-[color:var(--color-text-muted)]">PBMS Agency</dt>
              <dd className="font-mono text-xs">{ngo.pbms_agency_id || "—"}</dd>
            </div>
            <div>
              <dt className="text-[color:var(--color-text-muted)]">PBMS Program</dt>
              <dd className="font-mono text-xs">{ngo.pbms_program_id || "—"}</dd>
            </div>
            <div>
              <dt className="text-[color:var(--color-text-muted)]">Approved</dt>
              <dd>{fmtDate(ngo.approved_at)}</dd>
            </div>
          </dl>
        </div>
      </div>

      {/* 1. Verify */}
      <div className="card mb-4">
        <div className="flex items-center justify-between mb-3 gap-2 flex-wrap">
          <h2 className="text-lg">1. Compliance (URSB · NGO Bureau)</h2>
          {(req.status === "created" || req.status === "compliance_passed") && (
            <button
              className="btn-primary"
              disabled={busy}
              onClick={() =>
                act(() => api.post(`/requests/${id}/run-compliance`))
              }
            >
              Run checks
            </button>
          )}
        </div>
        {checks.length === 0 ? (
          <p className="text-sm text-[color:var(--color-text-muted)]">
            No checks yet. Run URSB and NGO Bureau verification.
          </p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Kind</th>
                <th>Status</th>
                <th>Reference</th>
                <th>Message</th>
                <th>Checked</th>
              </tr>
            </thead>
            <tbody>
              {checks.map((c) => (
                <tr key={c.id}>
                  <td>{c.kind}</td>
                  <td>
                    <StatusPill status={c.status} />
                  </td>
                  <td>{c.reference_number || "—"}</td>
                  <td>{c.message || "—"}</td>
                  <td>{fmtDate(c.checked_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* 2. MoU */}
      <div className="card mb-4">
        <h2 className="text-lg mb-3">2. MoU</h2>
        {mous.length > 0 && (
          <table className="data-table mb-4">
            <thead>
              <tr>
                <th>Title</th>
                <th>Status</th>
                <th>Document</th>
                <th>Signed</th>
              </tr>
            </thead>
            <tbody>
              {mous.map((m) => (
                <tr key={m.id}>
                  <td>{m.title}</td>
                  <td>
                    <StatusPill status={m.status} />
                  </td>
                  <td className="truncate max-w-[200px]">{m.document_uri || "—"}</td>
                  <td>{fmtDate(m.signed_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {(req.status === "compliance_passed" || req.status === "mou_attached") && (
          <div className="grid gap-3 md:grid-cols-3 items-end">
            <div>
              <label className="field-label">Title</label>
              <input
                className="field-input"
                value={mouTitle}
                onChange={(e) => setMouTitle(e.target.value)}
              />
            </div>
            <div>
              <label className="field-label">Document URI</label>
              <input
                className="field-input"
                placeholder="s3://… or https://…"
                value={mouUri}
                onChange={(e) => setMouUri(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <button
                className="btn-secondary"
                disabled={busy || !mouTitle.trim()}
                onClick={() =>
                  act(async () => {
                    await api.post(`/ngos/${ngo.id}/mous`, {
                      title: mouTitle,
                      document_uri: mouUri || null,
                      request_id: id,
                      mark_signed: true,
                    });
                  })
                }
              >
                Attach &amp; sign MoU
              </button>
              <button
                className="btn-primary"
                disabled={busy}
                onClick={() =>
                  act(() => api.post(`/requests/${id}/mark-mou-attached`))
                }
              >
                Mark MoU attached
              </button>
            </div>
          </div>
        )}
        {req.status === "created" && (
          <p className="text-sm text-[color:var(--color-text-muted)]">
            Complete compliance before attaching an MoU.
          </p>
        )}
      </div>

      {/* 3. Decision */}
      <div className="card mb-4">
        <h2 className="text-lg mb-3">3. Decision</h2>
        {req.status === "mou_attached" ? (
          <div className="space-y-3">
            <div>
              <label className="field-label">Comment</label>
              <textarea
                className="field-input"
                rows={2}
                value={comment}
                onChange={(e) => setComment(e.target.value)}
              />
            </div>
            <div className="flex gap-2">
              <button
                className="btn-primary"
                disabled={busy}
                onClick={() =>
                  act(() =>
                    api.post(`/requests/${id}/approve`, {
                      comment,
                      decided_by: "opm.staff",
                    })
                  )
                }
              >
                Approve &amp; provision
              </button>
              <button
                className="btn-danger"
                disabled={busy}
                onClick={() =>
                  act(() =>
                    api.post(`/requests/${id}/reject`, {
                      comment,
                      decided_by: "opm.staff",
                    })
                  )
                }
              >
                Reject
              </button>
            </div>
          </div>
        ) : req.status === "approved" || req.status === "rejected" ? (
          <p className="text-sm">
            Decided by <strong>{req.decided_by}</strong> on {fmtDate(req.decided_at)}
            {req.decision_comment ? ` — ${req.decision_comment}` : ""}
          </p>
        ) : (
          <p className="text-sm text-[color:var(--color-text-muted)]">
            Approval unlocks after compliance and a signed MoU.
          </p>
        )}
      </div>
    </div>
  );
}
