import { useState, useCallback, useRef } from "react";
import { StreamingConnectionManager } from "@/lib/streaming/connection-manager";
import { getEventTitle } from "@/lib/streaming/stream-utils";
import {
  StreamingAPIPayload,
  StreamEvent,
} from "@/lib/streaming/types";

export interface UseStreamingReturn {
  isLoading: boolean;
  startStream: (
    apiPayload: { message: string; userId: string; sessionId: string }
  ) => ReadableStream<StreamEvent>;
  getEventTitle: (agentName: string) => string;
}

/**
 * Custom hook for managing SSE streaming connections and data processing
 */
export function useStreaming(
  retryFn: <T>(fn: () => Promise<T>) => Promise<T>
): UseStreamingReturn {
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const connectionManager = useRef<StreamingConnectionManager | null>(null);

  if (connectionManager.current === null) {
    connectionManager.current = new StreamingConnectionManager({
      retryFn,
      endpoint: "/api/run_sse",
    });
  }

  const startStream = useCallback(
    (
      apiPayload: { message: string; userId: string; sessionId: string }
    ): ReadableStream<StreamEvent> => {
      if (!connectionManager.current) {
        throw new Error("Connection manager not initialized");
      }

      const streamingPayload: StreamingAPIPayload = {
        message: apiPayload.message,
        userId: apiPayload.userId,
        sessionId: apiPayload.sessionId,
      };

      const stream = connectionManager.current.submitMessage(streamingPayload);

      const newStream = new ReadableStream<StreamEvent>({
        async start(controller) {
          setIsLoading(true);
          try {
            for await (const chunk of stream as any) {
              controller.enqueue(chunk);
            }
          } catch (error) {
            controller.error(error);
          } finally {
            setIsLoading(false);
            controller.close();
          }
        },
      });

      return newStream;
    },
    []
  );

  const getEventTitleCallback = useCallback((agentName: string): string => {
    return getEventTitle(agentName);
  }, []);

  return {
    isLoading,
    startStream,
    getEventTitle: getEventTitleCallback,
  };
}
