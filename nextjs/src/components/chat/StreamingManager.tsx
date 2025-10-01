'use client';

import { useCallback, useEffect, useRef } from "react";
import { useStreaming } from "@/hooks/useStreaming";
import { useBackendHealth } from "@/hooks/useBackendHealth";
import { StreamProcessingCallbacks } from "@/lib/streaming/types";

interface StreamingManagerProps extends StreamProcessingCallbacks {
  userId: string;
  sessionId: string;
  onLoadingChange?: (isLoading: boolean) => void;
  debug?: boolean; // Add debug flag
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
  debug = false,
}: StreamingManagerProps): StreamingManagerReturn {
  const { retryWithBackoff } = useBackendHealth();
  
  // Track if component is mounted to prevent state updates after unmount
  const isMountedRef = useRef(true);
  
  // Create stable callback references with logging
  const stableOnMessageUpdate = useCallback((update: any) => {
    if (debug) {
      console.log('[StreamingManager] Message update received:', update);
    }
    if (isMountedRef.current) {
      onMessageUpdate?.(update);
    }
  }, [onMessageUpdate, debug]);

  const stableOnEventUpdate = useCallback((update: any) => {
    if (debug) {
      console.log('[StreamingManager] Event update received:', update);
    }
    if (isMountedRef.current) {
      onEventUpdate?.(update);
    }
  }, [onEventUpdate, debug]);

  const stableOnWebsiteCountUpdate = useCallback((count: number) => {
    if (debug) {
      console.log('[StreamingManager] Website count update:', count);
    }
    if (isMountedRef.current) {
      onWebsiteCountUpdate?.(count);
    }
  }, [onWebsiteCountUpdate, debug]);

  const { isLoading, currentAgent, startStream, cancelStream } = useStreaming({
    retryFn: retryWithBackoff,
    onMessageUpdate: stableOnMessageUpdate,
    onEventUpdate: stableOnEventUpdate,
    onWebsiteCountUpdate: stableOnWebsiteCountUpdate,
  });

  useEffect(() => {
    return () => {
      isMountedRef.current = false;
    };
  }, []);

  useEffect(() => {
    if (debug) {
      console.log('[StreamingManager] Loading state changed:', isLoading);
    }
    if (onLoadingChange) {
      onLoadingChange(isLoading);
    }
  }, [isLoading, onLoadingChange, debug]);

  const submitMessage = useCallback(
    async (message: string): Promise<void> => {
      if (debug) {
        console.log('[StreamingManager] Submit started', { 
          message: message.substring(0, 50) + '...', 
          userId, 
          sessionId 
        });
      }

      if (!message.trim() || !userId || !sessionId) {
        const error = new Error("Message, userId, and sessionId are required");
        if (debug) {
          console.error('[StreamingManager] Validation error:', error);
        }
        throw error;
      }

      const apiPayload = {
        message: message.trim(),
        userId,
        sessionId,
      };

      try {
        await startStream(apiPayload);
        if (debug) {
          console.log('[StreamingManager] Stream completed successfully');
        }
      } catch (error) {
        if (debug) {
          console.error('[StreamingManager] Stream error:', error);
        }
        throw error;
      }
    },
    [userId, sessionId, startStream, debug]
  );

  return {
    isLoading,
    currentAgent,
    submitMessage,
    cancelStream,
  };
}