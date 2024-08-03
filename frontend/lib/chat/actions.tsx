import { nanoid } from 'nanoid'
import { UserMessage, BotMessage, SpinnerMessage } from '@/components/message'

export type MessageUI = {
    id: string
    display: React.ReactNode
}

export type MessageUIState = MessageUI[]

export const toRequestMessageUI = (req: string) => {
    return {
        id: nanoid(),
        display: (<UserMessage content={req}/>)
    }
}

export const toResponseMessageUI = (resp: string) => {
    return {
        id: nanoid(),
        display:(<BotMessage content={resp}/>)
    }
}

export const currentMessagesUIState = (msgs: MessageUIState, msg: MessageUI, req: boolean) => {
    if (req) {
        return [...msgs, msg, {id: nanoid(), display: (<SpinnerMessage />)}]
    }

    msgs = msgs.slice(0, msgs.length - 1)
    return [...msgs, msg]
}
  