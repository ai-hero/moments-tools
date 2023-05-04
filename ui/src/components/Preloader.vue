<template>
  <div class="flex">
    <span>{{ theText }}{{ dots }}</span>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { ArrowPathIcon } from "@heroicons/vue/24/outline";

export default defineComponent({
  name: "preloader",
  props: ["theText"],
  data() {
    return {
      counter: 0,
      dots: "...",
      timeoutId: null,
    };
  },
  components: {
    ArrowPathIcon,
  },
  mounted() {
    this.inc();
  },
  unmounted() {
    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  },
  methods: {
    inc() {
      this.counter = (this.counter + 1) % 3;
      if (this.counter == 0) {
        this.dots = ".";
      } else if (this.counter == 1) {
        this.dots = "..";
      } else if (this.counter == 2) {
        this.dots = "...";
      }
      this.timeoutId = setTimeout(this.inc, 500);
    },
  },
});
</script>
