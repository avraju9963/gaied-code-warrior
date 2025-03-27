Architecture Diagram

(A simple high-level overview of the flow)



┌──────────────┐          ┌─────────────────┐
│   User/API   │  ---->   │  FastAPI Server │
└──────────────┘          └─────────────────┘
                                 │
                                 ▼
                     ┌────────────────────┐
                     │   Email Parser     │
                     └────────────────────┘
                                 │
                                 ▼
             ┌─────────────────────────────┐
             │  AI-Based Summarization (NLP) │
             └─────────────────────────────┘
                                 │
                                 ▼
          ┌────────────────────────────┐
          │  Attachment Processing      │
          │ (PDF, Images, DOCX, JSON)   │
          └────────────────────────────┘
                                 │
                                 ▼
               ┌────────────────────────────┐
               │  Forward to External API   │
               └────────────────────────────┘
