/**
 * Connection Manager
 *
 * This module handles SSE streaming connection lifecycle management including
 * connection establishment, data streaming, error handling, and cleanup.
 */

import {
  SSEConnectionState,
  StreamingAPIPayload,
  ConnectionManagerOptions,
} from "./types";
import { createDebugLog } from "@/lib/handlers/run-sse-common";

/**
 * Manages SSE streaming connections
 */
export class StreamingConnectionManager {
  private connectionState: SSEConnectionState = "idle";
  private retryFn: <T>(fn: () => Promise<T>) => Promise<T>;
  private endpoint: string;
  private abortController: AbortController | null = null;

  constructor(options: ConnectionManagerOptions = {}) {
    this.retryFn = options.retryFn || ((fn) => fn());
    this.endpoint = options.endpoint || "/api/run_sse";
  }

  /**
   * Gets the current connection state
   */
  public getConnectionState(): SSEConnectionState {
    return this.connectionState;
  }

  /**
   * Starts a streaming connection and returns the response
   *
   * @param apiPayload - API request payload
   * @returns Promise that resolves with the fetch response
   */
  public async submitMessage(
    apiPayload: StreamingAPIPayload
  ): Promise<Response> {
    this.connectionState = "connecting";
    this.abortController = new AbortController();

    try {
      createDebugLog(
        "CONNECTION",
        "Sending API request with payload",
        apiPayload
      );

      const response = await this.retryFn(() =>
        fetch(this.endpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(apiPayload),
          signal: this.abortController?.signal,
        })
      );

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      this.connectionState = "connected";
      return response;
    } catch (error) {
      if ((error as Error).name === "AbortError") {
        this.connectionState = "closed";
        createDebugLog("CONNECTION", "Request was cancelled by the user");
      } else {
        this.connectionState = "error";
        createDebugLog("CONNECTION", "Streaming error", error);
      }
      throw error;
    }
  }

  /**
   * Cancels the current streaming connection
   */
  public cancelRequest(): void {
    if (this.abortController) {
      this.abortController.abort();
    }
    this.connectionState = "closed";
  }
}