import { describe, it, expect, beforeEach } from 'vitest';
import { useChatStore } from '@/store/chatStore';

describe('Chat Store', () => {
  beforeEach(() => {
    // Reset store before each test
    useChatStore.setState({
      isStreaming: false,
      streamingContent: '',
      inputValue: '',
      selectedModel: 'gpt-5',
      sidebarOpen: true,
    });
  });

  it('should initialize with default values', () => {
    const state = useChatStore.getState();
    expect(state.isStreaming).toBe(false);
    expect(state.streamingContent).toBe('');
    expect(state.inputValue).toBe('');
    expect(state.selectedModel).toBe('gpt-5');
    expect(state.sidebarOpen).toBe(true);
  });

  it('should set streaming state', () => {
    const { setIsStreaming } = useChatStore.getState();
    setIsStreaming(true);
    expect(useChatStore.getState().isStreaming).toBe(true);
  });

  it('should set streaming content', () => {
    const { setStreamingContent } = useChatStore.getState();
    setStreamingContent('Test content');
    expect(useChatStore.getState().streamingContent).toBe('Test content');
  });

  it('should append streaming content', () => {
    const { setStreamingContent, appendStreamingContent } = useChatStore.getState();
    setStreamingContent('Hello ');
    appendStreamingContent('World');
    expect(useChatStore.getState().streamingContent).toBe('Hello World');
  });

  it('should set input value', () => {
    const { setInputValue } = useChatStore.getState();
    setInputValue('Test input');
    expect(useChatStore.getState().inputValue).toBe('Test input');
  });

  it('should set selected model', () => {
    const { setSelectedModel } = useChatStore.getState();
    setSelectedModel('claude-3-opus');
    expect(useChatStore.getState().selectedModel).toBe('claude-3-opus');
  });

  it('should toggle sidebar', () => {
    const { toggleSidebar } = useChatStore.getState();
    toggleSidebar();
    expect(useChatStore.getState().sidebarOpen).toBe(false);
    toggleSidebar();
    expect(useChatStore.getState().sidebarOpen).toBe(true);
  });

  it('should reset state', () => {
    const { setIsStreaming, setStreamingContent, setInputValue, reset } = useChatStore.getState();

    // Set some values
    setIsStreaming(true);
    setStreamingContent('Test');
    setInputValue('Input');

    // Reset
    reset();

    const state = useChatStore.getState();
    expect(state.isStreaming).toBe(false);
    expect(state.streamingContent).toBe('');
    expect(state.inputValue).toBe('');
  });
});
