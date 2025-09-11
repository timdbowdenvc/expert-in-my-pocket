import { NextRequest } from "next/server";
import { MessageInput } from "@/types";

/**
 * Common types shared by all deployment strategies
 */
export interface ProcessedRequest {
  message: MessageInput;
  sessionId: string;
  userId: string;
}

export interface ValidationResult {
  isValid: boolean;
  error?: string;
}

// Legacy interface - use SessionCreationResult from session-service.ts instead
export interface LegacySessionCreationResult {
  sessionId: string;
  created: boolean;
}

/**
 * CORS headers for OPTIONS requests
 */
export const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
} as const;

/**
 * Parse and validate the incoming request body
 */
export async function parseRequest(request: NextRequest): Promise<{
  data: ProcessedRequest | null;
  validation: ValidationResult;
}> {
  try {
    const requestBody = (await request.json()) as {
      message: MessageInput;
      sessionId?: string;
      userId?: string;
    };

    // Validate required fields
    const validation = validateMessageRequest(requestBody);
    if (!validation.isValid) {
      return { data: null, validation };
    }

    // Validate required session and user IDs
    if (!requestBody.sessionId) {
      return {
        data: null,
        validation: {
          isValid: false,
          error: "Session ID is required",
        },
      };
    }

    if (!requestBody.userId) {
      return {
        data: null,
        validation: {
          isValid: false,
          error: "User ID is required",
        },
      };
    }

    const sessionId = requestBody.sessionId;
    const userId = requestBody.userId;

    return {
      data: {
        message: requestBody.message,
        sessionId,
        userId,
      },
      validation: { isValid: true },
    };
  } catch (error) {
    console.error("Request parsing error:", error);
    return {
      data: null,
      validation: {
        isValid: false,
        error: "Invalid request format",
      },
    };
  }
}

/**
 * Validate the message request structure
 */
export function validateMessageRequest(requestBody: {
  message: MessageInput;
  sessionId?: string;
  userId?: string;
}): ValidationResult {
  if (!requestBody.message?.text) {
    return {
      isValid: false,
      error: "Message text is required",
    };
  }

  if (typeof requestBody.message.text !== "string") {
    return {
      isValid: false,
      error: "Message text must be a string",
    };
  }

  if (requestBody.message.text.trim().length === 0) {
    return {
      isValid: false,
      error: "Message text cannot be empty",
    };
  }

  return { isValid: true };
}

/**
 * Format message data into a message string
 */
export function formatMessage(message: MessageInput): string {
  return message.text;
}

/**
 * Centralized logging for revision assistant operations
 */
export function logRevisionAssistantRequest(
  sessionId: string,
  userId: string,
  message: MessageInput,
  deploymentType: "agent_engine" | "local_backend"
): void {
  console.log(
    `📡 Revision Assistant API [${deploymentType}] - Session: ${sessionId}, User: ${userId}`
  );
  console.log(`📡 Message:`, message);
}
