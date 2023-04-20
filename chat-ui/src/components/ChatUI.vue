<script>
import { defineComponent } from 'vue'
import { UserIcon } from '@heroicons/vue/20/solid'

const PROMPT = `
You (the assistant) are a barista. You are helping a customer (the user) get their order. 
Your goal is to generate an order ticket at the end of the conversation. 
You will welcome there into the cafe, and then ask them questions about their order. 
Also, ask their name. When they are done, you must say: 
"Alright! We'll let you know when your order is ready.", followed by a summary of their order.
Do not charge the customer. 

YOU CAN ONLY SPEAK ONE TURN AT A TIME.

Here is an example:
You: Hi! welcome to the rainbow cafe! How may I help you?
Customer: Can I get a large tea please?
You: Sure, what kind of tea?
Customer: Earl gray.
You: Any sugar?
Customer: Unsweetend please.
You: Will that be all?
Customer: Yes.
You: Alright! We'll let you know when your order is ready.

Begin by welcoming them into our 'CafeGPT' cafe and asking them what they'd like to drink.
`
const DEFAULT_CONVERSATION = {
  bot_id: 'one',
  bot_type: 'openai',
  topic: "Ordering at the cafe",
  when: `${new Date().toISOString()}`,
  messages: [
    {
      role: "system",
      content: PROMPT,
    }
  ],
}

export default defineComponent({
  name: "ChatUI",
  components: {
    UserIcon
  },
  data() {
    return {
      conversation: DEFAULT_CONVERSATION,
      userMessage: ""
    }
  },
  mounted() {
    console.log(this.userMessage)
    fetch('/api/v1/conversations/1', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(DEFAULT_CONVERSATION)
    }).then(response => response.json())
      .then(data => {
        // handle the response
        this.conversation = data;
      })
      .catch(error => {
        // handle the error
        console.error(error)
      });
  },
  methods: {
    onUserMessage() {
      this.conversation.messages.push({ role: "user", content: this.userMessage })
      fetch('/api/v1/conversations/1', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(this.conversation)
      }).then(response => response.json())
        .then(data => {
          // handle the response
          this.conversation = data;
        })
        .catch(error => {
          // handle the error
          console.error(error)
        });
      this.userMessage = ""
    },
  },
})


</script>

<template>
  <div>
    <div class="container mx-auto min-h-[95vh]">
      <div class="min-w-full border border-gray-600 rounded">
        <div class="">
          <div class="w-full">
            <div class="relative flex items-center p-3 border-b border-gray-600">
              {{ conversation.topic }}
            </div>
            <div class="relative w-full p-6 overflow-y-auto h-[40rem] scroll-auto">
              <ul class="space-y-2">
                <li v-for="interaction of conversation.messages">
                  <div v-if="interaction.role == 'assistant'" class="flex justify-start items-center">
                    <div class="relative flex p-3">
                      <UserIcon class="w-10 h-10" />
                    </div>
                    <div class="relative max-w-xl px-4 py-2 text-gray-700 border border-gray-300 rounded">
                      <div class="block text-left">{{ interaction.content }}</div>
                    </div>
                  </div>
                  <div v-if="interaction.role == 'user'" class="flex justify-end items-center">
                    <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
                      <div class="block text-right">{{ interaction.content }}</div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>

            <div class="flex items-center justify-between w-full p-3 border-t border-gray-300">
              <input type="text" placeholder="Message" v-model="userMessage" @keyup.enter="onUserMessage"
                class="block w-full py-2 pl-4 mx-3 bg-gray-100 rounded-full outline-none focus:text-gray-700"
                name="message" required />
              <button type="submit" @click="onUserMessage">
                <svg class="w-5 h-5 text-gray-500 origin-center transform rotate-90" xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20" fill="currentColor">
                  <path
                    d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="conversation.messages[0].role == 'system'" class="flex justify-start items-center">
      <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
        <div class="block text-left whitespace-pre-line">{{ conversation.messages[0].content }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
