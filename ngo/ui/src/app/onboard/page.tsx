"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { NgoRequest } from "@/lib/types";
import { PageHeader, ErrorBanner } from "@/components/ui";

export default function OnboardPage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [shortCode, setShortCode] = useState("");
  const [registrationNumber, setRegistrationNumber] = useState("");
  const [ursb, setUrsb] = useState("");
  const [bureau, setBureau] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!name.trim()) {
      setError("Organisation name is required.");
      return;
    }
    setBusy(true);
    setError(null);
    try {
      const res = await api.post<NgoRequest>("/onboard", {
        name: name.trim(),
        short_code: shortCode.trim() || null,
        registration_number: registrationNumber.trim() || null,
        ursb_number: ursb.trim() || null,
        ngo_bureau_number: bureau.trim() || null,
        contact_email: email.trim() || null,
        contact_phone: phone.trim() || null,
        legal_address: address.trim() || null,
        notes: notes.trim() || null,
        submitted_by: "opm.staff",
      });
      router.push(`/requests/${res.id}`);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
      setBusy(false);
    }
  }

  return (
    <div>
      <PageHeader
        title="Onboard partner"
        subtitle="File a partner application. Gate order: Verify → MoU → Approve → provision Agent / Agency / Program."
      />
      <ErrorBanner message={error} />

      <form onSubmit={submit} className="card max-w-2xl space-y-4">
        <div>
          <label className="field-label">Organisation name *</label>
          <input
            className="field-input"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className="field-label">Short code</label>
            <input
              className="field-input"
              value={shortCode}
              onChange={(e) => setShortCode(e.target.value)}
              placeholder="HOPE-UG"
            />
          </div>
          <div>
            <label className="field-label">Registration number</label>
            <input
              className="field-input"
              value={registrationNumber}
              onChange={(e) => setRegistrationNumber(e.target.value)}
            />
          </div>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className="field-label">URSB number</label>
            <input
              className="field-input"
              value={ursb}
              onChange={(e) => setUrsb(e.target.value)}
              placeholder="URSB-…"
            />
          </div>
          <div>
            <label className="field-label">NGO Bureau number</label>
            <input
              className="field-input"
              value={bureau}
              onChange={(e) => setBureau(e.target.value)}
              placeholder="NB-…"
            />
          </div>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label className="field-label">Contact email</label>
            <input
              className="field-input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <label className="field-label">Contact phone</label>
            <input
              className="field-input"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
          </div>
        </div>
        <div>
          <label className="field-label">Legal address</label>
          <textarea
            className="field-input"
            rows={2}
            value={address}
            onChange={(e) => setAddress(e.target.value)}
          />
        </div>
        <div>
          <label className="field-label">Notes</label>
          <textarea
            className="field-input"
            rows={2}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>
        <div className="flex gap-2 pt-2">
          <button type="submit" className="btn-primary" disabled={busy}>
            {busy ? "Submitting…" : "Submit onboarding request"}
          </button>
        </div>
      </form>
    </div>
  );
}
