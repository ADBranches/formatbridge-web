const DEFAULT_OPTIONS = ["jpg", "png", "webp", "pdf", "docx"];

export default function FormatSelector({
  value,
  onChange,
  options = DEFAULT_OPTIONS,
  label = "Output format",
  disabled = false,
}) {
  return (
    <div>
      <label className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-600">
        {label}
      </label>

      <select
        value={value}
        onChange={(event) => onChange(event.target.value)}
        disabled={disabled}
        className="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm text-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
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