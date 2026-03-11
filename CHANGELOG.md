# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-03-12

Initial release: expressive shapes and morphing for everyone.

### Added

- `RoundedPolygon` - polygons with per-vertex corner rounding and smoothing (Material Design 3 spec)
- `Morph` - feature-aware shape morphing with greedy corner mapping, arc-length measurement, and lockstep curve walking
- `CornerRounding` - per-vertex control of corner radius and smoothing
- Core geometry primitives: `Point`, `Cubic`, `Feature`
- `MeasuredPolygon` and `DoubleMapper` for arc-length-based progress mapping between shapes
- 30+ built-in shape presets (circle, star, heart, clover, ghost, pixel shapes, etc.)
- Debug mode (`expressive_shapes.DEBUG = True`) for detailed morph tracing
- Cairo and GTK/Fabric rendering examples

### Infrastructure
- GitHub Actions CI workflow for PyPI publishing
