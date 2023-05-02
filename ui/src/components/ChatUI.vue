<script>
import { defineComponent } from 'vue'
import { v4 as uuidv4 } from 'uuid';
import { CubeTransparentIcon } from '@heroicons/vue/20/solid'

const CONFIG = {
  "apiVersion": 0.2,
  "kind": "LlmCohereAgent",
  "id": "cafebot",
  "variant": "01",
  "init": "\
    Instructions: \"You are a barista at the cafe 'ISO Ikigai'. You are serving customers of the cafe as they walk up to you. You will welcome them, and then ask them questions about their order. Also, ask their name. When they are done, you must say: \"Alright! We'll let you know when your order is ready.\", followed by a summary of their order. Do not charge the customer. You will only respond with your immediate turn. Your response should start with 'Self: ' followed by what your response is delimited by double quotes. Respond with only ONE interaction at a time.\"\n\
    Example: An example interaction with a customer - '''\\nContext: ```time: \"8:01am\"```\\nSelf: \"Good morning! Welcome to ISO Ikigai cafe.\"\\nCustomer (unknown): \"Hello.\"\\nSelf: (smile) \"What can I get you?\"\\nCustomer (unknown): \"Can I get a cup of coffee please?\"\\nSelf: \"Sure. How would you like it?\"\\nCustomer (unknown): \"Black, no sugar please.\"\\nSelf: \"What size would that be?\"\\nCustomer (unknown): \"8 oz.\"\\nSelf: \"Great! We'll let you know when your order is ready\".'''\n\
    Begin.\n\n\
  "
}

const DEFAULT_SNAPSHOT = {
  occurrences: [],
  __agent_config_override: CONFIG,
}

export default defineComponent({
  name: "ChatUI",
  components: {
    CubeTransparentIcon
  },
  data() {
    return {
      agentInstanceId: uuidv4(),
      momentId: uuidv4(),
      previousSnapshotId: null,
      snapshot: JSON.parse(JSON.stringify(DEFAULT_SNAPSHOT)),
      userMessage: ""
    }
  },
  mounted() {
    this.newConversation()
  },
  methods: {
    newConversation() {
      let request_snapshot = JSON.parse(JSON.stringify(DEFAULT_SNAPSHOT))
      request_snapshot.previous_snapshot_id = null;
      fetch(`/api/v1/agents/${this.agentInstanceId}/${this.momentId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(request_snapshot)
      }).then(response => response.json())
        .then(data => {
          // handle the response
          this.snapshot = data;
          this.previousSnapshotId = data.snapshot_id
        })
        .catch(error => {
          // handle the error
          console.error(error)
        });
    },
    onUserMessage() {
      this.snapshot.occurrences.push({ kind: "Participant", name: "Customer", identifier: "unknown", emotion: "", says: this.userMessage });
      this.snapshot.previous_snapshot_id = this.previousSnapshotId
      this.scrollToEnd()
      fetch(`/api/v1/agents/${this.agentInstanceId}/${this.momentId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(this.snapshot)
      }).then(response => response.json())
        .then(data => {
          // handle the response
          this.snapshot = data;
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
        var occurrences = this.$refs["occurrences"]
        occurrences.scrollTop = occurrences.scrollHeight
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
            Conversation with {{ agentInstanceId }} in moment {{ momentId }}
          </div>
          <div class="relative w-full p-6 overflow-y-auto h-[40rem] scroll-auto" ref="occurrences">
            <ul class="space-y-2">
              <li v-for="interaction of snapshot.occurrences">
                <div v-if="interaction.kind == 'Self'" class="flex justify-start items-center">
                  <div class="relative flex p-3">
                    <CubeTransparentIcon class="w-10 h-10" />
                  </div>
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 border border-gray-300 rounded">
                    <div class="block text-left">{{ interaction.says }}</div>
                  </div>
                </div>
                <div v-else-if="interaction.kind == 'Participant'" class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
                    <div class="block text-right">{{ interaction.says }}</div>
                  </div>
                </div>
                <div v-else-if="interaction.kind == 'Context'" class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
                    <div class="block text-right code">{{ interaction.context }}</div>
                  </div>
                </div>
                <div v-else-if="interaction.kind == 'Instructions'" class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
                    <div class="block text-right code">{{ interaction.instructions }}</div>
                  </div>
                </div>
                <div v-else-if="interaction.kind == 'Example'" class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
                    <div class="block text-right code">{{ interaction.example }}</div>
                  </div>
                </div>
                <div v-else-if="interaction.kind == 'Begin'" class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
                    <div class="block text-right code">Begin.</div>
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
    <div></div>
  </div>
</template>

<style scoped></style>
