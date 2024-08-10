import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { Message } from '@/lib/types'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const sleep = (ms: number) =>
  new Promise(resolve => setTimeout(resolve, ms))

export async function chat (msg: Message) {
  const response = await fetch(process.env.NEXT_PUBLIC_API_URL + "/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json", Accept: 'application/json'},
    body: JSON.stringify(msg),
    signal: AbortSignal.timeout(600000) // 10 mins
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json() as Message
  return result 
}

