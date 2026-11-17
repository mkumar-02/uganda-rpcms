"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import { Mou, Ngo, NgoLocation } from "@/lib/types";
import {
  BackLink,
  Empty,
  ErrorBanner,
  PageHeader,
  StatusPill,
  fmtDate,
} from "@/components/ui";

export default function NgoDetailPage() {
  const params = useParams();
  const id = params.id as string;

  const [ngo, setNgo] = useState<Ngo | null>(null);
  const [mous, setMous] = useState<Mou[]>([]);
  const [locations, setLocations] = useState<NgoLocation[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [locName, setLocName] = useState("");
  const [locKind, setLocKind] = useState("admin_large");
  const [locCode, setLocCode] = useState("");

  const reload = useCallback(async () => {
    const [n, m, l] = await Promise.all([
      api.get<Ngo>(`/ngos/${id}`),
      api.get<{ mous: Mou[] }>(`/ngos/${id}/mous`).then((d) => d.mous),
      api.get<{ locations: NgoLocation[] }>(`/ngos/${id}/locations`).then((d) => d.locations),
    ]);
    setNgo(n);
    setMous(m);
    setLocations(l);
  }, [id]);

  useEffect(() => {
    reload().catch((e) => setError(e.message));
  }, [reload]);

  async function addLocation() {
    if (!locName.trim()) return;
    setBusy(true);
    setError(null);
    try {
      await api.post(`/ngos/${id}/locations`, {
        name: locName,
        kind: locKind,
        code: locCode || null,
      });
      setLocName("");
      setLocCode("");
      await reload();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  async function removeLocation(locationId: string) {
    setBusy(true);
    setError(null);
    try {
      await api.delete(`/locations/${locationId}`);
      await reload();
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy(false);
    }
  }

  if (!ngo) {
    return (
      <div>
        <BackLink href="/ngos" label="Partners" />
        <div className="mt-4">
          <ErrorBanner message={error} />
          {!error && <Empty message="Loading…" />}
        </div>
      </div>
    );
  }

  return (
    <div>
      <BackLink href="/ngos" label="Partners" />
      <div className="mt-3">
        <PageHeader
          title={ngo.name}
          subtitle={ngo.short_code || ngo.id.slice(0, 8)}
          action={<StatusPill status={ngo.status} />}
        />
      </div>
      <ErrorBanner message={error} />

      <div className="grid gap-4 md:grid-cols-2 mb-6">
        <div className="card">
          <h2 className="text-lg mb-3">Details</h2>
          <dl className="text-sm space-y-2">
            <Row label="Registration" value={ngo.registration_number} />
            <Row label="URSB" value={ngo.ursb_number} />
            <Row label="NGO Bureau" value={ngo.ngo_bureau_number} />
            <Row label="Email" value={ngo.contact_email} />
            <Row label="Phone" value={ngo.contact_phone} />
            <Row label="Address" value={ngo.legal_address} />
            <Row label="Approved" value={fmtDate(ngo.approved_at)} />
          </dl>
        </div>
        <div className="card">
          <h2 className="text-lg mb-3">Downstream links</h2>
          <dl className="text-sm space-y-2">
            <Row label="Registry Agent" value={ngo.registry_agent_id} mono />
            <Row label="PBMS Agency" value={ngo.pbms_agency_id} mono />
            <Row label="PBMS Program" value={ngo.pbms_program_id} mono />
          </dl>
        </div>
      </div>

      <div className="card mb-4">
        <h2 className="text-lg mb-3">MoUs</h2>
        {mous.length === 0 ? (
          <p className="text-sm text-[color:var(--color-text-muted)]">No MoUs.</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Status</th>
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
                  <td>{fmtDate(m.signed_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      <div className="card">
        <h2 className="text-lg mb-3">Locations</h2>
        {locations.length > 0 && (
          <table className="data-table mb-4">
            <thead>
              <tr>
                <th>Name</th>
                <th>Kind</th>
                <th>Code</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {locations.map((l) => (
                <tr key={l.id}>
                  <td>{l.name}</td>
                  <td>{l.kind}</td>
                  <td>{l.code || "—"}</td>
                  <td>
                    <button
                      className="btn-danger"
                      disabled={busy}
                      onClick={() => removeLocation(l.id)}
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <div className="grid gap-3 md:grid-cols-4 items-end">
          <div>
            <label className="field-label">Name</label>
            <input
              className="field-input"
              value={locName}
              onChange={(e) => setLocName(e.target.value)}
              placeholder="Bidibidi Zone 3"
            />
          </div>
          <div>
            <label className="field-label">Kind</label>
            <select
              className="field-input"
              value={locKind}
              onChange={(e) => setLocKind(e.target.value)}
            >
              <option value="admin_large">Admin large</option>
              <option value="admin_small">Admin small</option>
              <option value="service_point">Service point</option>
            </select>
          </div>
          <div>
            <label className="field-label">Code</label>
            <input
              className="field-input"
              value={locCode}
              onChange={(e) => setLocCode(e.target.value)}
            />
          </div>
          <button className="btn-primary" disabled={busy} onClick={addLocation}>
            Add location
          </button>
        </div>
      </div>
    </div>
  );
}

function Row({
  label,
  value,
  mono,
}: {
  label: string;
  value?: string | null;
  mono?: boolean;
}) {
  return (
    <div>
      <dt className="text-[color:var(--color-text-muted)]">{label}</dt>
      <dd className={mono ? "font-mono text-xs" : undefined}>{value || "—"}</dd>
    </div>
  );
}
