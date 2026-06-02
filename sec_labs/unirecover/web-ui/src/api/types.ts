export interface CanonicalFileRecord {
    id: string;
    path: string;
    size_bytes: number;
    sha256_hash: string;
    confidence: number;
    metadata: Record<string, any>;
}

export interface CaseContext {
    case_number: string;
    investigator: string;
    authorizing_supervisor: string;
    judicial_reference: string;
    status: 'ACTIVE' | 'ARCHIVED';
}
