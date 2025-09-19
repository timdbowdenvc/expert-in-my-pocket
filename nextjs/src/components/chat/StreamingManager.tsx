"use client";

import { useCallback, useEffect } from "react";
import { useStreaming } from "@/hooks/useStreaming";
import { useBackendHealth } from "@/hooks/useBackendHealth";
import { StreamEvent } from "@/lib/streaming/types";

interface StreamingManagerProps {
  userId: string;
  sessionId: string;
  onLoadingChange?: (isLoading: boolean) => void;
}

export interface StreamingManagerReturn {
  isLoading: boolean;
  submitMessage: (message: string) => ReadableStream<StreamEvent>;
}

/**
 * Streaming management component that coordinates SSE streaming
 * Uses the useStreaming hook for stream processing and useBackendHealth for retry logic
 */
export function useStreamingManager({
  userId,
  sessionId,
  onLoadingChange,
}: StreamingManagerProps): StreamingManagerReturn {
  const { retryWithBackoff } = useBackendHealth();

  const { isLoading, startStream } = useStreaming(retryWithBackoff);

  useEffect(() => {
    if (onLoadingChange) {
      onLoadingChange(isLoading);
    }
  }, [isLoading, onLoadingChange]);

  const submitMessage = useCallback(
    (message: string): ReadableStream<StreamEvent> => {
      if (!message.trim() || !userId || !sessionId) {
        throw new Error("Message, userId, and sessionId are required");
      }

      const apiPayload = {
        message: message.trim(),
        userId,
        sessionId,
      };

      return startStream(apiPayload);
    },
    [userId, sessionId, startStream]
  );

  return {
    isLoading,
    submitMessage,
  };
}