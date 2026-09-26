# AI Doctor Appointment Booking Agent

A conversational Telegram agent that handles the full doctor appointment lifecycle — discovery, booking, cancellation, and rescheduling — without any manual staff involvement.

## Problem

Manual appointment scheduling for a healthcare provider is slow, depends entirely on staff availability, and doesn't scale outside business hours.

## Solution

Built a database-backed conversational agent on Telegram that:
- Lets patients discover available doctors and open slots through natural language, backed by real-time PostgreSQL queries
- Handles the entire booking lifecycle — booking, cancellation, and rescheduling — directly through chat
- Runs on a webhook-based architecture, so there's no polling and no manual coordination needed

## Architecture

```
Telegram User
      |
      v
Telegram Bot API (Webhook)
      |
      v
FastAPI Backend
      |
      v
PostgreSQL (doctors, slots, appointments)
```

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| Messaging | Telegram Bot API, Webhooks |

## Key Features

- **Natural-language doctor discovery** — real-time SQL lookups for doctor availability and open slots
- **Full appointment lifecycle** — booking, cancellation, and rescheduling handled conversationally
- **Webhook-driven** — no polling, appointments update the moment a patient interacts with the bot

## Setup

```bash
git clone <repo-url>
cd doctor-appointment-agent
pip install -r requirements.txt
cp .env.example .env   # fill in your bot token and DB credentials (never commit .env)
uvicorn main:app --reload
```

## Environment Variables

Requires a Telegram Bot token and PostgreSQL connection string — see `.env.example`. None of these are committed to this repository.

## Status

An independent project, designed and built solo end-to-end.
