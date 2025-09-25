
export enum LogLevel {
  DEBUG,
  INFO,
  WARN,
  ERROR,
}

let currentLogLevel = LogLevel.INFO;

export function setLogLevel(level: LogLevel) {
  currentLogLevel = level;
}

export function redact(data: any): any {
  const redactedData = { ...data };
  if (redactedData.prompt) {
    redactedData.prompt = 'REDACTED';
  }
  return redactedData;
}

function cloudLog(level: LogLevel, event: string, data: any) {
  // Placeholder for a cloud logging service like Google Cloud Logging
  console.log(`[CLOUD] [${LogLevel[level]}] ${event}`, redact(data));
}

export function logEvent(event: string, data: any, level: LogLevel = LogLevel.INFO) {
  if (level >= currentLogLevel) {
    if (process.env.NODE_ENV === 'production') {
      cloudLog(level, event, data);
    } else {
      console.log(`[${LogLevel[level]}] ${event}`, redact(data));
    }
  }
}
