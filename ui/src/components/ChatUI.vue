<script>
import { defineComponent } from 'vue'
import { v4 as uuidv4 } from 'uuid';
import { CubeTransparentIcon, ArrowPathIcon, PencilIcon } from '@heroicons/vue/20/solid'
import Preloader from './Preloader.vue'

const CONFIG = {
  mdl: "0.2.2",
  kind: "LlmCohereAgent",
  id: "cafebot",
  variant: "experiment",
  init: "\
    Instructions: You are a barista at the cafe 'ISO Ikigai'. You are serving customers of the cafe as they walk up to you. You will welcome them, and then ask them questions about their order. Also, ask their name. When they are done, you must say: \"Alright! We'll let you know when your order is ready.\", followed by a summary of their order. Do not charge the customer. You will only respond with your immediate turn. Your response should start with 'Self: ' followed by what your response is delimited by double quotes. Respond with only ONE interaction at a time.\n\
    Example: An example interaction with a customer - '''\\nContext: ```time: \"8:01am\"```\\nSelf: \"Good morning! Welcome to ISO Ikigai cafe.\"\\nCustomer (unknown): \"Hello.\"\\nSelf: (smile) \"What can I get you?\"\\nCustomer (unknown): \"Can I get a cup of coffee please?\"\\nSelf: \"Sure. How would you like it?\"\\nCustomer (unknown): \"Black, no sugar please.\"\\nSelf: \"What size would that be?\"\\nCustomer (unknown): \"8 oz.\"\\nSelf: \"Great! We'll let you know when your order is ready.\"'''\n\
    Begin.\n\n\
  "
}

export default defineComponent({
  name: "ChatUI",
  components: {
    CubeTransparentIcon,
    ArrowPathIcon,
    PencilIcon,
    Preloader
  },
  data() {
    return {
      isLoading: true,
      mode: "use",
      error: "",
      agentInstanceId: uuidv4(),
      previousSnapshotId: null,
      snapshot: { id: uuidv4(), moment: { id: uuidv4(), occurrences: [] } }, // Temporary
      userMessage: "",
      history: []
    }
  },
  mounted() {
    if (this.$route.query && this.$route.query.mode) {
      this.mode = this.$route.query.mode
    }
    this.newConversation()
  },
  methods: {
    newConversation() {
      this.error = ""
      this.isLoading = true
      this.snapshot.previous_snapshot_id = null;
      this.snapshot.__agent_config_override = CONFIG;
      fetch(`/api/v1/agents/${this.agentInstanceId}/moments`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(this.snapshot)
      }).then(response => response.json())
        .then(data => {
          // handle the response
          this.history.push(JSON.parse(JSON.stringify(data)))
          this.snapshot = JSON.parse(JSON.stringify(data));
          this.previousSnapshotId = data.id
          this.complete()
        })
        .catch(error => {
          // handle the error
          console.error(error)
          this.error = `${error}`;
        }).finally(() => {

        });
    },
    onUserMessage() {
      this.isLoading = true
      this.error = ""
      this.snapshot.moment.occurrences.push({ kind: "Participant", content: { name: "Customer", identifier: "unknown", emotion: "", says: this.userMessage } });
      this.snapshot.previous_snapshot_id = this.previousSnapshotId
      this.scrollToEnd()
      this.history.push(JSON.parse(JSON.stringify(this.snapshot)));
      this.complete()
      this.userMessage = ""
    },
    refetch() {
      this.isLoading = true
      this.error = ""
      this.history.pop()
      this.snapshot = JSON.parse(JSON.stringify(this.history[this.history.length - 1]));
      this.complete()
    },
    rollback() {
      let lastSnapshot = null;
      let lastOccurrences = null;
      while (this.history.length > 2) {
        lastSnapshot = this.history.pop()
        lastOccurrences = lastSnapshot.moment.occurrences;
        if (lastOccurrences[lastOccurrences.length - 1].kind == 'Participant')
          break
      }
      if (lastOccurrences) {
        this.userMessage = lastOccurrences[lastOccurrences.length - 1].content.says
      }
      this.snapshot = this.history[this.history.length - 1];
    },
    complete() {
      fetch(`/api/v1/agents/${this.agentInstanceId}/moments/${this.snapshot.moment.id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(this.snapshot)
      }).then(response => response.json())
        .then(data => {
          // handle the response
          this.history.push(JSON.parse(JSON.stringify(data)));
          console.log("Snapshot: ", data)
          this.snapshot = JSON.parse(JSON.stringify(data));
          this.previousSnapshotId = data.id
          this.scrollToEnd()
        })
        .catch(error => {
          // handle the error
          console.error(error)
          this.error = `${error}`;
        }).finally(() => {
          this.isLoading = false;
        });
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
            <div v-if="error" class="text-red-600">{{ error }}</div>
          </div>
          <div class="relative w-full p-6 overflow-y-auto h-[40rem] scroll-auto" ref="occurrences">
            <ul class="space-y-2">
              <li v-for="interaction of snapshot.moment.occurrences">
                <div v-if="interaction.kind == 'Self'" class="flex justify-start items-center">
                  <div class="relative flex p-3">
                    <CubeTransparentIcon class="w-10 h-10" />
                  </div>
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 border border-gray-300 rounded">
                    <div class="block text-left">{{ interaction.content.says }}</div>
                  </div>
                  <ArrowPathIcon v-if="!isLoading" class="w-4 h-4 text-gray-400 hover:text-gray-700 ml-2 hand"
                    @click="refetch" />
                </div>
                <div v-else-if="interaction.kind == 'Participant'" class="flex justify-end items-center">
                  <PencilIcon v-if="!isLoading" class="w-4 h-4 text-gray-400 hover:text-gray-700 mr-2 hand"
                    @click="rollback" />
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-100 border border-gray-300 rounded">
                    <div class="block text-right">{{ interaction.content.says }}</div>
                  </div>
                </div>
                <div v-else-if="mode == 'dev' && interaction.kind == 'Context'" class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-400 border border-gray-300 rounded">
                    <div class="block text-right code">Context: {{ interaction.content }}</div>
                  </div>
                </div>
                <div v-else-if="mode == 'dev' && interaction.kind == 'Instructions'"
                  class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-400 border border-gray-300 rounded">
                    <div class="block text-right code">Instructions: {{ interaction.content }}</div>
                  </div>
                </div>
                <div v-else-if="mode == 'dev' && interaction.kind == 'Example'" class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-400 border border-gray-300 rounded">
                    <div class="block text-right code">Example: {{ interaction.content.title }} - {{
                      interaction.content.example }}
                    </div>
                  </div>
                </div>
                <div v-else-if="mode == 'dev' && interaction.kind == 'Begin'" class="flex justify-end items-center">
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 bg-gray-400 border border-gray-300 rounded">
                    <div class="block text-right code">Begin.</div>
                  </div>
                </div>
              </li>
              <li v-if="isLoading">
                <div class="flex justify-start items-center">
                  <div class="relative flex p-3">
                    <CubeTransparentIcon class="w-10 h-10" />
                  </div>
                  <div class="relative max-w-xl px-4 py-2 text-gray-700 border border-gray-300 rounded">
                    <div class="block text-left">
                      <Preloader theText="" />
                    </div>
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
