'use client';

import { useCallback, useEffect } from "react";
import { useStreaming } from "@/hooks/useStreaming";
import { useBackendHealth } from "@/hooks/useBackendHealth";
import { StreamEvent, StreamProcessingCallbacks } from "@/lib/streaming/types";

interface StreamingManagerProps extends StreamProcessingCallbacks {
  userId: string;
  sessionId: string;
  onLoadingChange?: (isLoading: boolean) => void;
}

export interface StreamingManagerReturn {
  isLoading: boolean;
  currentAgent: string;
  submitMessage: (message: string) => Promise<void>;
  cancelStream: () => void;
}

/**
 * Streaming management component that coordinates SSE streaming
 * Uses the useStreaming hook for stream processing and useBackendHealth for retry logic
 */
export function useStreamingManager({
  userId,
  sessionId,
  onLoadingChange,
  onMessageUpdate,
  onEventUpdate,
  onWebsiteCountUpdate,
}: StreamingManagerProps): StreamingManagerReturn {
  const { retryWithBackoff } = useBackendHealth();

  const { isLoading, currentAgent, startStream, cancelStream } = useStreaming({
    retryFn: retryWithBackoff,
    onMessageUpdate,
    onEventUpdate,
    onWebsiteCountUpdate,
  });

  useEffect(() => {
    if (onLoadingChange) {
      onLoadingChange(isLoading);
    }
  }, [isLoading, onLoadingChange]);

  const submitMessage = useCallback(
    async (message: string): Promise<void> => {
      if (!message.trim() || !userId || !sessionId) {
        throw new Error("Message, userId, and sessionId are required");
      }

      const apiPayload = {
        message: message.trim(),
        userId,
        sessionId,
      };

      await startStream(apiPayload);
    },
    [userId, sessionId, startStream]
  );

  return {
    isLoading,
    currentAgent,
    submitMessage,
    cancelStream,
  };
}
