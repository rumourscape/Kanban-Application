<template>
  <div>

    <h1 style="margin: 30px">{{ msg }}</h1>

    <b-button variant="primary" @click="increment()">count is: {{ count }}</b-button>
  </div>
</template>

<script>
export default {
  props: {
    msg: String,
  },
  data() {
    return {
      count: 0,
      a: "abc",
    };
  },
  methods: {
    increment() {
      this.count++;
    },
    get() {
      return this.count;
    }
  }
};
</script>