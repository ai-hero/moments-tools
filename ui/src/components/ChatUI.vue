<script>
import { defineComponent } from 'vue'
import { v4 as uuidv4 } from 'uuid';
import { CubeTransparentIcon } from '@heroicons/vue/20/solid'

const CONFIG = {
  "version": 0.1,
  "config": {
    "variant": 1,
    "id": "cafe",
    "type": "llmopenai",
    "instructions": "You (the assistant) are a barista. You are helping a customer (the user) get their order. \nYour goal is to generate an order ticket at the end of the conversation. \nYou will welcome there into the cafe, and then ask them questions about their order. \nAlso, ask their name. When they are done, you must say: \n\"Alright! We'll let you know when your order is ready.\", followed by a summary of their order.\nDo not charge the customer. \n\nYOU CAN ONLY SPEAK ONE TURN AT A TIME.\n",
    "roles": {
      "user": "Customer",
      "assistant": "Barista"
    },
    "examples": [
      {
        "context": "The time is 08:01 AM.\n",
        "messages": [
          {
            "role": "assistant",
            "content": "Good morning! Welcome to In Search of Ikigai."
          },
          {
            "role": "user",
            "content": "Hello."
          },
          {
            "role": "assistant",
            "content": "What can I get you?"
          },
          {
            "role": "user",
            "content": "Can I get a cup of coffee please?"
          },
          {
            "role": "assistant",
            "content": "Sure. How would you like it?"
          },
          {
            "role": "user",
            "content": "Black, no sugar please."
          },
          {
            "role": "assistant",
            "content": "What size would that be?"
          },
          {
            "role": "user",
            "content": "8 oz."
          },
          {
            "role": "assistant",
            "content": "Great! We'll let you know when your order is ready."
          }
        ]
      }
    ],
    "begin": "Begin by welcoming them into our 'Way of Ikigai' cafe.\n",
    "sep_section": "-------",
    "sep_inline": "::"
  }
}

const DEFAULT_CONVERSATION = {
  bot_type: 'chatgpt',
  bot_id: 'cafe',
  bot_variant: '01',
  config_override: CONFIG,
}

export default defineComponent({
  name: "ChatUI",
  components: {
    CubeTransparentIcon
  },
  data() {
    return {
      conversationId: uuidv4(),
      conversation: DEFAULT_CONVERSATION,
      userMessage: ""
    }
  },
  mounted() {
    fetch(`/api/v1/conversations/${this.conversationId}`, {
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
      this.conversation.messages.push({ role: "user", content: this.userMessage });
      this.scrollToEnd()
      fetch(`/api/v1/conversations/${this.conversationId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(this.conversation)
      }).then(response => response.json())
        .then(data => {
          // handle the response
          this.conversation = data;
          this.scrollToEnd()
        })
        .catch(error => {
          // handle the error
          console.error(error)
        });
      this.userMessage = ""
    },
    scrollToEnd() {
      this.$nextTick(() => {
        var messages = this.$refs["messages"]
        messages.scrollTop = messages.scrollHeight
      })
    }
  },
})


</script>

<template>
  <div>
    <div class="container mx-auto min-h-[95vh]">
      <div class="min-w-full border border-gray-600 rounded">
        <div class="w-full">
          <div class="relative flex items-center p-3 border-b border-gray-600">
            {{ conversation.topic }}
          </div>
          <div class="relative w-full p-6 overflow-y-auto h-[40rem] scroll-auto" ref="messages">
            <ul class="space-y-2">
              <li v-for="interaction of conversation.messages">
                <div v-if="interaction.role == 'assistant'" class="flex justify-start items-center">
                  <div class="relative flex p-3">
                    <CubeTransparentIcon class="w-10 h-10" />
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
              class="block w-full py-2 pl-4 mx-3 bg-gray-100 rounded-full outline-none focus:text-gray-700" name="message"
              required />
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
    <div v-if="conversation.messages && conversation.messages[0].role == 'system'"
      class="flex justify-start items-center">
      <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
        <div class="block text-left whitespace-pre-line">{{ conversation.messages[0].content }}</div>
      </div>
    </div>
    <div></div>
  </div>
</template>

<style scoped></style>
