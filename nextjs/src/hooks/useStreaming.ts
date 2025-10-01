import { useState, useCallback, useRef } from "react";
import { StreamingConnectionManager } from "@/lib/streaming/connection-manager";
import { getEventTitle } from "@/lib/streaming/stream-utils";
import {
  StreamingAPIPayload,
  StreamProcessingCallbacks,
} from "@/lib/streaming/types";
import { processSseEventData } from "@/lib/streaming/stream-processor";

export interface UseStreamingProps extends StreamProcessingCallbacks {
  retryFn: <T>(fn: () => Promise<T>) => Promise<T>;
}

export interface UseStreamingReturn {
  isLoading: boolean;
  currentAgent: string;
  startStream: (apiPayload: { message: string; userId: string; sessionId: string }) => Promise<void>;
  cancelStream: () => void;
  getEventTitle: (agentName: string) => string;
}

/**
 * Custom hook for managing SSE streaming connections and data processing
 */
export function useStreaming({
  retryFn,
  onMessageUpdate,
  onEventUpdate,
  onWebsiteCountUpdate,
}: UseStreamingProps): UseStreamingReturn {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [currentAgent, setCurrentAgent] = useState<string>("");
  const accumulatedTextRef = useRef<string>("");
  const currentAgentRef = useRef<string>("");

  const connectionManager = useRef<StreamingConnectionManager | null>(null);

  if (connectionManager.current === null) {
    connectionManager.current = new StreamingConnectionManager({
      retryFn,
      endpoint: "/api/run_sse",
    });
  }

  const startStream = useCallback(
    async (apiPayload: { message: string; userId: string; sessionId: string }): Promise<void> => {
      if (!connectionManager.current) {
        throw new Error("Connection manager not initialized");
      }

      setIsLoading(true);
      accumulatedTextRef.current = "";
      currentAgentRef.current = "";

      const streamingPayload: StreamingAPIPayload = {
        message: apiPayload.message,
        userId: apiPayload.userId,
        sessionId: apiPayload.sessionId,
      };

      try {
        const response = await connectionManager.current.submitMessage(streamingPayload);
        const aiMessageId = response.headers.get("X-Message-Id") || `ai-${Date.now()}`;

        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error("No readable stream available");
        }

        const decoder = new TextDecoder();
        let lineBuffer = "";
        let eventDataBuffer = "";

        const pump = async (): Promise<void> => {
          const { done, value } = await reader.read();

          if (value) {
            const chunk = decoder.decode(value, { stream: true });
            lineBuffer += chunk;
          }

          let eolIndex;
          while (
            (eolIndex = lineBuffer.indexOf("\n")) >= 0 ||
            (done && lineBuffer.length > 0)
          ) {
            let line: string;
            if (eolIndex >= 0) {
              line = lineBuffer.substring(0, eolIndex);
              lineBuffer = lineBuffer.substring(eolIndex + 1);
            } else {
              line = lineBuffer;
              lineBuffer = "";
            }

            if (line.trim() === "") {
              if (eventDataBuffer.length > 0) {
                const jsonDataToParse = eventDataBuffer.endsWith("\n")
                  ? eventDataBuffer.slice(0, -1)
                  : eventDataBuffer;

                await processSseEventData(
                  jsonDataToParse,
                  aiMessageId,
                  { onMessageUpdate, onEventUpdate, onWebsiteCountUpdate },
                  accumulatedTextRef,
                  currentAgentRef,
                  setCurrentAgent
                );

                eventDataBuffer = "";
              }
            } else if (line.startsWith("data:")) {
              eventDataBuffer += line.substring(5).trimStart() + "\n";
            }
          }

          if (done) {
            if (eventDataBuffer.length > 0) {
              const jsonDataToParse = eventDataBuffer.endsWith("\n")
                ? eventDataBuffer.slice(0, -1)
                : eventDataBuffer;

              await processSseEventData(
                jsonDataToParse,
                aiMessageId,
                { onMessageUpdate, onEventUpdate, onWebsiteCountUpdate },
                accumulatedTextRef,
                currentAgentRef,
                setCurrentAgent
              );
            }
            return;
          }

          return pump();
        };

        await pump();
        
        // 🔥 CRITICAL FIX: Wait for React to finish all pending updates
        // This ensures all flushSync calls have completed before we set isLoading to false
        await new Promise(resolve => setTimeout(resolve, 0));
        
        console.log('[useStreaming] Stream completed, final accumulated text length:', accumulatedTextRef.current.length);
        
      } catch (error) {
        console.error("Streaming error:", error);
        throw error; // Re-throw to allow parent to handle
      } finally {
        // 🔥 CRITICAL FIX: Use setTimeout to ensure state updates complete
        // This gives React time to process all the flushSync updates before we signal completion
        setTimeout(() => {
          setIsLoading(false);
          console.log('[useStreaming] Loading state set to false');
        }, 10); // Small delay to ensure UI updates complete
      }
    },
    [onMessageUpdate, onEventUpdate, onWebsiteCountUpdate]
  );

  const cancelStream = useCallback(() => {
    if (connectionManager.current) {
      connectionManager.current.cancelRequest();
    }
    setIsLoading(false);
  }, []);

  const getEventTitleCallback = useCallback((agentName: string): string => {
    return getEventTitle(agentName);
  }, []);

  return {
    isLoading,
    currentAgent,
    startStream,
    cancelStream,
    getEventTitle: getEventTitleCallback,
  };
}