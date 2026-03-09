# VelocityTracker

The VelocityTracker (`signal/velocity.py`) monitors signal frequency over time to detect accelerating, stable, and decelerating topics. It provides the temporal dimension that transforms point-in-time signals into trend intelligence.

## Architecture

- **Storage**: SQLite database (`velocity.db` in `STATE_DIR`)
- **Window**: 7-day sliding window
- **Granularity**: Per-topic tracking (topics derived from EntityScorer NER output)

## Per-Topic Outputs

For each tracked topic, the VelocityTracker maintains:

| Field | Type | Description |
|-------|------|-------------|
| direction | enum | `accelerating`, `stable`, or `decelerating` |
| velocity | float | Signals per day (rolling average) |
| acceleration | float | Rate of change in velocity (ratio of current vs. prior window half) |
| signal_count | int | Total signals in the current 7-day window |

## Direction Classification

- **Accelerating**: Acceleration ratio > 1.5 (signal frequency increasing by 50%+ over the window)
- **Stable**: Acceleration ratio between 0.67 and 1.5
- **Decelerating**: Acceleration ratio < 0.67 (signal frequency dropping by 33%+)

## Methods

### heat_map()
Returns a dictionary of all topics with their current velocity and direction. Used by the curator planner to prioritize cook orders -- accelerating topics get higher `market_heat` scores and earlier scheduling.

### top_movers()
Returns the N topics with the highest absolute acceleration (both up and down). Useful for dashboard display and Discord alerts.

## Integration with Curator

The VelocityTracker feeds directly into the curator planner (`curator/planner.py`):

```
VelocityTracker.heat_map()
  -> accelerating topics get higher market_heat
  -> planner generates prioritized cook orders
  -> cook orders flow to factory for pair generation
```

This creates a feedback loop: real-world signal acceleration drives dataset production toward the topics that matter most right now.

## Database Schema

The SQLite database stores raw signal timestamps per topic, enabling arbitrary window calculations without holding everything in memory. Old entries beyond the 7-day window are periodically pruned.
