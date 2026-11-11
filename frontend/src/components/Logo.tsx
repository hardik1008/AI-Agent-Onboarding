import clsx from "clsx";

export function Logo({ inverted }: { inverted?: boolean }) {
  return (
    <span className="inline-flex items-center gap-2">
      <span
        className={clsx(
          "flex h-8 w-8 items-center justify-center rounded-lg text-sm font-bold",
          inverted ? "bg-white text-brand-800" : "bg-brand-700 text-white",
        )}
        aria-hidden
      >
        PN
      </span>
      <span className={clsx("text-lg font-semibold tracking-tight", inverted ? "text-white" : "text-slate-900")}>
        PolicyNest
      </span>
    </span>
  );
}
