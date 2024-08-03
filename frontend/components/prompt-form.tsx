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

        console.log(messages.length)

        let currentMsgs: MessageUIState = currentMessagesUIState(messages, toRequestMessageUI(value), true)
        setMessages(currentMsgs)

        // Submit and get response message
        //const responseMessage = await chat({id: nanoid(), content: value})
        sleep(1000)
        const responseMessage = {
          content: "The Managed Cluster Status being offline in the AWS CloudFormation stack (ACM) Hub can be a frustrating issue!\n\nTo help you troubleshoot and potentially fix this issue, let's go through some steps together:\n\n1. **Check the CloudFormation Stack**: Ensure that your managed cluster is associated with an active CloudFormation stack. You can do this by navigating to the AWS Management Console, going to the ACM Hub, and checking the \"Managed Clusters\" tab. If you don't see your managed cluster listed, it might indicate that the CloudFormation stack is not properly configured or is deleted.\n\n2. **Verify the Managed Cluster Configuration**: Review the configuration of your managed cluster to ensure that:\n   - The managed cluster is correctly created and deployed.\n   - The cluster's status is set to \"CREATE_COMPLETE\" (or whatever the desired state is for your use case).\n   - The cluster's VPC, subnet, and security group configurations are correct.\n\n3. **Check the Amazon ECS Cluster**: Verify that the underlying Amazon Elastic Container Service (ECS) cluster associated with your managed cluster is healthy and running. You can do this by:\n   - Navigating to the AWS Management Console, going to the Amazon ECS dashboard, and checking the \"Clusters\" tab.\n   - Reviewing the ECS cluster's status, which should be set to \"ACTIVE\" or \"CREATE_IN_PROGRESS\".\n\n4. **Check the IAM Roles and Permissions**: Ensure that the IAM roles and permissions associated with your managed cluster are correct:\n   - Verify that the IAM role is assigned correctly to the CloudFormation stack and the managed cluster.\n   - Check that the managed cluster has the necessary permissions to create and manage the underlying ECS cluster.\n\n5. **Check the Managed Cluster's Status History**: Review the status history of your managed cluster in the ACM Hub to identify any potential issues or errors:\n   - Check for any error messages, warnings, or failed operations related to your managed cluster.\n   - Identify any recent changes or updates that might have caused the issue.\n\n6. **Try Rebooting or Reconfiguring the Managed Cluster**: If none of the above steps help, you can try rebooting or reconfiguring the managed cluster:\n   - Reboot the managed cluster by clicking on the \"Reboot\" button in the ACM Hub.\n   - Reconfigure the managed cluster by modifying its settings and updating any configurations that might be causing issues.\n\n7. **Contact AWS Support**: If none of these steps resolve the issue, it's likely a problem with your specific configuration or setup. You can contact AWS support for further assistance:\n   - Provide them with detailed information about your CloudFormation stack, managed cluster, and any error messages you've encountered.\n   - Work with the AWS support team to troubleshoot and resolve the issue.\n\nRemember to thoroughly review each step before proceeding to ensure you don't inadvertently make things worse. If you're still unsure or need further guidance, feel free to ask!"
        }

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
