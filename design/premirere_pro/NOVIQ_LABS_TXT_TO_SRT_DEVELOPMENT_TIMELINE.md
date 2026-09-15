# TXT-to-SRT Converter Development Timeline

**Organization:** Noviq Labs Ltd  
**Implementation language:** PHP  
**Delivery approach:** Fast-track development  
**Prepared:** 15 September 2026  
**Target duration:** 4 working days

## 1. Project Goal

Build a lightweight PHP utility that converts manually edited lyric `.txt` files into valid UTF-8 `.srt` subtitle files for import into Adobe Premiere Pro.

The first release will prioritize accurate conversion, timestamp validation, a fast editing workflow, batch processing, and clear error reporting. It will not perform automatic speech transcription.

## 2. Input Format for the MVP

The recommended editable TXT structure is:

```text
00:00:05,000 | 00:00:08,500 | First lyric line
00:00:08,500 | 00:00:12,000 | Second lyric line
```

The generated SRT structure will be:

```srt
1
00:00:05,000 --> 00:00:08,500
First lyric line

2
00:00:08,500 --> 00:00:12,000
Second lyric line
```

## 3. Noviq Labs Ltd Brand Application

The interface, documentation examples, status messages, and any later web dashboard will use the official Noviq Labs Ltd colors through centralized design tokens rather than scattered hard-coded values.

The public search performed during planning did not identify a verified Uganda-specific Noviq Labs Ltd brand palette. Therefore, exact HEX values must be copied from the approved company brand kit during project initialization. No colors should be guessed.

Planned tokens:

```css
--noviq-primary: BRAND_KIT_PRIMARY_HEX;
--noviq-secondary: BRAND_KIT_SECONDARY_HEX;
--noviq-accent: BRAND_KIT_ACCENT_HEX;
--noviq-background: BRAND_KIT_BACKGROUND_HEX;
--noviq-text: BRAND_KIT_TEXT_HEX;
--noviq-success: BRAND_KIT_SUCCESS_HEX;
--noviq-error: BRAND_KIT_ERROR_HEX;
```

## 4. Development Timeline

### Phase 1: Requirements, Repository Setup, and File Specification

**Duration:** 0.5 working day  
**Target:** Day 1, morning

#### Objectives

- Define the supported TXT syntax and expected SRT output.
- Establish the PHP version and required extensions.
- Confirm Premiere-compatible UTF-8 output and SRT timestamp formatting.
- Define validation rules for missing, invalid, reversed, and overlapping timestamps.
- Define exit codes and terminal status messages.
- Insert the approved Noviq Labs Ltd color values into centralized tokens.
- Prepare representative valid and invalid lyric samples.

#### Files to create

- `README.md`
- `docs/INPUT_FORMAT.md`
- `docs/VALIDATION_RULES.md`
- `docs/BRAND_TOKENS.md`
- `composer.json`
- `.gitignore`
- `.editorconfig`
- `phpunit.xml`
- `config/brand.php`
- `samples/lyrics-valid.txt`
- `samples/lyrics-invalid.txt`
- `samples/expected-output.srt`

#### Completion gate

- Input syntax is documented.
- Output format is documented.
- Official color tokens are recorded from the approved brand kit.
- Sample inputs and expected output are ready.
- PHP and Composer requirements are explicit.

---

### Phase 2: Core TXT Parser and SRT Conversion Engine

**Duration:** 1 working day  
**Target:** Day 1 afternoon through Day 2 morning

#### Objectives

- Read TXT files safely using UTF-8.
- Ignore blank lines without corrupting subtitle numbering.
- Parse start time, end time, and lyric text.
- Normalize supported timestamp variants into `HH:MM:SS,mmm`.
- Generate sequential SRT caption indexes.
- Preserve lyric punctuation and Unicode characters.
- Reject malformed rows with precise line-number errors.
- Prevent accidental overwriting unless explicitly enabled.

#### Files to create

- `bin/txt-to-srt`
- `src/Application/ConvertTxtToSrt.php`
- `src/Domain/Caption.php`
- `src/Parser/LyricTxtParser.php`
- `src/Formatter/SrtFormatter.php`
- `src/Support/FileEncoding.php`
- `src/Support/ConversionResult.php`
- `src/Exception/ConversionException.php`

#### Files to modify

- `composer.json`
- `README.md`
- `docs/INPUT_FORMAT.md`

#### Completion gate

- A valid TXT file converts into a structurally correct SRT file.
- Output numbering is continuous.
- Output timestamps use commas for milliseconds.
- Generated files are UTF-8 encoded.
- Invalid source lines report their exact line numbers.

---

### Phase 3: Validation, Repair, and Premiere-Ready Output

**Duration:** 0.75 working day  
**Target:** Day 2 afternoon

#### Objectives

- Validate timestamp shape and numeric ranges.
- Ensure each end time occurs after its start time.
- Detect overlapping captions.
- Detect empty lyric text.
- Normalize line endings across Linux, macOS, and Windows.
- Remove a UTF-8 byte-order mark if present in source files.
- Add an optional safe repair mode for minor formatting mistakes.
- Validate the generated SRT before writing the final output.

#### Files to create

- `src/Validation/TimestampValidator.php`
- `src/Validation/CaptionValidator.php`
- `src/Validation/SrtValidator.php`
- `src/Repair/SafeInputRepairer.php`
- `src/Support/Timecode.php`
- `docs/ERROR_REFERENCE.md`

#### Files to modify

- `bin/txt-to-srt`
- `src/Application/ConvertTxtToSrt.php`
- `src/Parser/LyricTxtParser.php`
- `src/Formatter/SrtFormatter.php`
- `README.md`

#### Completion gate

- Malformed timestamps fail safely.
- Reversed timestamps fail safely.
- Overlaps are reported clearly.
- Repair mode changes only explicitly supported minor errors.
- The final SRT passes the internal validator before being saved.

---

### Phase 4: Batch Conversion and Fast Terminal Workflow

**Duration:** 0.5 working day  
**Target:** Day 3, morning

#### Objectives

- Convert one TXT file or an entire directory.
- Add recursive processing as an explicit option.
- Support a configurable output directory.
- Add `--overwrite`, `--repair`, `--recursive`, `--dry-run`, and `--help` options.
- Return reliable shell exit codes.
- Print a concise conversion summary containing passed, skipped, and failed counts.
- Apply Noviq Labs Ltd status-color tokens where the terminal supports ANSI colors.
- Automatically disable terminal colors when output is redirected.

#### Files to create

- `src/Console/ConvertCommand.php`
- `src/Console/TerminalTheme.php`
- `src/Application/BatchConverter.php`
- `src/Support/PathResolver.php`
- `docs/CLI_REFERENCE.md`

#### Files to modify

- `bin/txt-to-srt`
- `config/brand.php`
- `composer.json`
- `README.md`

#### Completion gate

- Single-file and directory conversions work.
- Dry-run performs validation without creating SRT files.
- Existing outputs are protected by default.
- Terminal summaries and exit codes accurately reflect results.

---

### Phase 5: Automated Tests and Quality Verification

**Duration:** 0.75 working day  
**Target:** Day 3 afternoon

#### Objectives

- Test valid conversion from TXT to SRT.
- Test Unicode lyrics and punctuation.
- Test blank lines, malformed separators, invalid timestamps, overlaps, and empty lyrics.
- Test overwrite protection and batch conversion.
- Compare generated output with fixed expected SRT fixtures.
- Add static analysis and coding-style checks.
- Perform a real import test in Adobe Premiere Pro using a short sample sequence.

#### Files to create

- `tests/Unit/LyricTxtParserTest.php`
- `tests/Unit/SrtFormatterTest.php`
- `tests/Unit/TimestampValidatorTest.php`
- `tests/Unit/SrtValidatorTest.php`
- `tests/Feature/ConvertCommandTest.php`
- `tests/Feature/BatchConversionTest.php`
- `tests/Fixtures/valid-lyrics.txt`
- `tests/Fixtures/invalid-lyrics.txt`
- `tests/Fixtures/unicode-lyrics.txt`
- `tests/Fixtures/expected-valid.srt`
- `phpstan.neon`
- `phpcs.xml`
- `docs/PREMIERE_IMPORT_TEST.md`

#### Files to modify

- `composer.json`
- `README.md`

#### Completion gate

- All unit and feature tests pass.
- Static analysis and coding-style checks pass.
- No failed conversion is falsely reported as successful.
- A generated SRT imports into Premiere Pro and creates a usable caption track.

---

### Phase 6: Packaging, Usage Guide, and Release

**Duration:** 0.5 working day  
**Target:** Day 4, morning

#### Objectives

- Finalize installation and usage instructions.
- Provide copy-ready TXT templates for lyric editors.
- Document the Premiere import workflow.
- Add troubleshooting guidance for encoding, timing, and file-extension problems.
- Package the first stable release.
- Create a changelog and version marker.

#### Files to create

- `CHANGELOG.md`
- `VERSION`
- `docs/QUICK_START.md`
- `docs/PREMIERE_IMPORT_GUIDE.md`
- `docs/TROUBLESHOOTING.md`
- `templates/lyrics-template.txt`
- `templates/lyrics-template-with-notes.txt`

#### Files to modify

- `README.md`
- `composer.json`

#### Completion gate

- A new user can install and run the converter from the documentation.
- Template TXT files convert without manual restructuring.
- The release package contains no temporary or test-output files.
- Version `1.0.0` is tagged only after every required check passes.

## 5. Final Version 1.0.0 File Structure

```text
txt-to-srt-converter/
├── bin/
│   └── txt-to-srt
├── config/
│   └── brand.php
├── docs/
│   ├── BRAND_TOKENS.md
│   ├── CLI_REFERENCE.md
│   ├── ERROR_REFERENCE.md
│   ├── INPUT_FORMAT.md
│   ├── PREMIERE_IMPORT_GUIDE.md
│   ├── PREMIERE_IMPORT_TEST.md
│   ├── QUICK_START.md
│   ├── TROUBLESHOOTING.md
│   └── VALIDATION_RULES.md
├── samples/
│   ├── expected-output.srt
│   ├── lyrics-invalid.txt
│   └── lyrics-valid.txt
├── src/
│   ├── Application/
│   ├── Console/
│   ├── Domain/
│   ├── Exception/
│   ├── Formatter/
│   ├── Parser/
│   ├── Repair/
│   ├── Support/
│   └── Validation/
├── templates/
│   ├── lyrics-template.txt
│   └── lyrics-template-with-notes.txt
├── tests/
│   ├── Feature/
│   ├── Fixtures/
│   └── Unit/
├── .editorconfig
├── .gitignore
├── CHANGELOG.md
├── composer.json
├── phpcs.xml
├── phpstan.neon
├── phpunit.xml
├── README.md
└── VERSION
```

## 6. Definition of Done

Version 1.0.0 is complete only when:

- TXT lyrics convert to valid SRT captions.
- The generated file is UTF-8 encoded.
- Caption indexes and timestamps are valid.
- Invalid or overlapping timestamps are reported accurately.
- Existing files are not overwritten without authorization.
- Batch conversion returns truthful counts and exit codes.
- Automated checks pass without errors.
- The sample SRT imports successfully into Adobe Premiere Pro.
- Official Noviq Labs Ltd color values are used from one centralized configuration.
- Installation, editing, conversion, and import instructions are complete.

## 7. Work Prioritization

To move quickly, development should remain focused on the critical path:

1. Freeze the TXT input format.
2. Build the parser and formatter.
3. Add strict validation.
4. Add batch conversion.
5. Complete automated and Premiere import testing.
6. Package version 1.0.0.

Automatic transcription, translation, graphical interfaces, waveform synchronization, and cloud uploads should remain outside version 1.0.0 unless the core converter is already complete and verified.
