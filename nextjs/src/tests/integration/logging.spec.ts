
import { render, screen } from '@testing-library/react';
import { ChatProvider } from '@/components/chat/ChatProvider';
import { MessageArea } from '@/components/chat/MessageArea';
import { ChatInput } from '@/components/chat/ChatInput';

describe('Simple Test', () => {
  it('should render the component', () => {
    render(
      <ChatProvider>
        <MessageArea />
        <ChatInput />
      </ChatProvider>
    );
    expect(screen.getByText('No messages yet. Start a conversation!')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Add more details, ask questions, or request changes...')).toBeInTheDocument();
  });
});
