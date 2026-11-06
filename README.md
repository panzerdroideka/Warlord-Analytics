# Warlord Analytics

Data-driven analysis of Lord of the Rings Online gameplay using combat logs, MangoHud telemetry, configuration snapshots, videos and mission benchmarks.

# Purpose
This repository exists to answer a simple question:

What actually makes missions faster?

Instead of focusing only on DPS, this project studies:

Mission completion time
Combat efficiency
Skill usage patterns
Player movement and positioning
Frame pacing and frametime stability
Graphics settings impact
Linux gaming performance
Rune-Keeper optimization
Current Toolchain
Data Collection
scripts/collect_logs.py Collects and organizes source data.
Reporting
scripts/inventory_report.py Generates file inventory reports.

scripts/lotro_report.py Creates LotRO-specific reports.

Duplicate Analysis
scripts/find_true_duplicates.py Finds SHA256 verified duplicate files.

scripts/cleanup_candidates.py Builds duplicate candidate lists.

Cleanup
hybelkaninjakt.py Verifies duplicate families, identifies master copies, creates cleanup reports, and safely sends verified duplicates to the system trash.
Current Capabilities
File inventory generation
SHA256 duplicate verification
Duplicate family grouping
Safe duplicate cleanup
Trash-based recovery
LotRO log collection
Mission analytics foundation
Development Roadmap
Current
✅ File inventory

✅ Duplicate analysis

✅ Safe duplicate cleanup

Next
Mission performance analysis
Mission reward analysis
Character comparison
Session efficiency metrics
Skill usage statistics
Combat effectiveness tracking

## Data Sources

### Combat Logs

- Native LotRO combat logs
- Full mission captures
- Boss encounters
- Skill usage statistics

### MangoHud Telemetry

- FPS
- Frametime
- GPU utilization
- CPU utilization
- Temperatures
- VRAM and RAM usage

### Configuration Snapshots

- UserPreferences.ini
- MangoHud settings
- System benchmarks

## Repository Structure

combat_logs/
mangohud/
userprefs/
missions/
analytics/
scripts/
benchmarks/

## Philosophy

The goal is not maximum DPS.

The goal is:

- Fewer keypresses
- Smoother gameplay
- Faster mission completion
- Better situational awareness
- Efficient solo gameplay

"If it isn't documented, it didn't happen."

This is the Way!

- The Warlord
