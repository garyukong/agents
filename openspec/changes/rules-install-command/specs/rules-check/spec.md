## ADDED Requirements

### Requirement: Check installed symlinks
The system SHALL scan known provider install directories and report the health of any symlinks found.

#### Scenario: All symlinks healthy
- **WHEN** `rules check` is run and all installed symlinks resolve correctly
- **THEN** the system SHALL print each symlink path with an OK status

#### Scenario: Broken symlink detected
- **WHEN** a symlink exists but its target no longer exists (agents repo moved or file deleted)
- **THEN** the system SHALL report the symlink as broken with its path and the missing target

#### Scenario: No installed rules found
- **WHEN** none of the known provider directories contain symlinks
- **THEN** the system SHALL print a message indicating no installed rules were found

#### Scenario: Mixed health report
- **WHEN** some symlinks are healthy and some are broken
- **THEN** the system SHALL report each symlink individually with its status
- **THEN** the system SHALL exit with a non-zero code if any broken symlinks exist
