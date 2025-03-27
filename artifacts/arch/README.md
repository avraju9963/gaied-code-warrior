

```mermaid
graph TD;
    A[Start: User Uploads .eml File] --> B[FastAPI Server Receives Request];
    B --> C[Validate Email File];
    C --> D[Extract Metadata, Body, and Attachments];
    
    D -->|Attachments Exist| E[Process Attachments];
    D -->|No Attachments| F[Summarization Module];

    E --> G[Extract Text from PDFs or Images (OCR)];
    G --> H[Extract Text from DOCX, JSON, XML];
    H --> F;
    
    F[AI Summarization Module] --> I[Generate Summary];
    
    I --> J{Forward Email?};
    J -->|Yes| K[Forward to External API];
    J -->|No| L[Store in Database];

    K --> M[End: Email Forwarded];
    L --> M[End: Email Stored];
