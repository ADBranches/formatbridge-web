export default function OcrOptionToggle({
  checked,
  onChange,
  disabled = false,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
      <label className="flex items-start gap-3">
        <input
          type="checkbox"
          checked={checked}
          onChange={(event) => onChange(event.target.checked)}
          disabled={disabled}
          className="mt-1 h-4 w-4 rounded border-slate-300 text-brand-600 focus:ring-brand-500"
        />

        <div>
          <p className="text-sm font-semibold text-slate-900">
            Enable OCR for editable DOCX
          </p>
          <p className="mt-1 text-xs leading-5 text-slate-600">
            When enabled, the app extracts readable text from scanned images and
            writes that text into a DOCX file. When disabled, DOCX export keeps
            the original images embedded in the document.
          </p>
        </div>
      </label>
    </div>
  );
}