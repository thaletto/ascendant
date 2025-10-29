# Ascendant

Ascendant is a modular, multi-astrology intelligence system designed to perform advanced astrological analysis, chart synthesis, and contextual reasoning. Each agent in the Ascendant ecosystem has a clearly defined domain and communicates via shared context, enabling specialized and layered interpreation of astrological data.

## Agent Architecture

**Root Agent** (General Reasoning & Context Manager)
- ChartAgent (Rasi Chart, Saptamsa, Navamsa, etc...)
- DashaAgent (Vimshottari Dasha Analysis)
- YogaAgent (Yogam Analysis)
- PlanetAgent (Positions & Relationships)
- TransitAgent (Current Influence)
- RemedyAgent (Remedial Insights)

## System Architect

### API Endpoints

**Prediction**

- `/predict` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (user's astrology question/request)

- `/predict/health` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (health-related astrology question/request)

- `/predict/career` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (career-related astrology question/request)

- `/predict/wealth` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (wealth-related astrology question/request)

- `/predict/marriage` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (marriage-related astrology question/request)

- `/predict/family` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (family-related astrology question/request)

- `/predict/emotion` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (emotion-related astrology question/request)

- `/predict/love` [POST]

  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (love-related astrology question/request)

- `/predict/children` [POST]
  - `session_id`: string (unique session identifier)
  - `user_id` (optional)
  - `birth_data` (optional)
  - `query`: string (children-related astrology question/request)
