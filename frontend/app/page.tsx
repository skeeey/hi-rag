'use client'

import { useState } from 'react'
import { ChatList } from '@/components/chat-list'
import { ChatPanel } from '@/components/chat-panel'
import { useScrollAnchor } from '@/lib/hooks/use-scroll-anchor'
import { MessageUIState } from '@/lib/chat/actions'
import { cn } from '@/lib/utils'

export default function Home() {
  const [input, setInput] = useState('')
  const uiState: MessageUIState = []
  const [messages, setMessages] = useState(uiState)
  const { messagesRef, scrollRef, visibilityRef, isAtBottom, scrollToBottom } = useScrollAnchor()

  return (
    <div
      className="group w-full overflow-auto pl-0 peer-[[data-state=open]]:lg:pl-[250px] peer-[[data-state=open]]:xl:pl-[300px]"
      ref={scrollRef}
    >
      <div
        className={cn('pb-[200px] pt-4 md:pt-10')}
        ref={messagesRef}
      >

      <ChatList messages={messages} />
      <div className="w-full h-px" ref={visibilityRef} />
      </div>
      <ChatPanel
        input={input}
        setInput={setInput}
        messages={messages}
        setMessages={setMessages}
        isAtBottom={isAtBottom}
        scrollToBottom={scrollToBottom}
      />
    </div>
  );
}
