# Data-Processing

# Talus Subsystem Data Processing

This repository handles data processing for various subsystems at the Talus ammonia production site.

## Current Modules
1. **Hydrogen Generation**  
   Processes `[PLC1]ACTUAL_FLOW` from electrolyzer logs (Nm³/hr)

2. **Oxygen Trace Monitoring**  
   Processes `[PLC1]ZQ_AI_AT1101` for O₂ concentration in the hydrogen stream (ppm)

## Notes
- Input data is resampled to 5-minute intervals.
- Outputs are saved for analysis and visualization.
- More subsystems and data sources will be integrated over time.
