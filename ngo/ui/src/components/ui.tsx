"use client";

import Link from "next/link";

export function PageHeader({
  title,
  subtitle,
  action,
}: {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="flex items-start justify-between mb-6 gap-4 flex-wrap">
      <div>
        <h1 className="text-2xl">{title}</h1>
        {subtitle && (
          <p className="text-[color:var(--color-text-muted)] mt-1">{subtitle}</p>
        )}
      </div>
      {action}
    </div>
  );
}

export function StatusPill({ status }: { status: string }) {
  const cls = status.replace(/[^a-z0-9_]/gi, "_");
  return <span className={`status-pill status-${cls}`}>{status.replace(/_/g, " ")}</span>;
}

export function BackLink({ href, label }: { href: string; label: string }) {
  return (
    <Link
      href={href}
      className="text-sm text-[color:var(--color-text-muted)] hover:underline"
    >
      ← {label}
    </Link>
  );
}

export function ErrorBanner({ message }: { message: string | null }) {
  if (!message) return null;
  return (
    <div className="card mb-4 border-[color:var(--color-danger)] text-[color:var(--color-danger)]">
      {message}
    </div>
  );
}

export function Empty({ message }: { message: string }) {
  return (
    <div className="card text-center text-[color:var(--color-text-muted)]">
      {message}
    </div>
  );
}

export function fmtDate(iso?: string | null) {
  if (!iso) return "—";
  const d = new Date(iso);
  return isNaN(d.getTime()) ? iso : d.toLocaleString();
}

const STEPS = ["Verify", "MoU", "Approve", "Provisioned"] as const;

export function GateSteps({ status }: { status: string }) {
  let current = 0;
  if (status === "compliance_passed") current = 1;
  else if (status === "mou_attached") current = 2;
  else if (status === "approved") current = 3;
  else if (status === "rejected") current = -1;

  return (
    <div className="step-rail" aria-label="Onboarding gates">
      {STEPS.map((label, i) => {
        const done = current > i || (current === 3 && i === 3);
        const isCurrent = current === i;
        return (
          <span
            key={label}
            className={
              "step-chip" + (done ? " done" : "") + (isCurrent ? " current" : "")
            }
          >
            {i + 1}. {label}
          </span>
        );
      })}
    </div>
  );
}
