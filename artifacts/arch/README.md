Architecture Diagram

(A simple high-level overview of the flow)

graph TD;
    A[User Uploads Email] -->|API Request| B[FastAPI Server];
    B --> C[Email Parser];
    C -->|Extracts Attachments & Body| D[Attachment Processor];
    D -->|Extracts OCR, PDF, DOCX| E[AI Summarization];
    E -->|Summarized Data| F[Forwarding Service];
    F -->|Send Data to API| G[External System];

![image](https://github.com/user-attachments/assets/c97117bb-2116-46f8-9be1-978f9f9a386d)



