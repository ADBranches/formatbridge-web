const ALLOWED_EXTENSIONS = ["heic", "heif", "jpg", "jpeg", "png", "webp", "gif"];
const ALLOWED_MIME_TYPES = [
  "image/heic",
  "image/heif",
  "image/jpeg",
  "image/png",
  "image/webp",
  "image/gif",
];

const EXTENSION_MIME_FALLBACKS = {
  heic: ["application/octet-stream"],
  heif: ["application/octet-stream"],
};

const MAX_FILES = 10;
const MAX_FILE_SIZE_MB = 8;
const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;

export function getFileExtension(filename = "") {
  return filename.includes(".") ? filename.split(".").pop().toLowerCase() : "";
}

export function formatFileSize(bytes = 0) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
}

function isMimeAllowedForExtension(extension, mimeType) {
  if (ALLOWED_MIME_TYPES.includes(mimeType)) return true;
  return (EXTENSION_MIME_FALLBACKS[extension] || []).includes(mimeType);
}

export function validateFilesClientSide(files) {
  const errors = [];
  const validFiles = [];

  if (files.length > MAX_FILES) {
    errors.push(`You can upload at most ${MAX_FILES} files at once.`);
  }

  files.slice(0, MAX_FILES).forEach((file) => {
    const extension = getFileExtension(file.name);

    if (!ALLOWED_EXTENSIONS.includes(extension)) {
      errors.push(`${file.name}: unsupported extension.`);
      return;
    }

    if (file.type && !isMimeAllowedForExtension(extension, file.type)) {
      errors.push(`${file.name}: unsupported MIME type (${file.type}).`);
      return;
    }

    if (file.size > MAX_FILE_SIZE_BYTES) {
      errors.push(`${file.name}: exceeds ${MAX_FILE_SIZE_MB} MB limit.`);
      return;
    }

    validFiles.push(file);
  });

  return { validFiles, errors };
}