'use client'

import * as React from 'react'
import Textarea from 'react-textarea-autosize'
import { nanoid } from 'nanoid'
import { Button } from '@/components/ui/button'
import { IconArrowElbow } from '@/components/ui/icons'
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip'
import { useEnterSubmit } from '@/lib/hooks/use-enter-submit'
import { MessageUIState, currentMessagesUIState, toRequestMessageUI, toResponseMessageUI } from '@/lib/chat/actions'
import { chat, sleep } from '@/lib/utils'

export interface PromptFormProps {
  input: string
  setInput: (value: string) => void
  messages: MessageUIState
  setMessages: (uiState: MessageUIState) => void
}

export function PromptForm({input, setInput, messages, setMessages}: PromptFormProps) {
  const { formRef, onKeyDown } = useEnterSubmit()
  const inputRef = React.useRef<HTMLTextAreaElement>(null)

  React.useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus()
    }
  }, [])

  return (
    <form
      ref={formRef}
      onSubmit={async (e: any) => {
        e.preventDefault()

        // Blur focus on mobile
        if (window.innerWidth < 600) {
          e.target['message']?.blur()
        }

        const value = input.trim()
        setInput('')
        if (!value) return

        let currentMsgs: MessageUIState = currentMessagesUIState(messages, toRequestMessageUI(value), true)
        setMessages(currentMsgs)

        // Submit and get response message
        const responseMessage = await chat({id: nanoid(), content: value})

        // Update the chat list
        setMessages(currentMessagesUIState(currentMsgs, toResponseMessageUI(responseMessage.content), false))
      }}
    >
      <div className="relative flex max-h-60 w-full grow flex-col overflow-hidden bg-background px-8 sm:rounded-md sm:border sm:px-12">
        <Textarea
          ref={inputRef}
          tabIndex={0}
          onKeyDown={onKeyDown}
          placeholder="Send a message."
          className="min-h-[60px] w-full resize-none bg-transparent px-4 py-[1.3rem] focus-within:outline-none sm:text-sm"
          autoFocus
          spellCheck={false}
          autoComplete="off"
          autoCorrect="off"
          name="message"
          rows={1}
          value={input}
          onChange={e => setInput(e.target.value)}
        />
        <div className="absolute right-0 top-[13px] sm:right-4">
          <Tooltip>
            <TooltipTrigger asChild>
              <Button type="submit" size="icon" disabled={input === ''}>
                <IconArrowElbow />
                <span className="sr-only">Send message</span>
              </Button>
            </TooltipTrigger>
            <TooltipContent>Send message</TooltipContent>
          </Tooltip>
        </div>
      </div>
    </form>
  )
}
