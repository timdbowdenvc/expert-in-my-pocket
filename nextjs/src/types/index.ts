export type DisplayData = string | null;

// Core message types for single-agent chat
export interface Message {
  type: "human" | "ai";
  content: string;
  id: string;
  timestamp: Date;
}

// Single agent response types
export interface AgentMessage {
  parts: { text: string }[];
  role: string;
}

export interface AgentResponse {
  content: AgentMessage;
  usageMetadata: {
    candidatesTokenCount: number;
    promptTokenCount: number;
    totalTokenCount: number;
  };
}

// Timeline event types
export interface TimelineEvent {
  id: string;
  type: "message_sent" | "message_received" | "error";
  title: string;
  description: string;
  timestamp: Date;
  relatedId?: string;
  metadata?: Record<string, unknown>;
}

// SSE event types for streaming
export interface SSEEvent {
  event: string;
  data: string;
}

export interface ProcessedEvent {
  type: "text" | "thought" | "status" | "error";
  content: string;
  timestamp: Date;
  metadata?: Record<string, unknown>;
}

// Chat session types
export interface ChatSession {
  id: string;
  userId: string;
  messages: Message[];
  timeline: TimelineEvent[];
  createdAt: Date;
  updatedAt: Date;
}

// API response types
export type ApiResponse<T> =
  | { success: true; data: T }
  | { success: false; error: string };

// Form types
export interface MessageInput {
  text: string;
}
