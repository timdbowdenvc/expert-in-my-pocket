
import { logEvent, setLogLevel, LogLevel, redact } from './logging';

describe('logging utility', () => {
  let consoleSpy: jest.SpyInstance;
  const originalNodeEnv = process.env.NODE_ENV;

  beforeEach(() => {
    // Spy on console.log before each test
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    process.env.NODE_ENV = originalNodeEnv;
  });

  afterEach(() => {
    // Restore console.log after each test
    consoleSpy.mockRestore();
    // Reset log level
    setLogLevel(LogLevel.INFO);
    process.env.NODE_ENV = originalNodeEnv;
  });

  it('should log a message with the default log level', () => {
    logEvent('test event', { data: 'some data' });
    expect(consoleSpy).toHaveBeenCalledWith('[INFO] test event', { data: 'some data' });
  });

  it('should not log a message if the log level is lower than the current log level', () => {
    setLogLevel(LogLevel.WARN);
    logEvent('test event', { data: 'some data' }, LogLevel.INFO);
    expect(consoleSpy).not.toHaveBeenCalled();
  });

  it('should log a message if the log level is equal to or higher than the current log level', () => {
    setLogLevel(LogLevel.WARN);
    logEvent('test event', { data: 'some data' }, LogLevel.WARN);
    expect(consoleSpy).toHaveBeenCalledWith('[WARN] test event', { data: 'some data' });

    logEvent('another test event', { data: 'more data' }, LogLevel.ERROR);
    expect(consoleSpy).toHaveBeenCalledWith('[ERROR] another test event', { data: 'more data' });
  });

  it('should use cloudLog when in production environment', () => {
    process.env.NODE_ENV = 'production';
    logEvent('test event', { data: 'some data' });
    expect(consoleSpy).toHaveBeenCalledWith('[CLOUD] [INFO] test event', { data: 'some data' });
  });

  it('should redact sensitive data', () => {
    const sensitiveData = { prompt: 'this is a secret', other: 'this is not' };
    const redactedData = redact(sensitiveData);
    expect(redactedData.prompt).toBe('REDACTED');
    expect(redactedData.other).toBe('this is not');
  });
});
