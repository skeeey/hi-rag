import { Separator } from '@/components/ui/separator'
import { MessageUIState } from '@/lib/chat/actions'

export interface ChatList {
  messages: MessageUIState
}

export function ChatList({ messages }: ChatList) {
  if (!messages.length) {
    return null
  }

  return (
    <div className="flex flex-col justify-start px-64 pt-8">
      {messages.map((message, index) => (
        <div key={message.id} id={message.id}>
          {message.display}
          {index < messages.length - 1 && <Separator className="my-4" />}
        </div>
      ))}
    </div>
  )
}
