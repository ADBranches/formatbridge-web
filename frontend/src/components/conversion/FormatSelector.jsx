const DEFAULT_OPTIONS = ["jpg", "png", "webp", "pdf", "docx"];

export default function FormatSelector({
  value,
  onChange,
  options = DEFAULT_OPTIONS,
  label = "Output format",
  disabled = false,
}) {
  return (
    <div className="space-y-2">
      <label className="block text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
        {label}
      </label>

      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
        className="h-11 min-w-[170px] rounded-xl border border-slate-300 bg-white px-4 text-sm font-medium text-slate-800 shadow-sm outline-none transition focus:border-brand-500 focus:ring-4 focus:ring-brand-100 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {options.map((format) => (
          <option key={format} value={format}>
            {format.toUpperCase()}
          </option>
        ))}
      </select>
    </div>
  );
}