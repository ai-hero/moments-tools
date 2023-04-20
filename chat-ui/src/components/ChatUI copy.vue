<script setup>
import { ref, onMounted } from 'vue'
import { UserIcon } from '@heroicons/vue/20/solid'


// reactive state
const selectedConversation = ref(0)

const conversations = [{
  topic: "Hello World",
  when: "Today, 3:26 pm",
  messages: [
    {
      speaker: "user",
      text: 'Hi.',
    },
    {
      speaker: "agent",
      text: 'Hi User.',
    },
    {
      speaker: "agent",
      text: 'How can I help?',
    },
  ],
},
{
  topic: "Bye world",
  when: "Today, 4:13 am",
  messages: [
    {
      speaker: "user",
      text: 'Bye.',
    },
    {
      speaker: "agent",
      text: 'Good bye.',
    },
    {
      speaker: "agent",
      text: 'Come back soon.',
    },
  ],
}]
const conversation = ref(conversations[selectedConversation.value])

// functions that mutate state and trigger updates
function selectConversation(index) {
  selectedConversation.value = index;
  conversation.value = conversations[selectedConversation.value];
}

// lifecycle hooks
onMounted(async () => {
  console.log(`The initial selectedConversation is ${selectedConversation.value}.`)
  let user = {
    bot_id: 'one',
    bot_type: 'openai'
  };

  let response = await fetch('/api/v1/conversations/1', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify(user)
  })

  let result = await response.json();
  console.log(result);
  result.topic = "Ordering at a cafe";
  result.when = "Today, 3:26 pm";
  conversation.value = result;
})

</script>

<template>
  <div class="container mx-auto min-h-[95vh]">
    <div class="min-w-full border border-gray-600 rounded lg:grid lg:grid-cols-3">
      <div class="border-r border-gray-600 lg:col-span-1">
        <div class="px-3 py-3 border-b border-gray-600">
          <div class="relative text-gray-600 text-center flex items-center">
            <h2 class="w-5/6 my-2 mb-2 ml-2 text-lg text-gray-600">Conversations</h2>
            <button class="w-1/6 my-2 mb-2 ml-2 text-lg text-gray-600 hover:text-rose-600 active:text-gray-300">+</button>
          </div>
        </div>
        <ul class="overflow-auto h-[32rem]">
          <li v-for="(conversation, index) in conversations">
            <a @click="selectConversation(index)"
              class="flex items-center px-3 py-2 text-sm transition duration-150 ease-in-out border-b border-gray-300 cursor-pointer hover:bg-gray-100 focus:outline-none">
              <div class="w-full py-2 items-center">
                <div class="text-left">
                  <span class="block ml-2 text-gray-600">{{ conversation.topic }}</span>
                  <span class="block ml-2 text-xs text-gray-400">{{ conversation.when }}</span>
                </div>
              </div>
            </a>
          </li>
        </ul>
      </div>
      <div class="hidden lg:col-span-2 lg:block">
        <div class="w-full">
          <div class="relative flex items-center p-3 border-b border-gray-600">
            {{ conversation.topic }}
          </div>
          <div class="relative w-full p-6 overflow-y-auto h-[40rem]">
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
                <div v-if="interaction.role == 'system'" class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
                    <div class="block text-right">{{ interaction.content }}</div>
                  </div>
                </div>
              </li>
            </ul>
          </div>

          <div class="flex items-center justify-between w-full p-3 border-t border-gray-300">
            <input type="text" placeholder="Message"
              class="block w-full py-2 pl-4 mx-3 bg-gray-100 rounded-full outline-none focus:text-gray-700" name="message"
              required />
            <button type="submit">
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
</template>

<style scoped></style>
