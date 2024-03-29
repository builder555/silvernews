<script setup>
import { RouterView } from 'vue-router'
import TheHeader from './components/TheHeader.vue'
</script>

<template>
  <TheHeader />
  <RouterView />
</template>
<style>
*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-weight: normal;
}
html, body {
  height: 100%;
}
body.dark {
  --bg-color: #000;
  --bg-secondary-color: #131316;
  --font-color: #f5f5f5;
  --color-grey: #ccc;
  --color-darkGrey: #777;
}
:root {
  --color-warning: #ffcc00;
}
/* .button.warning {
  background-color: var(--color-warning);
  color: var(--font-color);
} */
.warning {
  color: var(--color-warning);
}
</style>